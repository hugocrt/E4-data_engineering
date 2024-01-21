from flask import render_template, request, Flask
from ..utils.utils import *
from ..Elasticsearch_utils.elasticsearch_operations import *

app = Flask(__name__)
collection = connect_to_mongodb(app)
unique_fields = retrieve_unique_fields(collection)
data = retrieve_mongo_data(collection)
create_index(es_client, data)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/db', methods=['GET'])
def database_page():
    order = request.args.get('sort_order', default='asc', type=str)
    page = request.args.get('page', default=1, type=int)
    page_size = 30

    filters = Filters(
        title=request.args.get('title_query', default='', type=str),
        directors=request.args.getlist('Réalisateurs'),
        genres=request.args.getlist('Genres'),
        native_countries=request.args.getlist('Pays de production'),
        min_duration=request.args.get('min_duration', default='', type=str),
        max_duration=request.args.get('max_duration', default='', type=str),
        min_year=request.args.get('min_year', default='', type=str),
        max_year=request.args.get('max_year', default='', type=str),
    )

    hits, total_hits, search_details = search_movies('movies', filters, page, page_size, order)

    movie_data_list = [{key: value for key, value in hit['_source'].items()} for hit in hits]
    print(movie_data_list)

    render_params = {
        'movie_data_list': movie_data_list,
        'search_details': search_details,
        'page': page,
        'page_size': page_size,
        'total_hits': total_hits,
        'unique_fields': unique_fields
    }

    return render_template('db.html', **render_params)


@app.route('/map')
def map_page():
    countries_counts = count_per_field(field='native_countries')
    folium_map, country_colors = generate_map(countries_counts)
    render_params = {
        'folium_map': folium_map,
        'info': countries_counts,
        'country_colors': country_colors,
    }
    return render_template('map.html', **render_params)


@app.route('/analysis')
def analysis_page():

    genres_counts = count_per_field(field='genres')
    tot_genres = len(genres_counts)

    director_counts = count_per_field(field='director')
    top15_dir = {key: director_counts[key] for key in islice(director_counts, 15)}

    year_counts = count_per_field(field='publication_year')

    duration_counts = count_per_field(field='duration')
    inf150_movies = sum(value for duration, value in duration_counts.items() if duration <= 150)
    sum_movies = sum(duration_counts.values())
    percent_inf150_movies = int(round((inf150_movies / sum_movies) * 100, 0))


    render_param = {
        'genres_piechart': create_pie_chart(genres_counts,
                                         'Fréquences d\'apparitions des genres dans le top 1000',
                                         'genres_piechart.png'),
        'duration_hist': create_histogram(duration_counts,
                                          'Distribution du temps (min) des films',
                                          'duration_hist.png'),
        'year_hist': create_histogram(year_counts,
                                          'Distribution des années de parution des films',
                                          'year_hist.png'),
        'tot_genres': tot_genres,
        'top15_dir': top15_dir,
        'duration_counts': duration_counts,
        'percent_inf150_movies': percent_inf150_movies
    }

    return render_template('analysis.html', **render_param)
