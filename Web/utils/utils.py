import pandas as pd
import folium, branca
import matplotlib.pyplot as plt
import numpy as np
from unidecode import unidecode
from flask_pymongo import PyMongo
from itertools import islice


class Filters(object):
    def __init__(self, title=None, directors=None, genres=None, native_countries=None,
                 min_duration='', max_duration='', min_year='', max_year=''):
        self.title = title.lower()
        self.director = directors
        self.genres = genres
        self.native_countries = native_countries
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.min_publication_year = min_year
        self.max_publication_year = max_year


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


def generate_map(result_search):
    csv_file = 'Web/FlaskApp/annexes/geocoded_countries.csv'
    df = pd.read_csv(csv_file)

    count_countries_map = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')
    coef = 2
    min_value = min(result_search.values())**(1/coef)
    max_value = max(result_search.values())**(1/coef)
    cm = branca.colormap.LinearColormap(['blue', 'red'], vmin=min_value, vmax=max_value)
    count_countries_map.add_child(cm)

    country_colors = {}
    for country, value in result_search.items():
        lat = df.loc[df['Pays'] == country, 'Latitude'].values[0]
        lon = df.loc[df['Pays'] == country, 'Longitude'].values[0]
        color = cm(value**(1/coef))
        country_colors[country] = color

        folium.CircleMarker(
            location=(lat, lon),
            radius=value*0.25,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=f"{country}: {value}"
        ).add_to(count_countries_map)

    return count_countries_map._repr_html_(), country_colors


def create_histogram(dictionary, title, filename):
    keys, values = zip(*dictionary.items())

    positions = np.array(list(keys))

    data_range = max(keys) - min(keys)

    plt.bar(
        positions,
        height=values,
        width=data_range / len(dictionary),
        color='blue',
        alpha=0.6,
        align='center'
    )
    plt.title(title)
    plt.xlabel('Valeurs')
    plt.ylabel('Nombre d\'apparitions')
    plt.savefig(f'Web/FlaskApp/static/img/{filename}', bbox_inches='tight')
    plt.close()


def create_pie_chart(data, title, filename):
    # Trier le dictionnaire par valeurs dans l'ordre décroissant
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    # Séparer les 15 premières valeurs et le reste
    top_15 = dict(list(sorted_data.items())[:15])
    other = dict(list(sorted_data.items())[15:])

    # Regrouper les valeurs restantes sous la clé "Autre"
    other_value = sum(other.values())
    top_15['Autre'] = other_value

    labels = list(top_15.keys())
    sizes = list(top_15.values())

    # Création du donut chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))

    # Personnalisation pour créer un trou au centre (donut)
    centre_circle = plt.Circle((0, 0), 0.2, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title(title)

    # Sauvegarde du graphique
    plt.savefig(f'Web/FlaskApp/static/img/{filename}', bbox_inches='tight')
    plt.close()
