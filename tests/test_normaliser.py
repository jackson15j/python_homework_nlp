import pytest
from nltk.corpus import stopwords
from python_homework_nlp.normaliser import (
    Normaliser,
    STOPWORDS_EN,
)


class TestNormaliser:
    @pytest.mark.parametrize(
        "actual,exp", ((["look", "looking", "looked"], ["look"] * 3),)
    )
    def test_get_stems(self, actual, exp):
        normaliser = Normaliser("")
        normaliser._get_stems(actual)
        assert normaliser.filtered_tokens == exp

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
    def test__get_tokens_without_stopwords(self, actual, exp, stop_words):
        if stop_words:
            assert (
                Normaliser._get_tokens_without_stopwords(actual, stop_words)
                == exp
            )
        else:
            assert Normaliser._get_tokens_without_stopwords(actual) == exp

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
        normaliser = Normaliser(actual)
        normaliser._tokenize()
        assert normaliser.original_tokens == exp
