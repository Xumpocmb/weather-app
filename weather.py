import os
from dotenv import load_dotenv

import requests
import json

from art import tprint


load_dotenv('.env')
API = os.getenv('API_TOKEN', default=None)


def check_weather(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric'
    try:
        response = requests.get(url)
        if response:
            write_info_to_file(response, city_name)
            # with open("weather.json", "r") as file:
            #     weather_data = json.load(file)

            weather = response.json()
            print(f'[+] City: {weather["name"]}')
            print(f'[+] Temperature: {weather["weather"][0]["main"]}')
            print(f'[+] Feels like: {weather["main"]["feels_like"]}')
            print(f'[+] Humidity: {weather["main"]["humidity"]}')
            print(f'[+] Wind: {weather["wind"]["speed"]}')
            print(f'[+] Cloudiness: {weather["weather"][0]["description"]} - '
                  f'{weather["clouds"]["all"]}')
        elif response.json()["message"] == 'city not found':
            print('[-] Please check that the city name is entered correctly..')
        else:
            print(f'{response.json()["message"]}')
    except requests.exceptions.ConnectionError as exception:
        print(f'[-] Connection ERROR! Check your connection to the internet..')
        # print(f'{exception}')
    finally:
        print('*' * 30)


def write_info_to_file(data, city_name):
    with open(f'weather-{city_name}.json', 'w') as file:
        json.dump(data.json(), file, indent=4)


if __name__ == '__main__':
    tprint('WEATHER')
    city = input('[/] Enter the name of the city: ')
    print('*' * 30)
    check_weather(city_name=city)
