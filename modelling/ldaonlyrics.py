#!/usr/bin/env python
#coding: utf8

"""
Do some LDA on lyrics
"""
import sys, os
import logging

from gensim import corpora, models

from utils import cleanLyrics, englishOnly
from lyricsources import getLyricsFromJson, getLyricsFromElasticSearch

def filterFrequentWords(corpus, dictionary):
    """
    Filter out words that are too common and would appear everywhere
    """

    StopWords = 'the a have you my i been for that from in and no me they it as such but to of'.split() + \
        "we is your are with our it's on be".split()

    stopMapped = frozenset(dictionary.token2id[term] for term in StopWords)

    newCorpus = []
    for lyric in corpus:
        newLyrics = [(word[0], word[1]) for word in lyric if word[0] not in stopMapped]
        if newLyrics:
            newCorpus.append(newLyrics)

    return newCorpus



def main(args):

    from argparse import ArgumentParser
    from simplelogsetter import SimpleLogSetter
    
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", dest="verbosity", default=0, action="count",
                      help="Verbosity.  Invoke many times for higher verbosity")
    parser.add_argument("-c", "--corpus", dest="corpus", required=True,
                      help="Corpus file to save to/load from")
    parser.add_argument("-d", "--dictionary", dest="dictionary", required=True,
                      help="Dictionary file to save to/load from")
    parser.add_argument("-m", "--model", dest="model", required=True,
                      help="Model file to save to/load from")
    parser.add_argument("-t", "--topics", dest="topics", required=True, type=int,
                      help="Number of topics")
    parser.add_argument("-p", "--passes", dest="passes", type=int, default=1,
                      help="How many passes of the data (default: %(default)s)")    
    parser.add_argument("-e", "--english-only", dest="filterEnglishOnly", default=False, action="store_true",
                      help="Filter corpus and only let through english lyrics")
    parser.add_argument("--save-filtered", dest="filteredCorpus", default=None,
                      help="Save the filtered corpus to this filename")
    parser.add_argument("-s", "--filter-stop", dest="filterStopWords", default=False, action="store_true",
                      help="Filter stop words before modelling (only implemented for english at the moment)")
    parser.add_argument("--elastic-search", dest="elasticSearch", default=False, action="store_true",
                      help="Get data from elastic search instead of a file")
    parser.add_argument("lyrics", nargs="?",
                      help="File to load lyrics from")



    parameters = parser.parse_args(args)


    logger = SimpleLogSetter(verbosity=parameters.verbosity)
    logger.startLogging()

    dictionaryPath = os.path.expanduser(parameters.dictionary)
    if os.path.exists(dictionaryPath):
        logging.info("Loading dictionary from %s" % dictionaryPath)
        dictionary = corpora.Dictionary.load(dictionaryPath)
        allowUpdate = False
    else:
        dictionary = corpora.Dictionary()
        allowUpdate = True

    corpusPath = os.path.expanduser(parameters.corpus)
    if len(dictionary) > 0 and os.path.exists(corpusPath):
        logging.info("Loading corpus from %s" % corpusPath)
        allLyrics = corpora.MmCorpus(corpusPath)
    else:

        if parameters.elasticSearch:
            lyricsGenerator = getLyricsFromElasticSearch()
        else:
            lyricsGenerator = getLyricsFromJson(os.path.expanduser(parameters.lyrics))

        allLyrics = []
        for songLyrics in lyricsGenerator:
            allLyrics.append(dictionary.doc2bow(cleanLyrics(songLyrics), allow_update=allowUpdate))

        corpora.MmCorpus.serialize(corpusPath, allLyrics)

        if allowUpdate:
            logging.info("Saving dictionary to %s" % dictionaryPath)
            dictionary.save(dictionaryPath)


    if parameters.filterEnglishOnly:
        logging.info("Filtering for english only")
        allLyrics = englishOnly(allLyrics, dictionary)

        if parameters.filteredCorpus:
            corpora.MmCorpus.serialize(os.path.expanduser(parameters.filteredCorpus), allLyrics)

    if parameters.filterStopWords:
        logging.info("Filtering out stop words")
        allLyrics = filterFrequentWords(allLyrics, dictionary)

    model = models.ldamodel.LdaModel(corpus=allLyrics, id2word=dictionary, num_topics=parameters.topics, 
                                     passes=parameters.passes)
    model.save(os.path.expanduser(parameters.model))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
