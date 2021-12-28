import pytest
from python_homework_nlp.common import configure_logging, download_nltk_data


@pytest.fixture(autouse=True, scope="session")
def configure_logs():
    configure_logging()


@pytest.fixture(autouse=True, scope="session")
def download_required_nltk_data():
    # FIXME: call before tests (`conftest.py` is not earlier enough due to
    # import side-effects!!).
    download_nltk_data()
