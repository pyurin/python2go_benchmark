import re

WORD_PATTERN = "here will be some patter we'll use for words, only ASCII "
datasets = {}

SHA256_SRC = "some string"
SHA256_RESULT = "61d034473102d7dac305902770471fd50f4c5b26f6831a56dd90b5184b3c30fc"

def count_words(data:str):
    return len(re.findall('[^\\s\\n\\t]+', data))

def get_word_count_dataset(dataset_max_size):
    """
    Generates dataset string of repeated word pattern not longer than dataset_max_size.
    Not generator, static string. Pattern is repeated only entirely.

    Args:
        dataset_max_size (int): max dataset size in bytes

    Returns:
        str
    """
    pattern_byte_len = len(WORD_PATTERN.encode('UTF-8'))
    pattern_word_count = count_words(WORD_PATTERN)
    if dataset_max_size not in datasets:
        entire_pattern_count = dataset_max_size // pattern_byte_len
        datasets[dataset_max_size] = (
            WORD_PATTERN * entire_pattern_count,
            pattern_word_count * entire_pattern_count
        )

    return datasets[dataset_max_size]