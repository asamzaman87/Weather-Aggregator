from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect_api', methods=['GET', 'POST'])
def connect_api():
    if request.method == 'POST':
        city = request.form["city"]
        news_data = get_weather_news(city)
        return render_template('news.html', news=news_data, city=city)


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
