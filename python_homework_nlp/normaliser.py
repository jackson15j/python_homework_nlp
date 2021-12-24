from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer


def tokenize(string: str) -> str:
    # Requires: `nltk.download('punkt')`
    # TODO: gracefully handle:
    #     raise LookupError(resource_not_found)
    #     LookupError:
    #     **********************************************************************
    #       Resource punkt not found.
    #       Please use the NLTK Downloader to obtain the resource:
    #
    #       >>> import nltk
    #       >>> nltk.download('punkt')
    #
    #       For more information see: https://www.nltk.org/data.html
    #
    #       Attempted to load tokenizers/punkt/PY3/english.pickle

    return word_tokenize(string)


def get_stems(string: str) -> list:
    """Parses the string and returns a string with all of the _"stemmed"_
    versions of the words. Stemming is process of reducing words to their
    base/root/stem version. eg. fishing, fished, and fisher to the stem fish.
    """
    # See: https://www.nltk.org/howto/stem.html#unit-tests-for-snowball-stemmer
    # Requires: `nltk.download("stopwords")`
    _tokens = tokenize(string)
    # TODO: Create `stemmer` once.
    stemmer = SnowballStemmer("english", ignore_stopwords=True)
    return [stemmer.stem(x) for x in _tokens]
