#!/usr/bin/env python
#coding: utf8

"""
Apply LDA model to lyrics
"""
import sys, os
import logging

import simplejson
from gensim import corpora, models
import pyes

from utils import cleanLyrics, englishOnly, isItEnglish

def getLyrics(filename):
    logging.info("Loading lyrics from %s" % filename)
    fin = open(filename)
    for line in fin:
        lyrics = simplejson.loads(line)
        yield lyrics
    fin.close()


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
    parser.add_argument("-e", "--english-only", dest="filterEnglishOnly", default=False, action="store_true",
                      help="Filter corpus and only let through english lyrics")
    parser.add_argument("-i", "--index-name", dest="indexName", required=True,
                      help="Index name to use in elastic search")
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

    connection = pyes.ES()

    lyricsGenerator = getLyrics(os.path.expanduser(parameters.lyrics))

    for index, song in enumerate(lyricsGenerator):
        lyrics = song['lyrics']
        frequencied = dictionary.doc2bow(cleanLyrics(lyrics), allow_update=False)
        if not parameters.filterEnglishOnly or isItEnglish(frequencied, dictionary):
            distribution = model[frequencied]
            topics = {}
            for topic, probability in distribution:
                topics['topic%s' % topic] = probability
            song['model'] = topics

            connection.index(simplejson.dumps(song), parameters.indexName, 'song')

        if index % 1000 == 0:
            logging.debug("Processed %s" % index)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
