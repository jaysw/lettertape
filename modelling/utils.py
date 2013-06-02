def cleanWord(word):
    """
    Get rid of leading or trailing punctuation
    """
    Punctuation = frozenset('.,:;"\'!')
    if word[0] in Punctuation:
        word = word[1:]

    if len(word) > 0 and word[-1] in Punctuation:
        word = word[:-1]

    return word


def cleanLyrics(lyrics):
    """
    normalise words
    """
    words = lyrics.lower().split()

    words = [cleanWord(word) for word in words]
    words = [word for word in words if len(word) > 0]

    return words


def isItEnglish(lyric, dictionary):
    NecessaryTerms = ['the']
    IncompatibleTerms = 'ich la da dem'.split()

    necessaryMapped = frozenset(dictionary.token2id[term] for term in NecessaryTerms)
    incompatibleMapped = frozenset(dictionary.token2id[term] for term in IncompatibleTerms)

    if not any(word[0] in necessaryMapped for word in lyric):
        return False

    if any(word[0] in incompatibleMapped for word in lyric):
        return False

    return True


def englishOnly(corpus, dictionary):
    return [lyric for lyric in corpus if isItEnglish(lyric, dictionary)]
