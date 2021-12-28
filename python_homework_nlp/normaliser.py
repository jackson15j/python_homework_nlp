import logging
import string

from nltk import download
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from python_homework_nlp.common import Content
from python_homework_nlp.common import download_nltk_data

log = logging.getLogger(__name__)
# TODO: Move to `main()` and call before tests (`conftest.py` is not earlier
# enough due to import side-effects!!).
download_nltk_data()
STOPWORDS_EN = stopwords.words("english")
STOPWORDS_EN.extend(string.punctuation)
# TODO: strip additional stop words eg.
# i, 's, and, n't, us, ve, the, but
#
# TODO: fix stop words with lemmitisation (or output both types), due to root
# words like:
# countri, peopl, promis, chang


class Normaliser:
    """Class for NLP workflow."""

    content: Content

    def __init__(self, content: Content, stop_words: list = STOPWORDS_EN) -> None:
        self.content = content
        # See:
        # https://www.nltk.org/howto/stem.html#unit-tests-for-snowball-stemmer
        # Requires: `nltk.download("stopwords")`
        try:
            self.stemmer = SnowballStemmer("english", ignore_stopwords=True)
        except LookupError as e:
            log.debug("Stem exception: %r", e)
            download("stopwords")
            self.stemmer = SnowballStemmer("english", ignore_stopwords=True)

    def normalise(self):
        """Normaliser workflow to convert raw content to a nested list of
        filtered tokens. Workflow:

        1. Tokenize sentences/words.
        2. Filter out _"stop words"_.
        3. Stem words.
        """
        self._tokenize()
        _filtered_tokens = [
            self._get_tokens_without_stopwords(x)
            for x in self.content.original_tokens
        ]
        self.content.filtered_tokens = [
            self._get_stems(x) for x in _filtered_tokens
        ]

    def _tokenize(self) -> None:
        """Convert a block of text into a nested list of sentences and then a
        nested list of tokens.
        """
        # Requires: `nltk.download('punkt')`
        try:
            self.content.original_sentences = sent_tokenize(
                self.content.original_content
            )
        except LookupError as e:
            # TOOD: switch to upfront download/gathering of NLTK Data, to simplify
            # these functions. Call:
            # `python_homework_nlp.common.download_nltk_data` from `main()`.
            log.debug("Tokenize exception: %r", e)
            download("punkt")
            self.content.original_sentences = sent_tokenize(
                self.content.original_content
            )

        self.content.original_tokens = [
            word_tokenize(sentence)
            for sentence in self.content.original_sentences
        ]

    @staticmethod
    def _get_tokens_without_stopwords(
        tokens: list[str], stop_words: list[str] = STOPWORDS_EN
    ) -> list[str]:
        """Gets a new list of tokens with all stopwords removed."""
        return [x for x in tokens if x not in stop_words]

    def _get_stems(self, tokens: list[str]) -> list[str]:
        """Parses the string and returns a string with all of the _"stemmed"_
        versions of the words. Stemming is process of reducing words to their
        base/root/stem version. eg. fishing, fished, and fisher to the stem fish.
        """
        # TODO: Switch to Lemmatizing (eg. `nltk.stem.WorkNetLemmatizer`) if the
        # accuracy is poor and I'm okay with the time hit.
        return [self.stemmer.stem(x) for x in tokens]
