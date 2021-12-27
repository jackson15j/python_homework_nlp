import collections
import pytest
from python_homework_nlp.common import Content


class TestCommon:
    @pytest.mark.parametrize(
        "method,exp",
        (
            ("file_name", ""),
            ("original_content", ""),
            ("original_sentences", []),
            ("original_tokens", []),
            ("filtered_tokens", []),
            ("filtered_collections_counters", []),
        ),
    )
    def test_content__unset(self, method, exp):
        content = Content()
        content_method = getattr(content, method)
        assert content_method == exp

    def test_filterd_collections_counters(self):
        _tokens = [["a", "b", "a"], ["a", "c"]]
        exp = [collections.Counter(x) for x in _tokens]
        content = Content()
        content.filtered_tokens = _tokens
        assert content.filtered_tokens == _tokens
        assert content.filtered_collections_counters == exp
