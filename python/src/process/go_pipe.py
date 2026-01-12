import hashlib
import subprocess
import time
import os
from dataset import *

if os.path.exists("go/bin/perftest"):
    go_bin_path = "go/bin/perftest"
if os.path.exists("./../go/bin/perftest"):
    go_bin_path = "./../go/bin/perftest"

def proc_count_words(string:str, method):
    '''
    Count words using Go app using pipe communication

    :param string:
    :param method: one of count_words_pipe_chunked, count_words_pipe, count_words_pipe_scanner
    :return:
    '''
    proc = subprocess.Popen(
        #["wc", "-w"],
        [go_bin_path, method],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    # full encode and write
    proc.stdin.write(string.encode())
    proc.stdin.close()
    out = proc.stdout.read(1000).decode()
    out = int(out)
    return out