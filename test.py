import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json



df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')
unique_signals = df['KKS'].unique()
signal = ['10LCT51CT015_XQ01']


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

def get_plot(signals):

    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')
    df2 = df.dropna(subset=['Знач'])
    print(len(df), len(df2))

    fig = make_subplots(rows=1, cols=1)
    for signal in signals:
        plot_signal = df[df["KKS"] == signal]
        plot_signal2 = df2[df2["KKS"] == signal]


        fig.add_trace(
            go.Scatter(x=plot_signal2.index, y=plot_signal2['Знач'], name = signal),
            row=1, col=1
            )

        """ fig.add_trace(
            go.Scatter(x=plot_signal2.index, y=plot_signal2['Знач'],  mode='lines', showlegend=False,
                line = {
            'dash': 'dashdot',
            'width': 2
                }),
            row=1, col=1
            ) """

        fig.update_xaxes(row=1, col=1)

    fig.update_layout(height=600, showlegend=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.show()
    return graphJSON

def get_empty_plot():

    df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')

    fig = make_subplots(rows=1, cols=1)
    '''fig.add_trace(
        go.Scatter(x=[0], y=[0], name = "Empty"),
        row=1, col=1
        )'''
    fig.update_xaxes(row=1, col=1)

    fig.update_layout(height=600, showlegend=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

if __name__ == '__main__':
    signal = ['10LCT51CT015_XQ01']
    get_plot(signal)