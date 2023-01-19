"""2-Pass counter to return filtered tokens of counts + file/sentence mappings.
"""
from typing import Union
from typing_extensions import TypedDict
from python_homework_nlp.common import Content, sum_collection_counters, Sentence


class MatchData(TypedDict):
    count: int
    matches: list[str]
    files: list[str]


class Counter:
    """Class for counting/discovery of most used words + files & original
    sentences.
    """

    content_objs: list[Content]

    def __init__(self, content_objs: list[Content]) -> None:
        self.content_objs = content_objs

    def _get_matches(self, word: str) -> tuple[list[str], list[str]]:
        """Returns all files + sentences that match a given word.

        :param str word: word to find matches for.
        :returns: tuple of: ([<matched_sentences>], [<files>])
        """
        _matched_files = []
        _matched_sentences = []
        for content in self.content_objs:
            _matches = Counter._get_matches_by_word(word, content.sentences)
            if _matches:
                _matched_files.append(content.file_name)
                _matched_sentences.extend(_matches)

        return (_matched_sentences, _matched_files)

    @staticmethod
    def _get_matches_by_word(word: str, sentences: list[Sentence]) -> list:
        """Returns all sentences that match a given word.

        :param str word: word to find matches for.
        :param list orig_sentences: List of sentences to find matches in.
        :returns: list of matched sentences.
        """
        # Match up original_sentences with filtered/original_tokens, so
        # that I can match on the filtered tokens, but return the
        # original_sentence. Reduce false positives from doing an `in` check !!
        return [
            x.original_sentence for x in sentences if word in x.filtered_tokens
        ]

    def counter(
        self, most_common: Union[int, None] = None
    ) -> dict[str, MatchData]:
        """Counts number of words duplicate words in a filtered tokens list +
        generates the return structure.

        :param int most_common: Returns X most common words. Returns all if None.
        :returns: dict of:
        {<word>: {"count": <int>, "matches": [<str>,], "files": [<str>,]}}
        Where:
        * `count` = number of matches.
        * `matches` = list of matched sentences.
        * `files` = list of filenames with matched sentences.
        """
        ret_dict = {}

        [x.update_collections_counters() for x in self.content_objs]
        _total_counter = sum_collection_counters(
            [x.filtered_collections_counter_total for x in self.content_objs]
        )
        for _word, _count in _total_counter.most_common(most_common):
            _matches, _files = self._get_matches(_word)
            _match_data: MatchData = {
                "count": _count,
                "matches": _matches,
                "files": _files,
            }
            ret_dict[_word] = _match_data
        return ret_dict
