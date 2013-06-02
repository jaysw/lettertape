def cleanWord(word):
    Punctuation = frozenset('.,:;"\'!')
    if word[0] in Punctuation:
        word = word[1:]

    if len(word) > 0 and word[-1] in Punctuation:
        word = word[:-1]

    return word


def cleanLyrics(lyrics):
    words = lyrics.lower().split()

    words = [cleanWord(word) for word in words]
    words = [word for word in words if len(word) > 0]

    return words


def englishOnly(corpus, dictionary):
    NecessaryTerms = ['the']
    IncompatibleTerms = 'ich la da dem'.split()
    StopWords = 'the a have you my i been for that from in and no me they it as such but to of'.split()

    necessaryMapped = frozenset(dictionary.token2id[term] for term in NecessaryTerms)
    incompatibleMapped = frozenset(dictionary.token2id[term] for term in IncompatibleTerms)
    stopMapped = frozenset(dictionary.token2id[term] for term in StopWords)

    newCorpus = []
    for lyric in corpus:
        if not any(word[0] in necessaryMapped for word in lyric):
            continue
        if any(word[0] in incompatibleMapped for word in lyric):
            continue

        newCorpus.append(lyric)

    return newCorpus


