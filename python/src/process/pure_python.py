import hashlib
import time
from dataset import *

def proc_count_words(string:str):
    return len([1 for s in string.split(' ') if s])