import requests, json
from datetime import datetime

TOKEN = '5409091546:AAG8686b4kyMpyPenIjHQqxZ5HxIwyvwFrI'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "2e3c8af964ae0130a52f86bd97aefd81"
CITY = ['Bishkek', 'Osh', 'Jalal-Abad', 'Karakol',
        'Kyzyl-Kiya', 'Uzgen', 'Balykchy', 'Kara-Balta',
        'Naryn', 'Talas']

TEXT_FOR_USERS = f"0 - {CITY[0]} \n" \
                 f"1 - {CITY[1]} \n" \
                 f"2 - {CITY[2]} \n" \
                 f"3 - {CITY[3]} \n" \
                 f"4 - {CITY[4]} \n" \
                 f"5 - {CITY[5]} \n" \
                 f"6 - {CITY[6]} \n" \
                 f"7 - {CITY[7]} \n" \
                 f"8 - {CITY[8]} \n" \
                 f"9 - {CITY[9]} \n"

def response_weather(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url)
    all_info = json.loads(response.text)
    main = all_info['main']
    weather = {
        'City': f'{city}',
        'Date': f'{datetime.now()}',
        'Temperature': f'{main["temp"]}',
        'Feels_like': f'{main["feels_like"]}',
    }
    return weather
