#!/usr/bin/env python
#coding: utf8

"""
Apply LDA model to lyrics
"""
import sys, os
import logging

from gensim import corpora, models

from utils import cleanLyrics, englishOnly
from lyricsources import getLyricsFromJson, getLyricsFromElasticSearch

def main(args):

    from argparse import ArgumentParser
    from simplelogsetter import SimpleLogSetter
    
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", dest="verbosity", default=0, action="count",
                      help="Verbosity.  Invoke many times for higher verbosity")
    parser.add_argument("-d", "--dictionary", dest="dictionary", required=True,
                      help="Dictionary file")
    parser.add_argument("-m", "--model", dest="model", required=True,
                      help="Model file")
    parser.add_argument("-s", "--show-examples", dest="showExamples", type=int, default=None,
                      help="Show n examples that rank high in each topic")
    parser.add_argument("-e", "--english-only", dest="filterEnglishOnly", default=False, action="store_true",
                      help="Filter corpus and only let through english lyrics")
    parser.add_argument("--elastic-search", dest="elasticSearch", default=False, action="store_true",
                      help="Get data from elastic search instead of a file")
    parser.add_argument("lyrics", nargs="?",
                      help="File to load lyrics from")


    parameters = parser.parse_args(args)
    logger = SimpleLogSetter(verbosity=parameters.verbosity)
    logger.startLogging()

    dictionaryPath = os.path.expanduser(parameters.dictionary)
    logging.info("Loading dictionary from %s" % dictionaryPath)
    dictionary = corpora.Dictionary.load(dictionaryPath)

    modelPath = os.path.expanduser(parameters.model)
    logging.info("Loading model from %s" % modelPath)
    model = models.ldamodel.LdaModel.load(modelPath)

    if parameters.elasticSearch:
        lyricsGenerator = getLyricsFromElasticSearch()
    else:
        lyricsGenerator = getLyricsFromJson(os.path.expanduser(parameters.lyrics))

    allLyrics = []
    rawLyrics = []
    for index, songLyrics in enumerate(lyricsGenerator):
        allLyrics.append(dictionary.doc2bow(cleanLyrics(songLyrics), allow_update=False))
        rawLyrics.append(songLyrics)
        if index > 10:
            break

    if parameters.filterEnglishOnly:
        logging.info("Filtering for english only")
        allLyrics = englishOnly(allLyrics, dictionary)


    logging.info("Calculating distributions")
    for index, lyric in enumerate(allLyrics[:10]):
        distribution = model[lyric]
        print distribution
        print rawLyrics[index]

    lyricRatings = {}
    




    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
