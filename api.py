import requests
import math


def get_coordinates(first_city, second_city):

    cities = [first_city, second_city]

    coordinates = []

    url = "https://opencage-geocoder.p.rapidapi.com/geocode/v1/json"

    opencage_key = '0393e6ddf4344a1c844a5a5cd2bf23e5'

    headers = {
        'x-rapidapi-host': "opencage-geocoder.p.rapidapi.com",
        'x-rapidapi-key': "b3e33994b9mshd8f39d1dfaa3e21p198457jsnc8985ee58d8d"
        }

    for city in cities:

        querystring = {"language":"en","key":f"{opencage_key}","q":f"{city}"}
        response = requests.get(url, headers=headers, params=querystring).json()

        lat = response['results'][0]['geometry']['lat']
        lng = response['results'][0]['geometry']['lng']
        print(lat, lng)

        coordinates.append((lat, lng))

    return coordinates

def calculate_distance(coordinates):

    earth_radius = 6370 #km
    lat1 = coordinates[0][0]
    lng1 = coordinates[0][1]
    lat2 = coordinates[1][0]
    lng2 = coordinates[1][1]

    a = math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.cos(lng1*math.pi/180)*math.cos(lng2*math.pi/180)
    b = math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.sin(lng1*math.pi/180)*math.sin(lng2*math.pi/180)
    c = math.sin(lat1*math.pi/180)*math.sin(lat2*math.pi/180)

    distance = math.acos(a+b+c)*earth_radius #km

    return distance

distance = calculate_distance(get_coordinates('Minsk, Belarus', 'Moscow, Russia'))
print(distance)