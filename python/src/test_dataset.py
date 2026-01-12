import pytest

from dataset import *


class TestDataset:

    def test1(self):
        assert count_words('') == 0
        assert count_words('hello') == 1
        assert count_words('hello ') == 1
        assert count_words('two words') == 2


    def test2(self):
        for dataset_len in [3, 100, 99, 203, 1000]:
            dataset, word_count = get_word_count_dataset(dataset_len)
            l1 = len(dataset.encode('UTF-8'))
            l2 = len(WORD_PATTERN.encode('UTF-8')) * (dataset_len // len(WORD_PATTERN.encode('UTF-8')))
            if l1 != l2:
                pytest.fail(f"Data len not correct for dataset len = {dataset_len}, expected {l1}, got {l2}")
            c1, c2 = word_count, count_words(dataset)
            if c1 != c2:
                pytest.fail(f"Word count correct for dataset len = {dataset_len}, expected {c1}, got {c2}")