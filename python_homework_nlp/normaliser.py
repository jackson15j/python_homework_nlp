import logging

from nltk import download
from nltk import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer

log = logging.getLogger(__name__)


def tokenize(string: str) -> list:
    # Requires: `nltk.download('punkt')`
    try:
        sentences = sent_tokenize(string)
    except LookupError as e:
        # TOOD: switch to upfront download/gathering of NLTK Data, to simplify
        # these functions.
        log.debug("Tokenize exception: %r", e)
        download("punkt")
        sentences = sent_tokenize(string)

    return [word_tokenize(sentence) for sentence in sentences]


def get_stems(tokens: list) -> list:
    """Parses the string and returns a string with all of the _"stemmed"_
    versions of the words. Stemming is process of reducing words to their
    base/root/stem version. eg. fishing, fished, and fisher to the stem fish.
    """
    # See: https://www.nltk.org/howto/stem.html#unit-tests-for-snowball-stemmer
    # Requires: `nltk.download("stopwords")`
    # TODO: Create `stemmer` once.
    try:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
    except LookupError as e:
        log.debug("Stem exception: %r", e)
        download("stopwords")
        stemmer = SnowballStemmer("english", ignore_stopwords=True)

    return [stemmer.stem(x) for x in tokens]
