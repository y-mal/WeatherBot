import requests, json
from datetime import datetime

TOKEN = '5409091546:AAG8686b4kyMpyPenIjHQqxZ5HxIwyvwFrI'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "2e3c8af964ae0130a52f86bd97aefd81"
CITY = "Bishkek"


def response_weather():
    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url)
    all_info = json.loads(response.text)
    main = all_info['main']
    weather = {
        'City': f'{CITY}',
        'Date': f'{datetime.now()}',
        'Temperature': f'{main["temp"]}',
        'Feels_like': f'{main["feels_like"]}',
    }
    return weather
