import requests
import math
from datetime import datetime
import pandas as pd
import pickle
import MySQLdb
from MySQLdb import escape_string as thwart



connection = MySQLdb.connect(
                            host='localhost', 
                            user = 'root', 
                            password = 'learntocode27', 
                            db = 'flaskproject'
                            )
cursor = connection.cursor()

lat = '53.6693538' 
lng = '23.8131306'

def get_weather(lat, lon):

    weather_key = 'dd50b92e38f6ed0c9dc3990ab98f1773'


    url = f"https://api.openweathermap.org/data/2.5/weather"

    querystring = {"lat":lat,"lon":lon, 'appid':weather_key}


    response = requests.get(url, params=querystring)

    content = (response.json())

    main = content['weather'][0]['main']
    description = content['weather'][0]['description']
    temp = round(float(content['main']['temp']) - 273.15 , 2) # Celsius
    temp_feels_like = round(float(content['main']['feels_like']) - 273.15 , 2) # Celsius
    humidity = content['main']['humidity'] # %
    wind_speed = content['wind']['speed'] # m/s
 
    print(response.json())

    print(main, description, temp, temp_feels_like, humidity, wind_speed)


def get_weather_5(lat, lon):

    weather_key = 'dd50b92e38f6ed0c9dc3990ab98f1773'


    url = f"https://api.openweathermap.org/data/2.5/forecast"

    querystring = {"lat":lat,"lon":lon, 'appid':weather_key}


    response = requests.get(url, params=querystring)

    content = response.json()

    city_name = content['city']['name']

    for index, entry in enumerate(content['list']):

        main = entry['weather'][0]['main']
        description = entry['weather'][0]['description']
        time = datetime.fromtimestamp(int(entry['dt']))
        temp = round(float(entry['main']['temp']) -275.15, 2)
        feels_like = round(float(entry['main']['feels_like'])-275.15, 2)
        pressure = entry['main']['pressure']
        humidity = entry['main']['humidity']
        wind_speed = entry['wind']['speed']

        try:
            cursor.execute('INSERT IGNORE INTO weather (location, main, description, time,\
            temperature, feels_like, pressure, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (thwart(city_name), thwart(main), thwart(description), thwart(str(time)), thwart(str(temp)), thwart(str(feels_like)), thwart(str(pressure)),
            thwart(str(humidity)), thwart(str(wind_speed))))
        except Exception as e:
            print(e)
    connection.commit()
    result = cursor.execute("SELECT * FROM weather")
    result = cursor.fetchall()
    print(len(result))
    print(result)
    

def get_coordinates():

    ip = '37.212.60.60'

    url = f"https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/{ip}"

    opencage_key = '0393e6ddf4344a1c844a5a5cd2bf23e5'

    headers = {
        'x-rapidapi-host': "ip-geolocation-ipwhois-io.p.rapidapi.com",
        'x-rapidapi-key': "b3e33994b9mshd8f39d1dfaa3e21p198457jsnc8985ee58d8d"
        }

    response = requests.get(url, headers = headers)

    content = response.json()
    lat = content['latitude']
    lng = content['longitude']
    print(lat, lng)

if __name__ == "__main__":
    result = cursor.execute("SELECT * FROM weather")
    result = cursor.fetchall()
    print(len(result))
    print(result)
    #get_weather(lat, lng)
    #get_weather_5(lat, lng)
