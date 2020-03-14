import pandas as pd

class Route():
    def __init__(self):
        self.data = pd.read_csv('/home/sergey/Desktop/Flask/static/worldcities.csv')
        self.sorted_data = cities.sort_values('country').reset_index()

        print(self.sorted_data)

        self.search_list = sorted_cities['city'].values
        print(len(self.search_list))

'''searched_city = 'Minsk'

searched_country_cities = (sorted_cities[sorted_cities['city'] == searched_city]).reset_index()


print(type(searched_country_cities['city'].values))

#smorgon = searched_country_cities[searched_county_cities['city'] == 'Vitsyebsk']'''
