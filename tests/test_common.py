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
        ),
    )
    def test_content__unset(self, method, exp):
        content = Content()
        content_method = getattr(content, method)
        assert content_method == exp
