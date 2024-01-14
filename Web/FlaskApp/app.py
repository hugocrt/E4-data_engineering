from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from ..Elasticsearch_utils.elasticsearch_operations import *


app = Flask(__name__)


def connect_to_mongodb(flaskapp=app):
    try:
        flaskapp.config['MONGO_URI'] = 'mongodb://localhost:27017/senscritique'
        mongo = PyMongo(flaskapp)
        collection = mongo.db.movies
        return collection

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


def retrieve_mongo_data(collection):
    projection = {'_id': 0}
    return list(collection.find({}, projection))


def create_index(documents):
    bulk(es, generate_data(documents))


def search_movies(index_name, query, page_size, page=1):
    if query:
        body_query = {"wildcard": {"title": {"value": f"*{query}*"}}}
    else:
        body_query = {"match_all": {}}
    from_value = (page - 1) * page_size
    result = es.search(index=index_name,
                       body={"query": body_query, "from": from_value, "size": page_size})
    hits = result['hits']['hits']
    total_hits = result['hits']['total']['value']
    info = (f"{total_hits} film{'s' if total_hits > 1 else ''} correspondant à votre recherche \
    '{query}\' (~{result['took']}ms)")
    return hits, total_hits, info


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/db', methods=['GET'])
def database_page():
    page = request.args.get('page', default=1, type=int)
    page_size = 5

    search_query = request.args.get('search_query', default='', type=str)

    hits, total_hits, info = search_movies('movies',
                                           search_query,
                                           page_size=page_size,
                                           page=page)

    movie_data_list = [{key: value for key, value in hit['_source'].items()} for hit in hits]

    params = {
        'res': movie_data_list,
        'search_info': info,
        'page': page,
        'page_size': page_size,
        'total_hits': total_hits
    }

    return render_template('db.html', **params)


@app.route('/map')
def map_page():
    return render_template('map.html')


@app.route('/analysis')
def analysis_page():
    return render_template('analysis.html')
