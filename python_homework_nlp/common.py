"""Common static low-level functions."""
import collections
import logging
import logging.config
import time
from dataclasses import dataclass, field
from functools import partial, wraps
from pathlib import Path
from typing import Union

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


def configure_logging(logger_name: Union[str, None] = None):
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


@dataclass
class Sentence:
    file_name: str
    original_sentence: str
    original_tokens: list[str]
    filtered_tokens: list[str] = field(init=False)


@dataclass
class Content:
    """Container class for all transformations done against the text from a
    file.

    .. note::
        Suggest to use by Reference, so that the instance can be built up as it
        passes through the App code!!
    """

    file_name: str = ""
    original_content: str = ""
    sentences: list[Sentence] = field(default_factory=list)
    filtered_collections_counters: list[collections.Counter] = field(
        default_factory=list, init=False, repr=False
    )
    filtered_collections_counter_total: collections.Counter = field(
        default_factory=collections.Counter, init=False, repr=False
    )

    def update_collections_counters(self):
        self.filtered_collections_counters = [
            collections.Counter(x.filtered_tokens) for x in self.sentences
        ]
        self.filtered_collections_counter_total = sum_collection_counters(
            self.filtered_collections_counters
        )
