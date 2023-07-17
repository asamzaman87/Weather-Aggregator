from flask import Flask, render_template, request
import requests
from pymongo import MongoClient
import plotly.express as px
import pandas as pd
import plotly.io as pio

app = Flask(__name__)

# Create a MongoClient to the running MongoDB instance
client = MongoClient('localhost', 27017)
db = client['weather_news_database']
collection = db['news']


@app.route('/')
def index():
    return render_template('index.html')


# make sure MongoDB DB is running. Here are the steps:
# 1- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# 2- brew tap mongodb/brew
# 3- brew install mongodb-community
# 4- brew services start mongodb-community

@app.route('/connect_api', methods=['GET', 'POST'])
def connect_api():
    if request.method == 'POST':
        city = request.form["city"]

        # First, try to find news data in the database
        news_data = collection.find_one({"city": city})['data']

        # If the news data isn't in the database, fetch it from the API and store it
        if not news_data:
            news_data = get_weather_news(city)
            collection.insert_one({"city": city, "data": news_data})

        fig = mateo(city)
        fig_html = pio.to_html(fig, full_html=False)

        return render_template('news.html', news=news_data, fig=fig_html)


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


# Geocode; this translates the city into coordinates and sends that to mateo
def get_coords(city):
    appid = '721680ff54a03bc78d8ee5423fd07e8f'
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={appid}'
    r = requests.get(url)
    if r.status_code == 200:
        data2 = r.json()
        latitude = data2[0]['lat']
        longitude = data2[0]['lon']
        cords = []
        cords.append(str(latitude))
        cords.append(str(longitude))
        return (cords)
    else:
        print('Error occurred', r.status_code)


# Open Mateo; this gets all the weather information
def mateo(city):
    cords = get_coords(city)
    URL = f'https://api.open-meteo.com/v1/forecast?latitude={cords[0]}&longitude={cords[1]}&daily=weathercode,' \
          f'temperature_2m_max,temperature_2m_min,windspeed_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&' \
          f'precipitation_unit=inch&timezone=auto&past_days=7'
    l = requests.get(URL)
    if l.status_code == 200:
        data1 = l.json()

        variables = list(data1["daily_units"])
        labels = list(data1['daily']['time'])
        weather_values = list(data1['daily']['weathercode'])
        tempmax_values = list(data1['daily']['temperature_2m_max'])
        tempmin_values = list(data1['daily']['temperature_2m_min'])
        wind_values = list(data1['daily']['windspeed_10m_max'])
    else:
        print('Error occurred', l.status_code)

    iterations = (len(variables) - 1)
    xvars = labels * iterations
    yvars = weather_values + tempmax_values + tempmin_values + wind_values

    # Displays Weather information in line graph
    df = pd.DataFrame({'Day': xvars, 'Value': yvars,
                       'Condition': ['Weather Codes WMO Code'] * len(weather_values) + ['Min Temp °F'] * len(
                           tempmin_values) +
                                    ['Max Temp °F'] * len(tempmax_values) + ['Wind Speed Mph'] * len(wind_values)})
    fig = px.line(df, x='Day', y='Value', color='Condition')
    return fig


if __name__ == '__main__':
    app.run()
