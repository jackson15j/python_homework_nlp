import pytest
from argparse import Namespace
from pathlib import Path
from python_homework_nlp.common import Content
from python_homework_nlp.file_reader import get_folder_contents
from python_homework_nlp.main import workflow


@pytest.fixture
def get_test_docs():
    content_objs = get_folder_contents(Path("test_docs/"))
    return content_objs


class TestMain:
    def test_workflow(self):
        exp_content = "Some made up words to test with."
        exp_dict = {
            "made": {
                "count": 1,
                "files": ["file1"],
                "matches": ["Some made up words to test with."],
            },
            "test": {
                "count": 1,
                "files": ["file1"],
                "matches": ["Some made up words to test with."],
            },
            "word": {
                "count": 1,
                "files": ["file1"],
                "matches": ["Some made up words to test with."],
            },
        }

        args = Namespace(num_most_common_words=None)
        content = Content(file_name="file1", original_content=exp_content)
        ret_val = workflow([content], args)
        assert ret_val == exp_dict

    def test_workflow_with_real_docs(self, get_test_docs):
        args = Namespace(num_most_common_words=None)
        ret_val = workflow(get_test_docs, args)
        assert ret_val != {}
