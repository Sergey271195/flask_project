import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

data = pd.read_csv('kc_house_data.csv')
print(data.head())

class MultLinReg():
    def __init__(self, data_x, data_y):
        self.data_x = data_x
        self.Y  = data_y
        self.n = len(self.Y)
        self.X = self.data_x.reshape((self.data_x.shape[0], 1))
        self.X = np.hstack((np.ones((1, self.n)).reshape((self.data_x.shape[0], 1)), self.X))

        print(self.X)
        print(self.X.shape[0])
        
        self.coefficients = np.zeros(self.X.shape[1])
        self.gradient_descent(20, 0.0001)

    def gradient_descent(self, steps, alpha):
        self.steps = steps
        self.alpha = alpha
        self.hypothesis = np.matmul (self.X, self.coefficients)
        self.cost_function = (0.5/self.n)*((np.subtract(self.Y, self.hypothesis)**2).sum())

        for _ in range(self.steps):
            for i in range(len(self.coefficients)):
                self.coefficients[i] = self.coefficients[i] - self.alpha * ( (1/self.n) * ((np.subtract(self.hypothesis, self.Y)*self.X[:,i]) .sum()) )
            self.hypothesis = np.matmul (self.X, self.coefficients)
            self.cost_function = (0.5/self.n)*((np.subtract(self.Y, self.hypothesis)**2).sum())
        print(self.coefficients)

    
    def predict(self, values):
        self.values = np.insert(values, 0, 1.0)
        prediction = np.matmul(self.values, self.coefficients)
        print(prediction)
        return prediction



class Linreg_grad_descent():
    def __init__(self, data_x, data_y, start_m = 0, start_b = 0):
        self.data_x = data_x
        self.X = np.vstack([np.ones((1, len(data_x))), self.data_x])
        self.data_y  = data_y
        self.start_m = start_m
        self.start_b = start_b
        self.create_cost_contour()
        self.create_hypothesis()
    

    def create_hypothesis(self):
        self.m = self.start_m
        self.b = self.start_b
        self.h = self.m*self.data_x + self.start_b
        self.cost_function = ((self.data_y - self.h)*(self.data_y - self.h)).sum()

    def create_cost_contour(self):
        n = len(self.data_x)
        self.contour = []
        for i in np.linspace(-100, 100, 101, endpoint = True):
            self.row = []
            for j in np.linspace(-6000, 6000,  2001, endpoint = True):
                cost_function = (((self.data_y - i*self.data_x-j)*(self.data_y - i*self.data_x-j)).sum())/(n*2)
                self.row.append(cost_function)
            self.contour.append(self.row)
    
    def gradient_descent(self, steps, learning_rate, plot = False):
        self.steps = steps
        self.learning_rate = learning_rate
        self.plot = plot

        self.n = len(self.data_x)

        self.animate_dict = []
        self.cost_function_dict = [self.cost_function]
        self.m_dict = [self.m]
        self.b_dict = [self.b]

        for _ in range(self.steps):   
            b_step = ((self.h - self.data_y).sum())/self.n
            m_step = (((self.h - self.data_y)*self.data_x).sum())/self.n
            self.b-=self.learning_rate*b_step
            self.m-=self.learning_rate*m_step
            self.h = self.h = self.m*self.data_x + self.b
            self.cost_function = (((self.data_y - self.h)*(self.data_y - self.h)).sum())/(self.n*2)
            self.cost_function_dict.append(self.cost_function)
            self.animate_dict.append(self.h)

        print(self.m, self.b)

        if self.plot:
            self.graph()
        
        return self.h



    def graph(self):

        fig = make_subplots(
            rows=3, cols=2,
            shared_xaxes=False,
            vertical_spacing=0.08,
            subplot_titles=("Linear regression", "Cost function"),
            specs=[[{"type": "scatter"}, {"type": "contour"}],
                [{"type": "scatter"}, {}],
                [{"type": "table"}, {}]]
)

        fig.add_trace(
            go.Scatter(x=self.data_x, y=self.h,
                     name="Linear regression",
                     mode="lines",
                     line=dict(width=2, color="red")),
                     row = 1, col =1)

        fig.add_trace(
                go.Scatter(x=self.data_x, y=self.data_y,
                            mode="markers",
                            name = 'Starting data',
                            line=dict(width=2, color="blue")),
                    row = 1, col = 1)
                    
        fig.add_trace(
                go.Scatter(x=np.array(range(self.steps)), y=self.cost_function_dict,
                            mode="lines",
                            showlegend=False,
                            line=dict(width=2, color="blue", dash = 'dot')),
                    row = 2, col = 1)

        
        
        fig.add_trace(
            go.Table(
                header=dict(
                    values=["Variance<br>", "Bias<br>", "Number of<br>Iterations", "Learning<br>Rate"],
                    line_color='darkslategray',
                    font=dict(size=15),
                    align="left"
                ),
                cells=dict(
                    values=[round(self.m,3), round(self.b,3), self.steps, self.learning_rate],
                    font=dict(size=15),
                    line_color='darkslategray',
                    height = 30,
                    align = "left")
            ),
            row=3, col=1
        )


        fig.add_trace(
                go.Contour(
                    z=self.contour,
                    x = np.linspace(-6000, 6000,  2001, endpoint = True),
                    y = np.linspace(-100,100,101, endpoint = True),
                    contours_coloring='lines',
                    line_width=2,
                    colorbar=dict(
                        thickness=25,
                        thicknessmode='pixels',
                        len=0.1)
                    ), row = 1, col = 2)

        fig.update_layout(height=1000,
                            title="Linear regression with gradient descent"
        )



        fig.show()

class Normal_equation():
    def __init__(self, data_x, data_y):
        self.X = np.vstack([data_x, np.zeros((1, len(data_x)))+1])
        self.data_y  = data_y
        self.X_T = np.transpose(self.X)
        solv = np.linalg.solve(self.data_y, self.X)
        print(solv)
        self.pseudo = np.linalg.inv(np.dot(self.X_T,self.X))
        print(self.pseudo)


if __name__ == '__main__':
    data_x = np.array(range(100))
    data_y = np.array(range(100))/4  + np.array([random.randrange(0, 1) for i in range(100)])
    multilin = MultLinReg(data_x, data_y)
    multilin.predict(np.array([20]))
    #lin = Linreg_grad_descent(data_x, data_y)
    #lin.gradient_descent(20, 0.0001, plot = False)
    """ data = np.array([0.7,20,3,11])
    data_y = data/4 + np.array([random.randrange(0, 10) for i in range(4)])
    norm = Normal_equation(data, data_y) """
        