import requests
from datetime import datetime, timedelta
import math

""" key = 'bb83894237a0889b08dfcb5cdbf5872f'

url = 'http://data.fixer.io/api/latest'

querystring = {'access_key': key,
'base': 'BYN'}

response = requests.get(url, params = querystring)
print(response)

content = response.json()
print(content) """

url = "https://free.currconv.com/api/v7/convert"

curr = 'USD'
host_key = '91a7c6b71f4a592e8c59'
now = datetime.now().date()
month = timedelta(days = 7)
start_date = now - month
print(now - month)

querystring = {'q': f'{curr}_RUB,USD_{curr},EUR_{curr}',
                'date': start_date,
                'endDate': now,
                "apiKey": host_key}



response = requests.get(url, params=querystring)

content = response.json()
print(content)
exchange_rate = []
for value in content['results']:
    print(value)
    exchange_rate.append(content['results'][value]['val'])

#api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&date=[yyyy-mm-dd]&endDate=[yyyy-mm-dd]&apiKey=[YOUR_API_KEY]

print(exchange_rate)

