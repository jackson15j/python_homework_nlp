from collections import Counter


def _get_word_counts(tokens: list) -> Counter:
    return Counter(tokens)


def _sum_collection_counters(counters: list) -> Counter:
    total_counter: Counter = Counter()
    for x in counters:
        total_counter += x
    return total_counter


def _get_matches(word: str, orig: dict) -> dict:
    """Returns all files + sentences that match a given word.

    :param str word: word to find matches for.
    :param dict orig: Original nested dictionary of files and original sentences
    + filtered tokens.
    {<filename>: {"original_sentences": [<str>,], "filtered_tokens": [[<str>,],]}}
    :returns: dict of: {"matches": <list>, "files": <list>}
    """
    # TOOD: test
    _matched_files = []
    _matched_sentences = []
    for _file in orig:
        _matches = _get_matches_by_word(word, orig[_file]["original_sentences"])
        if _matches:
            _matched_files.append(_file)
            _matched_sentences.extend(_matches)

    return {"matches": _matched_sentences, "files": _matched_files}


def _get_matches_by_word(word: str, original_sentences: list) -> list:
    """Returns all sentences that match a given word.

    :param str word: word to find matches for.
    :param list orig_sentences: List of sentences to find matches in.
    :returns: list of matched sentences.
    """
    # TOOD: test
    return [x for x in original_sentences if word in x.lower()]


def counter(orig: dict, most_common: int = None) -> dict:
    """Counts number of words duplicate words in a filtered tokens list +
    generates the return structure.

    :param dict orig: Original nested dictionary of files and original sentences
    + filtered tokens.
    {<filename>: {"original_sentences": [<str>,], "filtered_tokens": [[<str>,],]}}
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
    _counters = [
        _get_word_counts(x) for k, v in orig.items() for x in v["filtered_tokens"]
    ]
    _total_counter = _sum_collection_counters(_counters)
    ret_dict = {
        k: {"count": v} for k, v in _total_counter.most_common(most_common)
    }
    for _word in ret_dict.keys():
        ret_dict[_word].update(_get_matches(_word, orig))
    return ret_dict
