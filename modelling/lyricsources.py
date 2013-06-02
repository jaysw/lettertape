import logging 

def getLyricsFromElasticSearch():
    import pyes

    logging.info("Loading lyrics from elastic search")
    elastic = pyes.ES()
    query = pyes.WildcardQuery(field='lyrics', value='*')
    count = elastic.count(query)

    results = elastic.search(query, size=count['count'] + 1)
    for result in results:
        yield result['lyrics']


def getLyricsFromJson(filename):
    import simplejson

    logging.info("Loading lyrics from %s" % filename)
    fin = open(filename)
    for line in fin:
        lyrics = simplejson.loads(line)
        yield lyrics['lyrics']
    fin.close()

