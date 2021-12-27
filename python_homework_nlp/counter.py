import collections
from python_homework_nlp.common import Content


class Counter:
    """Class for counting/discovery of most used words + files & original
    sentences.
    """

    content_objs: list[Content]

    def __init__(self, content_objs: list[Content]) -> None:
        self.content_objs = content_objs

    @staticmethod
    def _sum_collection_counters(
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

    def _get_matches(self, word: str) -> dict:
        """Returns all files + sentences that match a given word.

        :param str word: word to find matches for.
        :returns: dict of: {"matches": <list>, "files": <list>}
        """
        # TOOD: test
        _matched_files = []
        _matched_sentences = []
        for content in self.content_objs:
            _matches = Counter._get_matches_by_word(
                word, content.original_sentences
            )
            if _matches:
                _matched_files.append(content.file_name)
                _matched_sentences.extend(_matches)

        # TODO: Update `Content` to have these fields, or move out to `Renderer`??
        return {"matches": _matched_sentences, "files": _matched_files}

    @staticmethod
    def _get_matches_by_word(word: str, original_sentences: list[str]) -> list:
        """Returns all sentences that match a given word.

        :param str word: word to find matches for.
        :param list orig_sentences: List of sentences to find matches in.
        :returns: list of matched sentences.
        """
        # TOOD: test
        return [x for x in original_sentences if word in x.lower()]

    def counter(self, most_common: int = None) -> dict:
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
        # TODO: separate counter logic from result dict generation ??
        # TODO: reduce the number of loops to generate the `ret_dict`!!
        ret_dict = {}

        _total_counter = Counter._sum_collection_counters(
            [x.filtered_collections_counter_total for x in self.content_objs]
        )
        ret_dict = {
            k: {"count": v} for k, v in _total_counter.most_common(most_common)
        }
        for _word in ret_dict.keys():
            ret_dict[_word].update(self._get_matches(_word))
        return ret_dict
