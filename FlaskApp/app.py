from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)


def connect_to_mongodb():
    try:
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/senscritique'
        mongo = PyMongo(app)
        collection = mongo.db.movies
        return collection

    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/db', methods=['GET'])
def database_page():
    collection = connect_to_mongodb()
    res = []
    for item in collection.find()[:5]:
        res.append({
            'title': item['title'],
            'ranking': item['ranking'],
            'genres': item['genres'],
            'director': item['director'],
            'duration': item['duration'],
            'publication_year': item['publication_year'],
            'poster': item['poster'],
            'native_countries': item['native_countries'],

        })
    return render_template('db.html', res=res)


@app.route('/map')
def map_page():
    return render_template('map.html')


@app.route('/analysis')
def analysis_page():
    return render_template('analysis.html')


if __name__ == '__main__':
    app.run(debug=True)
