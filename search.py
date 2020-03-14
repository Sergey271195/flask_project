import pandas as pd
import pickle, math

class Route():
    def __init__(self):
        try:

            #self.useful_data = pd.read_pickle('countries.pickle')
            
            self.search_list = ['1', '2']
        except:
            self.data = pd.read_csv('/home/sergey/Desktop/Flask/static/worldcities.csv')
            subs = ['`', '\'']
            for sub in subs:
                self.data['Drop_index'] = self.data['city_ascii'].str.find(sub)
                self.data = self.data[self.data['Drop_index'] != 0]
            self.sorted_data = self.data.sort_values('city_ascii').reset_index()
            self.search_list = self.sorted_data[['city_ascii', 'country']].to_numpy()
            self.pickle_data = self.sorted_data[['city_ascii', 'country', 'lat', 'lng']]
            self.pickle_data.to_pickle('countries.pickle')
            self.useful_data = self.pickle_data

    def count_miles(self, route):
        origin = route[0]
        destination = route[1]
        origin_name = origin.split(',')[0]
        destination_name = destination.split(',')[0]

        earth_radius = 6370 #km
        lat1 = self.useful_data[self.useful_data['city_ascii'] == origin_name]['lat'].values[0]
        lng1 = self.useful_data[self.useful_data['city_ascii'] == origin_name]['lng'].values[0]
        lat2 = self.useful_data[self.useful_data['city_ascii'] == destination_name]['lat'].values[0]
        lng2 = self.useful_data[self.useful_data['city_ascii'] == destination_name]['lng'].values[0]

        a = math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.cos(lng1*math.pi/180)*math.cos(lng2*math.pi/180)
        b = math.cos(lat1*math.pi/180)*math.cos(lat2*math.pi/180)*math.sin(lng1*math.pi/180)*math.sin(lng2*math.pi/180)
        c = math.sin(lat1*math.pi/180)*math.sin(lat2*math.pi/180)
        distance = round(math.acos(a+b+c)*earth_radius, 2) #km

        return distance
    

if __name__ =='__main__':
    route = Route()
