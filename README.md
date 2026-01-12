# Benchmarking of Python and Go integration

### Goal is to understand 
 - How Go might be used in Python projects
 - What are major bottlenecks

### Usage scenarios:
 - Many calls, small data exchange, simple processing (for example, word count)
 - Single call with large data exchange, simple processing (for example, word count)

### Transport type and execution environment
 - Pure python
 - Go shared library, using Python ctypes
 - Go app, using pipes
 - Go app, using GRPC on unix socket

### Run
Requires 16GB+ memory for all tests (mem usage not not optimised).
To run in docker use `./docker-run.sh`

## Benchmark results:
#### Macbook Pro M1 PRO
```
Testing with large dataset = 1 GB, repeat_calls = 1 M times
Count words / Go shared lib:                    954 ms
Count words / Go pipe:                        1,496 ms
Count words / Go pipe, chunked:               1,005 ms
Count words / Go pipe, scanner:               4,829 ms
Count words / pure Python:                   10,009 ms
Count words / Go GRPC:                       15,440 ms
Repeated calls / Pure Python:                   234 ms
Repeated calls / Go shared lib:                 321 ms
Repeated calls / Go GRPC:                   255,886 ms
```

#### Macbook Pro M1 PRO / docker
```
Testing with large dataset = 1 GB, repeat_calls = 1 M times
Count words / Go shared lib:                  1,940 ms
Count words / Go pipe:                        3,597 ms
Count words / Go pipe, chunked:               1,210 ms
Count words / Go pipe, scanner:               5,060 ms
Count words / pure Python:                   11,529 ms
Count words / Go GRPC:                       40,263 ms
Repeated calls / Pure Python:                   225 ms
Repeated calls / Go shared lib:                 402 ms
Repeated calls / Go GRPC:                   422,168 ms
```