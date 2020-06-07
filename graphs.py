import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json


class Plot():
    def __init__(self):
        self.fig = make_subplots(rows=1, cols=1)
        self.load_info()
        self.unique_signals_d = sorted([x for x in self.discret_df['KKS'].unique() if x != 'HISTORY_OFF'])
        self.unique_signals_a = sorted([x for x in self.analog_df['KKS'].unique() if x != 'HISTORY_OFF'])
        self.empty_plot = self.create_empty_plot()



    def load_info(self):
        try:
            self.df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/data.pickle')
            self.discret_df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')
            self.analog_df = pd.read_pickle('/home/sergey/Desktop/Flask/static/plots/analog.pickle')
        except Exception as error:
            parser = lambda date: datetime.strptime(date, '%d.%m.%y %H:%M:%S,%f')
            self.df = pd.read_csv('/home/sergey/Desktop/Flask/static/plots/data.txt', sep = '\t', engine = 'python', skiprows = 3, parse_dates = ['Время'], date_parser=parser)
            drop_columns = [column for column in df.columns if 'Unnamed' in column]
            self.df.drop(drop_columns, axis = 1, inplace = True)
            self.df['Знач']= pd.to_numeric(df['Знач'],errors = 'coerce')
            self.df.set_index(['Время'], inplace = True)
            self.df.to_pickle('/home/sergey/Desktop/Flask/static/plots/data.pickle')
            self.discret_df = df[df['Ед.изм'].notnull()]
            self.discret_df.to_pickle('/home/sergey/Desktop/Flask/static/plots/discret.pickle')
            self.analog_df = df[df['Ед.изм'].istnull()]
            self.analog_df.to_pickle('/home/sergey/Desktop/Flask/static/plots/analog.pickle')
            print(error)

    def create_empty_plot(self):
        self.fig.update_layout(height=700, showlegend=True, legend_orientation="h")
        graphJSON = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def add_trace(self, signal):
        plot_signal = self.discret_df[self.discret_df["KKS"] == signal]
        x = plot_signal.index
        y = plot_signal['Знач']
        self.fig.add_trace(
            go.Scatter(x=plot_signal.index, y=plot_signal['Знач'], name = signal),
            row=1, col=1
            )
        graphJSON = json.dumps(self.fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def get_traces(self, signal):
        plot_signal = self.discret_df[self.discret_df["KKS"] == signal]
        data = [go.Scatter(x=plot_signal.index, y=plot_signal['Знач'], name = signal)]
        data_json = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return data_json 