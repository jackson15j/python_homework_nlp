import collections
import pytest
from python_homework_nlp.common import Content, Sentence


class TestCommon:
    @pytest.mark.parametrize(
        "method,exp",
        (
            ("file_name", ""),
            ("original_content", ""),
            ("_sentences", []),
            ("filtered_collections_counters", []),
            ("filtered_collections_counter_total", collections.Counter()),
        ),
    )
    def test_content__unset(self, method, exp):
        content = Content()
        content_method = getattr(content, method)
        assert content_method == exp

    def test_filterd_collections_counters(self):
        _tokens = [["a", "b", "a"], ["a", "c"]]
        _sentences = []
        for _token in _tokens:
            _sentence = Sentence("", "", [])
            _sentence.filtered_tokens = _token
            _sentences.append(_sentence)
        exp_fcc = [collections.Counter(x) for x in _tokens]
        exp_fct = collections.Counter(["a", "b", "a", "a", "c"])
        content = Content(sentences=_sentences)
        content.update_collections_counters()
        for _id, x in enumerate(_tokens):
            assert content.sentences[_id].filtered_tokens == x
        assert content.filtered_collections_counters == exp_fcc
        assert content.filtered_collections_counter_total == exp_fct
