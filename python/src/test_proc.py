import pytest

from dataset import *
from process import pure_python
from process import go_pipe


class TestWordCount:

    def testPurePythonProc(self):
        dataset, word_count = get_word_count_dataset(1000)
        assert pure_python.proc_count_words(dataset) == word_count

    def testGoPipeProc(self):
        dataset, word_count = get_word_count_dataset(1000)
        assert go_pipe.proc_count_words(dataset) == word_count