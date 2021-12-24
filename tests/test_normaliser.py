from python_homework_nlp.normaliser import get_stems, tokenize


class TestNormaliser:
    def test_get_stems(self):
        actual = "look looking looked"
        exp = ["look"] * 3
        assert get_stems(actual) == exp

    def test_tokenize(self):
        actual = (
            "At eight o'clock on Thursday morning Arthur didn't feel very good."
        )
        exp = [
            "At",
            "eight",
            "o'clock",
            "on",
            "Thursday",
            "morning",
            "Arthur",
            "did",
            "n't",
            "feel",
            "very",
            "good",
            ".",
        ]
        assert tokenize(actual) == exp
