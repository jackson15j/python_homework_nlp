import pytest
from python_homework_nlp.normaliser import get_stems, tokenize


class TestNormaliser:
    @pytest.mark.parametrize(
        "actual,exp", ((["look", "looking", "looked"], ["look"] * 3),)
    )
    def test_get_stems(self, actual, exp):
        assert get_stems(actual) == exp

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
