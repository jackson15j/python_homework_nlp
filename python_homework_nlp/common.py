import collections
import logging
import logging.config
import time
from functools import partial, wraps
from pathlib import Path
from nltk import download

LOG_DIR = Path("logs/")
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "class": "logging.Formatter",
            "format": ("%(asctime)s %(name)-15s %(levelname)-8s %(message)s"),
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "app.log",
            "mode": "a",
            "formatter": "detailed",
        },
    },
    "loggers": {
        "__main__": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": True,
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}

log = logging.getLogger(__name__)
REQ_NLTK_DATA = (
    "punkt",
    "stopwords",
)


def configure_logging(logger_name: str = None):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger(logger_name) if logger_name else logging.getLogger()


def timer(func=None):
    """Decorator to report the time it takes to run a function.

    .. note::
        For more detail, replace with `cProfile` and pass CLI arg to disable.
        See: https://docs.python.org/3.6/library/profile.html.

    :param func: function to execute.
    """
    if func is None:
        return partial(timer)

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        total = time.time() - start
        log.debug("%r took: %ssecs", func, total)
        return result

    return wrapper


def download_nltk_data() -> None:
    """Downloads all required NLTK data."""
    for x in REQ_NLTK_DATA:
        logging.debug("Downloading required NLTK data: %r", x)
        download(x)


def sum_collection_counters(
    counters: list[collections.Counter],
) -> collections.Counter:
    """Collect together each sentence-level `collections.Counter` instance,
    so that we can return a singular (file-level) `collections.Counter`
    instance.
    """
    total_counter: collections.Counter = collections.Counter()
    for x in counters:
        total_counter += x
    return total_counter


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
    _filtered_collections_counters: list[collections.Counter] = []
    _filtered_collections_counter_total: collections.Counter = (
        collections.Counter()
    )

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
        self._filtered_collections_counters = [
            collections.Counter(x) for x in value
        ]
        self._filtered_collections_counter_total = sum_collection_counters(
            self._filtered_collections_counters
        )

    @property
    def filtered_collections_counters(self) -> list[collections.Counter]:
        """A list of `collections.Counter` instances with all words and their
        respective totals for the `filtered__tokens`.
        ie. a Counter for each sentence of tokens.
        """
        return self._filtered_collections_counters

    @property
    def filtered_collections_counter_total(self) -> collections.Counter:
        """A `collections.Counter` instance that totals all words and their
        respective totals for the `filtered__tokens`.
        ie. a Counter for all tokens in the file.
        """
        return self._filtered_collections_counter_total
