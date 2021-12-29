import string

from nltk import download
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from python_homework_nlp.common import (
    configure_logging,
    Content,
    download_nltk_data,
    Sentence,
)

log = configure_logging(__name__)
# FIXME: Move to `main()` and call before tests (`conftest.py` is not earlier
# enough due to import side-effects!!).
download_nltk_data()
# Manual list of Stemming overrides to clean up the noisy output. Ideally, I
# should either try one of the many other NLTK Stemming options, or move over
# to Lemmatization instead.
STEMMING_OVERRIDES = (
    "I",
    "'s",
    "And",
    "n't",
    "us",
    "ve",
    "The",
    "But",
    "It",
    "in",
    "ll",
    "'re",
    "'",
    "''",
    "``",
    "'d",
    "'m",
    "a",
)
STOPWORDS_EN = stopwords.words("english")
STOPWORDS_EN.extend(string.punctuation)
STOPWORDS_EN.extend(STEMMING_OVERRIDES)
# BUG: fix stop words with lemmitisation (or output both types), due to root
# words like:
# countri, peopl, promis, chang
#
# Mentioned this in the Retrospective section in the `README.md` in more
# detail.


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
        for sentence in self.content.sentences:
            _filtered_tokens = self._get_tokens_without_stopwords(
                sentence.original_tokens
            )
            sentence.filtered_tokens = self._get_stems(_filtered_tokens)
        self.content.update_collections_counters()

    def _tokenize(self) -> None:
        """Convert a block of text into a nested list of sentences and then a
        nested list of tokens.
        """
        # Requires: `nltk.download('punkt')`
        _sentences = []
        try:
            _sentences = sent_tokenize(self.content.original_content)
        except LookupError as e:
            # TOOD: switch to upfront download/gathering of NLTK Data, to simplify
            # these functions. Call:
            # `python_homework_nlp.common.download_nltk_data` from `main()`.
            log.debug("Tokenize exception: %r", e)
            download("punkt")
            _sentences = sent_tokenize(self.content.original_content)

        _sentence_objs: list[Sentence] = []
        for sentence in _sentences:
            _word_tokens = word_tokenize(sentence)
            _word_tokens = [x.lower() for x in _word_tokens]
            _sentence_objs.append(
                Sentence(
                    file_name=self.content.file_name,
                    original_sentence=sentence,
                    original_tokens=_word_tokens,
                )
            )
        self.content.sentences = _sentence_objs

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
