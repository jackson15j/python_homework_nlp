import pytest
from python_homework_nlp.common import Content, Sentence
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
                        "original_tokens": [
                            ["first", "sentence", "."],
                            ["second", "is", "sentence", "."],
                            ["final", "sentence", "!"],
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
                        "original_tokens": [
                            ["first", "sentence", "."],
                            ["second", "is", "sentence", "."],
                            ["final", "sentence", "!"],
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
        _sentence_objs = []
        for _id in range(len(actual["file1"]["original_sentences"])):
            _sentence = Sentence(
                file_name=file_name,
                original_sentence=actual["file1"]["original_sentences"][_id],
                original_tokens=actual["file1"]["original_tokens"][_id],
            )
            _sentence.filtered_tokens = actual["file1"]["filtered_tokens"][_id]
            _sentence_objs.append(_sentence)

        content = Content(
            file_name=file_name,
            sentences=_sentence_objs,
        )
        content.update_collections_counters()
        counter = Counter([content])
        assert counter.counter(most_common) == exp
