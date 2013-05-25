import random
import config
from database import DatabaseManager
from recommender import KeywordRecommender
from bottle import Bottle, run, request, view, static_file

class get_dbm(object):
    def __enter__(self):
        self.dbm = DatabaseManager(config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME)
        return self.dbm

    def __exit__(self, type, value, traceback):
        self.dbm.close()

# Real business begins
app = Bottle()

# Serve static files
STATIC_DIRECTORY = './demo-static'
@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=STATIC_DIRECTORY)

@app.route('/')
@view('home')
def home():
    with get_dbm() as dbm:
        group = random.randint(1, 10)
        query = 'SELECT query FROM query WHERE group_id = %d ORDER BY RAND() LIMIT 10' % group
        queries = [row['query'] for row in dbm.get_rows(query)]

        # source hot_cache.sql to make things go smoothly
        hot_product_query = 'SELECT product FROM hot_cache ORDER BY weight DESC LIMIT 5'
        products = transfrom_results(row['product'] for row in dbm.get_rows(hot_product_query))

    if not queries:
        print 'No quries selected', group

    return {
        'queries': queries,
        'products': products,
    }

@app.post('/update')
@view('recommendations')
def update_suggestions():
    query = request.POST.query
    with get_dbm() as dbm:
        recommender = KeywordRecommender(config.N, dbm, config.WordSegmenter(), None)
        products = transfrom_results(rec[0] for rec in recommender.recommend(query))
    return {'products': products}

def get_image_url(p):
    # we only have 5 images...
    i = abs(p.__hash__()) % 5 + 1
    return '/static/images/glasses%d.jpg' % i

def transfrom_results(products):
    return [(p, get_image_url(p)) for p in products]

run(app, host='localhost', port=8080, debug=True)
