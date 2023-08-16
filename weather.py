import os
import sys

from dotenv import load_dotenv

import requests
import json

from art import tprint

try:
    load_dotenv('.env')
    API = os.getenv('API_TOKEN', default=None)

    if API is None or API == '':
        print('[-] API_TOKEN is not provided. Please set the API_TOKEN in your .env file.')
        sys.exit(1)  # завершение программы с кодом ошибки

except Exception as e:
    print(f'[-] An error occurred while loading environment variables: {e}')
    sys.exit(1)


def check_weather(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API}&units=metric'
    try:
        response = requests.get(url)
        if response:
            print('[+] Data is received from the server. Data processing..')
            weather = response.json()
            try:
                print(f'[+] City: {weather["name"]}')
                print(f'[+] Temperature: {weather["weather"][0]["main"]}')
                print(f'[+] Feels like: {weather["main"]["feels_like"]}')
                print(f'[+] Humidity: {weather["main"]["humidity"]}')
                print(f'[+] Wind: {weather["wind"]["speed"]}')
                print(f'[+] Cloudiness: {weather["weather"][0]["description"]} - '
                      f'{weather["clouds"]["all"]}')
            except KeyError as exception:
                print(f'[-] Error occurred while parsing API response: {exception}.\nData format error.')
        elif response.status_code == 404:
            print('[-] City not found. Please check the entered city name.')
        else:
            print(f'[-] An error occurred: {response.status_code} - {response.reason}')
    except requests.exceptions.ConnectionError:
        print(f'[-] Connection ERROR! Check your connection to the internet..')
        # print(f'{exception}')
    except requests.exceptions.Timeout:
        print("[-] Timeout ERROR! The request took too long to complete.")
    except requests.exceptions.TooManyRedirects:
        print("[-] Too many redirects occurred.")
    except requests.exceptions.HTTPError as exception:
        print(f"[-] HTTP Error occurred: {exception}")
    except requests.exceptions.RequestException as exception:
        print(f"[-] An error occurred during the request: {exception}")
    finally:
        print('*' * 30)


if __name__ == '__main__':
    tprint('WEATHER')
    city = input('[/] Enter the name of the city: ')
    print('*' * 30)
    check_weather(city_name=city)
