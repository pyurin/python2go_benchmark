import time

class Timer:

    ts = None
    measurements = []
    context_label = None
    print = False
    multiplier = 1

    def __init__(self, context_label, print = True, multiplier = 1):
        self.context_label = context_label
        self.print = print
        self.multiplier = multiplier

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.print:
            print(f"{self.context_label+':':<40} {(time.time() - self.ts) * self.multiplier * 1000:10,.0f} ms")
        else:
            self.stop(self.context_label, self.multiplier)
        return False

    @classmethod
    def start(cls):
        cls.ts = time.time()

    @classmethod
    def stop(cls, label, multiplier = 1):
        cls.measurements.append(
            (label, (time.time() - cls.ts) * multiplier)
        )

    @classmethod
    def print(cls):
        for measurement in cls.measurements:
            label, ts = measurement
            print(f"{label}: {ts * 1000:,.0f} ms")