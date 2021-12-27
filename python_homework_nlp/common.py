import logging
from nltk import download

log = logging.getLogger(__name__)
REQ_NLTK_DATA = (
    "punkt",
    "stopwords",
)


def download_nltk_data() -> None:
    """Downloads all required NLTK data."""
    for x in REQ_NLTK_DATA:
        logging.debug("Downloading required NLTK data: %r", x)
        download(x)


class Content:
    """Container class for all transformations done against the text from a
    file.

    .. note::
        Suggest to use by Reference, so that the instance can be built up as it
        passes through the App code!!
    """

    _file_name: str = ""
    _original_content: str = ""
    _original_sentences: list[str] = []
    _original_tokens: list[list[str]] = []
    _filtered_tokens: list[list[str]] = []

    @property
    def file_name(self) -> str:
        return self._file_name

    @file_name.setter
    def file_name(self, value) -> None:
        self._file_name = value

    @property
    def original_content(self) -> str:
        return self._original_content

    @original_content.setter
    def original_content(self, value) -> None:
        self._original_content = value

    @property
    def original_sentences(self) -> list[str]:
        return self._original_sentences

    @original_sentences.setter
    def original_sentences(self, value) -> None:
        self._original_sentences = value

    @property
    def original_tokens(self) -> list[list[str]]:
        return self._original_tokens

    @original_tokens.setter
    def original_tokens(self, value) -> None:
        self._original_tokens = value

    @property
    def filtered_tokens(self) -> list[list[str]]:
        return self._filtered_tokens

    @filtered_tokens.setter
    def filtered_tokens(self, value) -> None:
        self._filtered_tokens = value
