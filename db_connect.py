import MySQLdb
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta, date
from PIL import Image
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import json, gc
import requests
import math, decimal


def timedelta_format(delta, seconds = False):
        if seconds:
            days = int(delta//(3600*24))
            seconds = delta - days*3600*24
        else:
            days = delta.days
            seconds = delta.total_seconds() - days*3600*24
        hours = int(seconds//3600)
        minutes = int((seconds - hours*3600)//60)
        formated_time = {'days': days, 'hours': hours, 'minutes': minutes}
        return formated_time


class DbConnection():
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("SHOW TABLES")
        except Exception as e:
            print(e, 'not connected, recconecting to Db')
            self.connection = MySQLdb.connect(
                            host='localhost', 
                            user = 'root', 
                            password = 'learntocode27', 
                            db = 'flaskproject'
                            )
            self.cursor = self.connection.cursor()
        return self.connection, self.cursor

    def close(self):
        self.cursor.execute("FLUSH TABLES")
        self.cursor.execute("FLUSH LOGS")
        self.cursor.close()
        self.connection.close()
        gc.collect()

    def check_username(self, username):
        self.connect()
        check = self.cursor.execute("SELECT * FROM users WHERE username = (%s)", (thwart(username),))
        result = self.cursor.fetchall()
        if int(check) > 0:
            self.close()
            return ('That username has already been taken, please, choose another one')
        self.close()

    
    def insert_user(self, username, password, email):
        #blob_value = open('static/images/logo.png', 'rb').read()
        self.connect()
        self.cursor.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
         (thwart(username), thwart(password), thwart(email), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()
        self.close()

    def show_table(self):
        check = self.cursor.execute("SELECT * FROM housing")
        result = self.cursor.fetchall()
        self.close()
        print(result)


    def login(self, username, password):
        self.connect()
        check = self.cursor.execute("SELECT password FROM users WHERE username = (%s)", (thwart(username),))
        result = self.cursor.fetchone()
        if sha256_crypt.verify(password, result[0]):
            self.close()
            return True
        self.close()
        return False

    
    def get_userdata(self, username):
        self.connect()
        search = self.cursor.execute("SELECT * FROM users WHERE username = (%s)", (thwart(username),))
        data = self.cursor.fetchone()
        user_id = data[0]
        user_username = data[1]
        user_email = data[3]
        self.close()
        return (user_id, user_username, user_email)

    
    def get_cities_select_options(self, value):
        self.connect()
        self.cursor.execute("SELECT * FROM countries WHERE lower(city) LIKE '%s%%'" %(value,))
        result = self.cursor.fetchall()
        self.close()
        return result

    def get_countries_select_options(self, value):
        self.connect()
        self.cursor.execute("SELECT DISTINCT country FROM countries WHERE lower(country) LIKE '%s%%'" %(value,))
        result = self.cursor.fetchall()
        self.close()
        return result

    def get_distance(self, route):
        self.connect()
        origin = route[0]
        destination = route[1]
        origin_name = origin.split(',')[0]
        destination_name = destination.split(',')[0]

        earth_radius = 6370 #km
        self.cursor.execute("SELECT lat, lng FROM countries WHERE city = (%s)", (thwart(origin_name),))
        cor = self.cursor.fetchone()
        lat1 = cor[0]
        lng1 = cor[1]
        self.cursor.execute("SELECT lat, lng FROM countries WHERE city = (%s)", (thwart(destination_name),))
        cor = self.cursor.fetchone()
        lat2 = cor[0]
        lng2 = cor[1]

        a = math.cos(lat1*decimal.Decimal(math.pi/180))*math.cos(lat2*decimal.Decimal(math.pi/180))*math.cos(lng1*decimal.Decimal(math.pi/180))*math.cos(lng2*decimal.Decimal(math.pi/180))
        b = math.cos(lat1*decimal.Decimal(math.pi/180))*math.cos(lat2*decimal.Decimal(math.pi/180))*math.sin(lng1*decimal.Decimal(math.pi/180))*math.sin(lng2*decimal.Decimal(math.pi/180))
        c = math.sin(lat1*decimal.Decimal(math.pi/180))*math.sin(lat2*decimal.Decimal(math.pi/180))
        distance = round(math.acos(a+b+c)*earth_radius, 2) #km
        self.close()

        return distance

    
    def create_table(self):
        try:
            self.cursor.execute("ALTER TABLE trips MODIFY COLUMN arrival DATETIME")
            self.cursor.execute("ALTER TABLE trips ADD post_date DATE")
            self.cursor.execute("CREATE TABLE trips \
            (trip_id INT(11) AUTO_INCREMENT PRIMARY KEY, origin VARCHAR(30), destination VARCHAR(30),\
            departure DATE, arrival DATE, fare VARCHAR(20), currency VARCHAR(10), origin_country VARCHAR(20),\
            destination_country VARCHAR(20), distance VARCHAR(20), road_time VARCHAR(40), uid INT(11), \
            FOREIGN KEY (uid) REFERENCES users (uid) ON DELETE CASCADE)")
            
        except Exception as e:
            print(e)

    def show_trips_table(self):
        self.connect()
        check = self.cursor.execute("SELECT * FROM trips")
        result = self.cursor.fetchall()
        self.close()

    def get_routes(self, user_id):
        self.connect()
        self.cursor.execute("SELECT origin, destination, departure, arrival, fare, currency, origin_country, destination_country, road_time, distance, trip_id\
         FROM trips WHERE uid = (%s) ORDER BY arrival DESC", 
        (thwart(user_id), ))
        result = self.cursor.fetchall()
        self.close()
        return result

    def get_housing(self, user_id):
        self.connect()
        self.cursor.execute("SELECT *\
         FROM housing WHERE uid = (%s) ORDER BY start_date DESC", 
        (thwart(user_id), ))
        result = self.cursor.fetchall()
        self.close()
        return result


    def delete_user(self, user_id):
        self.cursor.execute('DELETE FROM users WHERE uid = (%s)', (thwart(user_id), ))
        self.connection.commit()
        self.close()

    def delete_route(self, route_id):
        self.connect()
        self.cursor.execute('DELETE FROM trips WHERE trip_id = (%s)', (thwart(route_id), ))
        self.connection.commit()
        self.close()

    def delete_housing(self, start_date):
        self.connect()
        self.cursor.execute('DELETE FROM housing WHERE start_date = (%s)', (thwart(start_date), ))
        self.connection.commit()
        self.close()


    def count_time(self, first_date, second_date):
        first_date = datetime.strptime(first_date, '%Y-%m-%d %H:%M:%S')
        second_date = datetime.strptime(second_date, '%Y-%m-%d %H:%M:%S')
        road_time = second_date - first_date
        road_time_seconds = road_time.total_seconds()
        return road_time, road_time_seconds


    def format_time(self, date):
        date = date.strftime('%d.%m.%Y %H:%M:%S')
        return date

    def add_route(self, data):
        self.connect()
        origin, destination, departure, arrival, fare, currency, road_time, uid, distance = data
        origin_city = origin.split(',')[0]
        origin_country = origin.split(',')[1]
        destination_city = destination.split(',')[0]
        destination_country = destination.split(',')[1]
        currency_sym = currency.split(',')[1].strip()
        self.cursor.execute("INSERT INTO trips (origin, destination, departure, arrival, fare, currency, origin_country, destination_country, road_time, uid, post_date, distance) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
         (thwart(origin_city), thwart(destination_city), thwart(departure), thwart(arrival), thwart(fare), thwart(currency_sym), 
         thwart(origin_country), thwart(destination_country), thwart(str(road_time)), thwart(uid), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), thwart(str(distance))))
        self.connection.commit()
        self.close()

    def add_housing(self, data):
        self.connect()
        country, address, start_date, end_date, fare, currency, time, sum_rub, uid = data
        self.cursor.execute("INSERT IGNORE INTO housing (country, address, start_date, end_date, fare, currency, time, sum_rub, uid) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
         (thwart(country), thwart(address), thwart(start_date), thwart(end_date), thwart(fare), thwart(currency), 
         thwart(time), thwart(sum_rub), thwart(uid)))
        self.connection.commit()
        self.close()

    def check_dublicate_routes(self, new_route):
        self.connect()
        
        user_id = str(new_route[7])
        origin = new_route[0].split(',')[0]
        destination = new_route[1].split(',')[0]
        new_route = (origin, destination, datetime.strptime(new_route[2], '%Y-%m-%d %H:%M:%S'), datetime.strptime(new_route[3], '%Y-%m-%d %H:%M:%S'))
        self.cursor.execute("SELECT origin, destination, departure, arrival FROM trips WHERE uid = (%s)", 
        (thwart(user_id), ))
        routes = self.cursor.fetchall()
        if any(route == new_route for route in routes):
            self.close()
            return True
        else:
            self.close()
            return False



class Statistics():
    def __init__(self, connection, user_id):
        self.status = False
        self.country_percent = {}
        self.connection, self.cursor = connection.connect()
        self.country_time = {}
        self.total_fare = 0
        self.total_time = 0
        self.user_id = user_id
        self.current_country = None
        self.curr_location = None
        self.curr_location_time = None
        self.get_current_info()
        self.get_past_info()
        self.total_distance = 0
           

    def get_current_info(self):
        self.cursor.execute("SELECT arrival, destination_country FROM trips WHERE uid = (%s) ORDER BY arrival DESC LIMIT 1", 
        (thwart(self.user_id), ))
        result = self.cursor.fetchone()
        if len(result) > 0:
            self.curr_location = result[1]
            arrival_date = result[0]
            self.curr_loc_time = datetime.now() - arrival_date
            self.curr_location_time = timedelta_format(self.curr_loc_time)

    def get_past_info(self):
        self.cursor.execute("SELECT departure, arrival, fare, currency, origin_country, destination_country, distance FROM trips WHERE uid = (%s) ORDER BY arrival", 
        (thwart(self.user_id), ))
        routes = self.cursor.fetchall()
        self.connection.close()
        if len(routes) > 1:
            self.status = True
            self.total_distance = 0
            for route in routes:
                self.total_fare += float(route[2])
                self.total_distance += float(route[6])
            for i in range(len(routes)):
                if i == 0:
                    accomodation_country = routes[0][5]
                    arrival_time = routes[0][1]
                else:
                    departure_time = routes[i][0]
                    spent_time = departure_time - arrival_time
                    if accomodation_country not in self.country_time:
                        self.country_time[accomodation_country] = spent_time.total_seconds()
                    else:
                        self.country_time[accomodation_country] += spent_time.total_seconds()
                    accomodation_country = routes[i][5]
                    arrival_time = routes[i][1]
                    self.total_time+= spent_time.total_seconds()

            if self.curr_location in self.country_time:
                self.country_time[self.curr_location] += self.curr_loc_time.total_seconds()
            else:
                self.country_time[self.curr_location] = self.curr_loc_time.total_seconds()
            self.total_time += self.curr_loc_time.total_seconds()

            self.plot = self.create_plot(self.country_time)

            for el in self.country_time:
                self.country_percent[el] = round((self.country_time[el]/self.total_time)*100, 2)
                self.country_time[el] = timedelta_format(self.country_time[el], seconds = True)

            self.total_fare = round(self.total_fare, 2)
            
    def create_plot(self, data):
        df = pd.Series(data, name = 'values') 
        df.index.name = 'labels'
        df = df.reset_index()

        data = [
            go.Pie(
                values=df['values'],
                labels=df['labels'],
                textinfo='label+percent'
            )
        ]



        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON
        

class LocationInfo():
    def __init__(self, location, ip_address, connection):
        self.connection = connection
        self.ip_address = ip_address
        self.location = str(location).strip()
        self.url = "https://free.currconv.com/api/v7/convert"
        self.host_key = '91a7c6b71f4a592e8c59'
        self.curr_list =  pd.read_csv('curr-country.txt')
        self.curr_list.columns = ["country", "currency"]
        self.curr_currency = self.curr_list[self.curr_list['country'] == self.location]['currency'].values[0]
        self.lat, self.lng = self.get_current_coordinats()
        self.get_weather_5()


    def get_weather(self):

        weather_key = 'dd50b92e38f6ed0c9dc3990ab98f1773'

        url = f"https://api.openweathermap.org/data/2.5/weather"

        querystring = {"lat": self.lat,"lon": self.lng, 'appid':weather_key}

        response = requests.get(url, params=querystring)

        content = response.json()

        main = content['weather'][0]['main']
        description = content['weather'][0]['description']
        temp = round(float(content['main']['temp']) - 273.15 , 2) # Celsius
        temp_feels_like = round(float(content['main']['feels_like']) - 273.15 , 2) # Celsius
        humidity = content['main']['humidity'] # %
        wind_speed = content['wind']['speed'] # m/s

        return(main, description, temp, temp_feels_like, humidity, wind_speed)

    
    def get_weather_5(self):
        self.connection.connect()
        weather_key = 'dd50b92e38f6ed0c9dc3990ab98f1773'
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        querystring = {"lat": self.lat,"lon": self.lng, 'appid':weather_key}
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
                self.connection.cursor.execute('INSERT IGNORE INTO weather (location, main, description, time,\
                temperature, feels_like, pressure, humidity, wind_speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (thwart(city_name), thwart(main), thwart(description), thwart(str(time)), thwart(str(temp)), thwart(str(feels_like)), thwart(str(pressure)),
                thwart(str(humidity)), thwart(str(wind_speed))))
            except Exception as e:
                print(e)
        
        self.connection.connection.commit()
        self.connection.close()



    def get_current_coordinats(self):
        if self.ip_address == '127.0.0.1':
            self.ip_address = '37.212.60.60'

        url = f"https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/{self.ip_address}"

        headers = {
            'x-rapidapi-host': "ip-geolocation-ipwhois-io.p.rapidapi.com",
            'x-rapidapi-key': "b3e33994b9mshd8f39d1dfaa3e21p198457jsnc8985ee58d8d"
            }

        response = requests.get(url, headers = headers)
        content = response.json()

        lat = content['latitude']
        lng = content['longitude']

        return lat, lng

    def get_current_rate(self):
        
        querystring = {'q': f'{self.curr_currency}_RUB,USD_{self.curr_currency},EUR_{self.curr_currency}',
                        "apiKey": self.host_key}
        response = requests.get(self.url, params=querystring)
        if response.status_code == '200':
            content = response.json()
            exchange_rate = []
            for value in content['results']:
                exchange_rate.append((value, content['results'][value]['val']))

            response.close()
            return exchange_rate
        else:
            return 'LIMIT REACHED'

    def get_rate(self, currency, date):

        querystring = {'q': f'{currency[:3]}_RUB', 'date': date.strftime('%Y-%m-%d'),
                            "apiKey": self.host_key}

        response = requests.get(self.url, params=querystring)
        if response.status_code == '200':
            content = response.json()
            exchange_rate = []
            for value in content['results']:
                exchange_rate.append((value, content['results'][value]['val']))

            response.close()
            return exchange_rate
        else:
            return 'LIMIT REACHED'

    def get_rate_2(self, currnecy):
        apiKey = 'frNWPBXvQ9fhJ7zHru2g8NjNth6JRA'

    def get_weekly_rates(self):
        
        endDate = datetime.now().date()
        week = timedelta(days = 7)
        start_date = endDate - week

        querystring = {'q': f'{self.curr_currency}_RUB,USD_{self.curr_currency},EUR_{self.curr_currency},JPY_{self.curr_currency}',
                        'date': start_date,
                        'endDate': endDate,
                        "apiKey": self.host_key}



        response = requests.get(self.url, params=querystring)

        content = response.json()
        exchange_rate = []
        titles = []
        for value in content['results']:
            titles.append(value.replace('_', ' to '))

        fig = make_subplots(rows=2, cols=2, subplot_titles=titles)
        i = 1
        j = 1
        for value in content['results']:
            if i == 3:
                i = 1
                j+=1
            df = pd.Series(content['results'][value]['val'], name = 'values') 
            df.index.name = 'dates'
            df = df.reset_index()
            mean = df['values'].mean()
            fig.add_trace(
                go.Scatter(x=df['dates'], y=df['values'], name = value.replace('_', ' to ')),
                row=j, col=i
                )
            fig.update_xaxes(title_text = f'Mean {round(mean,2)}' ,tickformat = '%d.%m.%Y', row=j, col=i)
            i+=1

        fig.update_layout(height=600, width = 1000, showlegend=False)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        response.close()

        return graphJSON


    def graph_weather(self):
        self.connection.connect()
        result = self.connection.cursor.execute('SELECT time, feels_like, temperature, pressure, humidity, wind_speed FROM weather')
        result = self.connection.cursor.fetchall()
        df = pd.DataFrame(list(result), columns = ['time', 'Feels like', 'Temperature, Grad', 'Pressure, kPa', 'Humidity, %', 'Wind speed, m/s'])
        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        self.connection.close()

        fig = make_subplots(rows=2, cols=2, subplot_titles=df.columns[1:])


        for index, column in enumerate(df.columns[1:]):

            mean = round(df[column].mean(), 2)

            fig.add_trace(
                    go.Scatter(x=df.index, y=df[column], name = column),
                    row=index//2+1, col=index%2+1
                    )
            fig.update_xaxes(tickmode = 'linear', tick0 = df.index[4], title_text = f'Mean value {mean}' ,tickformat = '%d.%m.%y', row=index//2+1, col=index%2+1)

        fig.add_trace(
                    go.Scatter(x=df.index, y=df[df.columns[0]], name = df.columns[0]),
                    row=1, col=1
                    )

        fig.update_layout(height=600, width = 1000, showlegend=False)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON

    
                



