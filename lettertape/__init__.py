import pyes as es
from flask import Flask, session, g, render_template, request

app = Flask(__name__)
app.config.from_pyfile('../websiteconfig.py')

MAX_RESULTS = 500

def prepare_hits(hits):
    for hit in hits:
        if hit._meta.highlight and hit._meta.highlight.get('lyrics'):
            highlights = hit._meta.highlight['lyrics']
        yield dict(title=hit.title,
                   artist=hit.artist,
                   highlights=highlights,
                   wikia_url=hit.url)


@app.route("/", methods='GET POST'.split())
def index():
    """The home page"""
    conn = es.ES(app.config['ELASTICSEARCH_HOST'])
    hits = []
    total = 0
    searching = False
    q = 'Lettertape'
    if request.method == 'POST' and request.form.get('q'):
        q = request.form['q']
        h = es.HighLighter(['<span class="lyric-summary-highlight">'], ['</span>'])
        query = es.TermsQuery()
        query.add('lyrics', q.lower().split())
        s = es.Search(query, highlight=h, size=MAX_RESULTS)
        s.add_highlight('lyrics')
        hits = conn.search(s)
        total = hits.total
        hits = prepare_hits(hits)
    return render_template('index.html', hits=hits,
                           searching=searching, q=q, quotedq=q.replace("'","\\'"), total=total)
