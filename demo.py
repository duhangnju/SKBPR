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

    if not queries:
        print 'No quries selected', group

    return {'queries': queries}

@app.post('/update')
@view('recommendations')
def update_suggestions():
    query = request.POST.query
    with get_dbm() as dbm:
        recommender = KeywordRecommender(config.N, dbm, config.WordSegmenter(), None)
        recommendations = recommender.recommend(query)
    return {'recommendations': recommendations}

run(app, host='localhost', port=8080, debug=True)
