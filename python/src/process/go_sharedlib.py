import hashlib
import os.path
import subprocess
import time
import ctypes
from dataset import *

if os.path.exists("go/bin/perftest.so"):
    lib = ctypes.CDLL("go/bin/perftest.so")
if os.path.exists("./../go/bin/perftest.so"):
    lib = ctypes.CDLL("./../go/bin/perftest.so")

lib.CountWordsC.argtypes = [ctypes.c_char_p]
lib.CountWordsC.restype = ctypes.c_int64

def proc_count_words(string:str):
    '''
    Count words using Go app as shared lib

    :param string:
    :return:
    '''
    return lib.CountWordsC(string.encode())