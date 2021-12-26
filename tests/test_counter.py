import pytest
from python_homework_nlp.counter import counter


class TestCounter:
    @pytest.mark.parametrize(
        "actual,exp,most_common",
        (
            (
                {
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
                },
                {
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
                },
                None,
            ),
            (
                {
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
                },
                {
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
                },
                1,
            ),
        ),
    )
    def test_counter(self, actual, exp, most_common):
        assert counter(actual, most_common) == exp
