import pytest
from python_homework_nlp.common import Content
from python_homework_nlp.counter import Counter


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
        file_name = "file1"
        content = Content(
            file_name=file_name,
            original_sentences=actual[file_name]["original_sentences"],
        )
        content.filtered_tokens = actual[content.file_name]["filtered_tokens"]
        counter = Counter([content])
        assert counter.counter(most_common) == exp
