import pytest
from nltk.corpus import stopwords
from python_homework_nlp.common import Content
from python_homework_nlp.normaliser import (
    Normaliser,
    STOPWORDS_EN,
)


class TestNormaliser:
    @pytest.mark.parametrize(
        "actual,exp", ((["look", "looking", "looked"], ["look"] * 3),)
    )
    def test_get_stems(self, actual, exp):
        content = Content()
        normaliser = Normaliser(content)
        ret_val = normaliser._get_stems(actual)
        assert ret_val == exp
        # Verify that we are using Content by reference!!
        assert normaliser.content == content

    @pytest.mark.parametrize(
        "actual,exp,stop_words",
        (
            (
                ["this", "is", "a", "sentence", "with", "stopwords", "."],
                ["sentence", "stopwords", "."],
                stopwords.words("english"),
            ),
            (
                ["this", "is", "a", "sentence", "with", "stopwords", "."],
                ["sentence", "stopwords"],
                None,
            ),
            (
                ["this", "is", "a", "sentence", "with", "stopwords", "."],
                ["sentence", "stopwords"],
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
                        "arthur",
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
                [["first", "sentence", "."], ["second", "sentence", "."]],
            ),
        ),
    )
    def test_tokenize(self, actual, exp):
        content = Content(original_content=actual)
        normaliser = Normaliser(content)
        normaliser._tokenize()
        for _id, _exp in enumerate(exp):
            assert content.sentences[_id].original_tokens == _exp
        # Verify that we are using Content by reference!!
        assert normaliser.content == content

    def test_normalise(self):
        actual = "Arthur didn't feel good at eight o'clock."
        exp_orig_tokens = [
            "arthur",
            "did",
            "n't",
            "feel",
            "good",
            "at",
            "eight",
            "o'clock",
            ".",
        ]
        exp_filtered_tokens = [
            "arthur",
            "feel",
            "good",
            "eight",
            "o'clock",
        ]

        content = Content(original_content=actual)
        normaliser = Normaliser(content)
        normaliser.normalise()
        assert content.sentences[0].original_tokens == exp_orig_tokens
        assert content.sentences[0].filtered_tokens == exp_filtered_tokens
        # Verify that we are using Content by reference!!
        assert normaliser.content == content
