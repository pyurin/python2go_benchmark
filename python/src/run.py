from dataset import *
import datetime
from process import pure_python, go_pipe, go_sharedlib, go_grpc
from process.go_grpc import start_grpc_server
from timer import Timer

if __name__ == "__main__":


    small_dataset = "small data set"
    small_ds_wc = 3
    repeat_calls = 1_000_000
    large_ds_size = 1_000_000_000
    large_dataset, large_ds_wc = get_word_count_dataset(large_ds_size)

    start_grpc_server()

    print(f"Testing with large "
          f"dataset = {large_ds_size / 1_000_000_000:,.0f} GB, "
          f"repeat_calls = {repeat_calls / 1_000_000:,.0f} M times")

    with Timer("Count words / Go shared lib"):
        assert large_ds_wc == go_sharedlib.proc_count_words(large_dataset)

    with Timer("Count words / Go pipe"):
        assert large_ds_wc == go_pipe.proc_count_words(large_dataset, 'count_words_pipe')

    with Timer("Count words / Go pipe, chunked"):
        assert large_ds_wc == go_pipe.proc_count_words(large_dataset, 'count_words_pipe_chunked')

    with Timer("Count words / Go pipe, scanner"):
        assert large_ds_wc == go_pipe.proc_count_words(large_dataset, 'count_words_pipe_scanner')

    with Timer('Count words / pure Python'):
        assert large_ds_wc == pure_python.proc_count_words(large_dataset)

    with Timer("Count words / Go GRPC"):
        assert large_ds_wc == go_grpc.proc_count_words(large_dataset)

    with Timer('Repeated calls / Pure Python'):
        for _ in range(repeat_calls):
            assert small_ds_wc == pure_python.proc_count_words(small_dataset)

    with Timer('Repeated calls / Go shared lib'):
        for _ in range(repeat_calls):
            assert small_ds_wc == go_sharedlib.proc_count_words(small_dataset)

    with Timer('Repeated calls / Go GRPC', multiplier = 10):
        for _ in range(int(repeat_calls / 10)):
            assert small_ds_wc == go_grpc.proc_count_words(small_dataset)
