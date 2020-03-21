import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

'''try:
    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/data.pickle')
except Exception as e:
    parser = lambda date: datetime.strptime(date, '%d.%m.%y %H:%M:%S,%f')
    df = pd.read_csv('/home/sergey/Desktop/Flask/static/plots/data.txt', sep = '\t', engine = 'python', skiprows = 3, parse_dates = ['Время'], date_parser=parser)
    drop_columns = [column for column in df.columns if 'Unnamed' in column]
    df.drop(drop_columns, axis = 1, inplace = True)
    df['Знач']= pd.to_numeric(df['Знач'],errors = 'coerce')
    df.set_index(['Время'], inplace = True)
    df.to_pickle('/home/sergey/Desktop/Flask/static/plots/data.pickle')
    print(e)'''

#analog_signals = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/analog.pickle')

df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')
unique_signals = df['KKS'].unique()

def get_plots(signals):
    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')

    measure_units = df['Ед.изм'].unique()
    '''quality = df['Качество'].unique()
    valid = df['Дост'].unique()
    print(valid, len(valid))
    print(quality, len(quality))'''

    unique_signals = df['KKS'].unique()

    fig = make_subplots(rows=1, cols=1)
    for signal in unique_signals:
        plot_signal = df[df["KKS"] == signal]
        fig.add_trace(
            go.Scatter(x=plot_signal.index, y=plot_signal['Знач'], name = signal),
            row=1, col=1
            )
        fig.update_xaxes(row=1, col=1)

    fig.update_layout(title_text="Discrete Signals", showlegend=True)

    fig.show()

def get_plot(signal):

    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')

    fig = make_subplots(rows=1, cols=1)
    plot_signal = df[df["KKS"] == signal]
    print(plot_signal)
    fig.add_trace(
        go.Scatter(x=plot_signal.index, y=plot_signal['Знач'], name = signal),
        row=1, col=1
        )
    fig.update_xaxes(row=1, col=1)

    fig.update_layout(height=600, showlegend=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #fig.show()
    return graphJSON

def get_empty_plot():

    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(x=[0], y=[0], name = "Empty"),
        row=1, col=1
        )
    fig.update_xaxes(row=1, col=1)

    fig.update_layout(height=600, showlegend=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == '__main__':
    get_plots()