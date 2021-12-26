import pytest
from nltk.corpus import stopwords
from python_homework_nlp.normaliser import (
    counter,
    get_stems,
    get_tokens_without_stopwords,
    tokenize,
    STOPWORDS_EN,
)


class TestNormaliser:
    @pytest.mark.parametrize(
        "actual,exp", ((["look", "looking", "looked"], ["look"] * 3),)
    )
    def test_get_stems(self, actual, exp):
        assert get_stems(actual) == exp

    @pytest.mark.parametrize(
        "actual,exp,stop_words",
        (
            (
                ["This", "is", "a", "sentence", "with", "stopwords", "."],
                ["This", "sentence", "stopwords", "."],
                stopwords.words("english"),
            ),
            (
                ["This", "is", "a", "sentence", "with", "stopwords", "."],
                ["This", "sentence", "stopwords"],
                None,
            ),
            (
                ["This", "is", "a", "sentence", "with", "stopwords", "."],
                ["This", "sentence", "stopwords"],
                STOPWORDS_EN,
            ),
        ),
    )
    def test_get_tokens_without_stopwords(self, actual, exp, stop_words):
        if stop_words:
            assert get_tokens_without_stopwords(actual, stop_words) == exp
        else:
            assert get_tokens_without_stopwords(actual) == exp

    @pytest.mark.parametrize(
        "actual,exp",
        (
            (
                "Arthur didn't feel good at eight o'clock.",
                [
                    [
                        "Arthur",
                        "did",
                        "n't",
                        "feel",
                        "good",
                        "at",
                        "eight",
                        "o'clock",
                        ".",
                    ],
                ],
            ),
            (
                "First sentence. Second sentence.",
                [["First", "sentence", "."], ["Second", "sentence", "."]],
            ),
        ),
    )
    def test_tokenize(self, actual, exp):
        assert tokenize(actual) == exp

    def test_counter(self):
        actual = {
            "file1": {
                "original_sentences": [
                    "First sentence.",
                    "Second is sentences.",
                    "Final SENTENCE!",
                ],
                "filtered_tokens": [
                    ["first", "sentence"],
                    ["second", "sentence"],
                    ["final", "sentence"],
                ],
            }
        }
        exp = {
            "final": {
                "count": 1,
                "matches": ["Final SENTENCE!"],
                "files": [
                    "file1",
                ],
            },
            "first": {
                "count": 1,
                "matches": ["First sentence."],
                "files": [
                    "file1",
                ],
            },
            "second": {
                "count": 1,
                "matches": ["Second is sentences."],
                "files": [
                    "file1",
                ],
            },
            "sentence": {
                "count": 3,
                "matches": [
                    "First sentence.",
                    "Second is sentences.",
                    "Final SENTENCE!",
                ],
                "files": [
                    "file1",
                ],
            },
        }
        assert counter(actual) == exp
