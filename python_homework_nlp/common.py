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
