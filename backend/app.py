from flask import Flask, render_template, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

# Create a MongoClient to the running MongoDB instance
client = MongoClient('localhost', 27017)
db = client['weather_news_database']
collection = db['news']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect_api', methods=['GET', 'POST'])
def connect_api():
    if request.method == 'POST':
        city = request.form["city"]

        # First, try to find news data in the database
        news_data = collection.find_one({"city": city})

        # If the news data isn't in the database, fetch it from the API and store it
        if not news_data:
            news_data = get_weather_news(city)
            collection.insert_one({"city": city, "data": news_data})

        return render_template('news.html', news=news_data)


def get_weather_news(city):
    url = "https://newsapi.org/v2/everything"

    querystring = {
        "q": f"{city}",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": "139b0bea30c0465790f12c53116b74cd",
        "source": "cnn, abc-news",
        "language": "en"
    }

    response = requests.request("GET", url, params=querystring)
    return response.json()





if __name__ == '__main__':
    app.run()
