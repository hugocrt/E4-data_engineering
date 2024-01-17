from unidecode import unidecode
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from ..Elasticsearch_utils.elasticsearch_operations import *


def connect_to_mongodb(flaskapp):
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


def retrieve_unique_fields(collection):
    # Get a sample document to determine the keys (fields)
    sample_document = collection.find_one({})

    # Exclude fields from the sample document that you want to ignore
    excluded_fields = {'title', 'poster', 'ranking', '_id'}
    fields_to_check = [field for field in sample_document if field not in excluded_fields]

    # Get distinct values for each field
    unique_fields = {field: collection.distinct(field) for field in fields_to_check}

    unique_data_list = [
        {
            'Réalisateurs' if field == 'director' else (
                'Genres' if field == 'genres' else (
                    'Pays de production' if field == 'native_countries' else field)
            ): (
                sorted(
                    [value for value in values if value is not None],
                    key=lambda x: unidecode(x) if not isinstance(x, int) else x
                )
            )
        }
        for field, values in unique_fields.items()
        if values is not None
    ]

    native_countries_data = next((item for item in unique_data_list if 'Pays de production' in item),
                                 None)
    if native_countries_data:
        unique_data_list.remove(native_countries_data)
        unique_data_list.insert(2, native_countries_data)

    return unique_data_list


def launch_es(es_client, collection):
    # if es_client.indices.exists(index='movies'):
    #     # Delete the index
    #     es_client.indices.delete(index='movies')
    #     return
    clear_es_client(es_client)
    data = retrieve_mongo_data(collection)
    create_index(es_client, data)


app = Flask(__name__)
collection = connect_to_mongodb(app)
unique_fields = retrieve_unique_fields(collection)
print(unique_fields)

launch_es(es, collection)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/db', methods=['GET'])
def database_page():
    title_request = request.args.get('title_query', default='', type=str)
    native_countries_request = request.args.getlist('Pays de production')
    min_duration_request = request.args.get('min_duration', type=str)
    max_duration_request = request.args.get('max_duration', type=str)
    directors_request = request.args.getlist('Réalisateurs')
    genres_request = request.args.getlist('Genres')
    min_year_request = request.args.get('min_year', type=str)
    max_year_request = request.args.get('max_year', type=str)
    sort_order_request = request.args.get('sort_order', default='asc', type=str)
    page_request = request.args.get('page', default=1, type=int)

    page_size = 30

    search_params = {
        'title_query': title_request,
        'page_size': page_size,
        'page': page_request,
        'min_year': min_year_request,
        'max_year': max_year_request,
        'sort_order': sort_order_request,
        'directors': directors_request,
        'genres': genres_request,
        'native_countries': native_countries_request,
        'min_duration': min_duration_request,
        'max_duration': max_duration_request
    }

    print(type(str(min_duration_request)))
    for value in unique_fields[-1]['publication_year']:
        print(type(value))

    hits, total_hits, info = search_movies('movies', **search_params)

    movie_data_list = [{key: value for key, value in hit['_source'].items()} for hit in hits]
    render_params = {
        'res': movie_data_list,
        'search_info': info,
        'page': page_request,
        'page_size': page_size,
        'total_hits': total_hits,
        'unique_fields': unique_fields
    }

    return render_template('db.html', **render_params)


@app.route('/map')
def map_page():
    return render_template('map.html')


@app.route('/analysis')
def analysis_page():
    return render_template('analysis.html')
