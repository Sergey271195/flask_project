import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, timedelta
import math






def create_plot1():

    url = "https://free.currconv.com/api/v7/convert"

    curr = 'BYN'
    host_key = '91a7c6b71f4a592e8c59'
    now = datetime.now().date()
    month = timedelta(days = 7)
    start_date = now - month
    print(now - month)

    querystring = {'q': f'{curr}_RUB,USD_{curr},EUR_{curr},JPY_{curr}',
                    'date': start_date,
                    'endDate': now,
                    "apiKey": host_key}



    response = requests.get(url, params=querystring)

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

    print(exchange_rate)

    fig.update_layout(height=600, title_text="Weekly rates", showlegend=False)

    fig.show()

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == "__main__":
    create_plot1()