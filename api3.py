import requests
from datetime import datetime, timedelta
import math



url = "https://www.currency-api.com/rates"

'''curr = 'USD'
host_key = '91a7c6b71f4a592e8c59'
now = datetime.now().date()
month = timedelta(days = 7)
start_date = now - month
print(now - month)'''

'''querystring = {'q': f'{curr}_RUB,USD_{curr},EUR_{curr}',
                'date': start_date,
                'endDate': now,
                "apiKey": host_key}'''



response = requests.get(url)

content = response.json()
print(content)

