import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint 
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div

# parametry modelu

N = 38.5*10**6
beta = 0.8
gamma = 0.1

# warunki poczatkowe

S0 = 38*10**6
I0 = 10**4
R0 = 0


# definicja funkcji definiującej pochodną

def func(y, t, N, beta, gamma):
    S, I, R = y
    return -beta * S * I / N, beta * S * I / N - gamma * I, gamma * I


# tablica czasow

ts = np.linspace(0,150, 10000)


# rozwiazanie ukladu rownan z warunkami poczatkowymi
# każda kolumna to rozwiązanie dla innej zmiennej, tu w kolejności S(t), I(t), R(t)

result = odeint(func, (S0, I0, R0), ts, args=(N, beta, gamma))



fig = figure(sizing_mode='stretch_width', # rozszerzenie do odpowiedniej szerokosci
            aspect_ratio=2, # stosunek krawedzi jednej do drugiej
            title='SIR model',
            x_axis_label='time',
            y_axis_label='individuals')
fig.toolbar.logo = None # wykresy maja logo bokeh, nie chcemy tego
fig.toolbar.autohide = True # po prawej jest pasek narzedziowy pojawiajacy sie po najechaniu na wykres

fig.line(ts, result[:,0], color='blue', line_width=2, legend_label='S')
fig.line(ts, result[:,1], color='red', line_width=2, legend_label='I')
fig.line(ts, result[:,2], color='green', line_width=2, legend_label='R')

# funcje wywoluja sie w momencie zmiany parametru

def callback_I(attr, old, new):
    I0 = new * N/100
    result = odeint(func, (S0, I0, R0), ts, args=(N, beta, gamma))

    fig.renderers = []

    fig.line(ts, result[:,0], color='blue', line_width=2, legend_label='S')
    fig.line(ts, result[:,1], color='red', line_width=2, legend_label='I')
    fig.line(ts, result[:,2], color='green', line_width=2, legend_label='R')

def callback_beta(attr, old, new):
    beta = new
    result = odeint(func, (S0, I0, R0), ts, args=(N, beta, gamma))

    fig.renderers = []

    fig.line(ts, result[:,0], color='blue', line_width=2, legend_label='S')
    fig.line(ts, result[:,1], color='red', line_width=2, legend_label='I')
    fig.line(ts, result[:,2], color='green', line_width=2, legend_label='R')

def callback_gamma(attr, old, new):
    gamma = new
    result = odeint(func, (S0, I0, R0), ts, args=(N, beta, gamma))

    fig.renderers = []

    fig.line(ts, result[:,0], color='blue', line_width=2, legend_label='S')
    fig.line(ts, result[:,1], color='red', line_width=2, legend_label='I')
    fig.line(ts, result[:,2], color='green', line_width=2, legend_label='R')

def callback_N(attr, old, new):
    N = new
    result = odeint(func, (S0, I0, R0), ts, args=(N, beta, gamma))

    fig.renderers = []

    fig.line(ts, result[:,0], color='blue', line_width=2, legend_label='S')
    fig.line(ts, result[:,1], color='red', line_width=2, legend_label='I')
    fig.line(ts, result[:,2], color='green', line_width=2, legend_label='R')

slider_I = Slider(start = 0, end = 100, step = 1, value = I0/N*100, title = 'I0', sizing_mode='stretch_width') # zwiekszanie co jeden procent populacji
slider_I.on_change('value_throttled', callback_I)

slider_beta = Slider(start = 0, end = 1, step = 0.05, value = beta, title = 'beta', sizing_mode='stretch_width')
slider_beta.on_change('value_throttled', callback_beta)

slider_gamma = Slider(start = 0, end = 1, step = 0.05, value = gamma, title = 'gamma', sizing_mode='stretch_width')
slider_gamma.on_change('value_throttled', callback_gamma)

slider_N = Slider(start = 10**6, end = 38.5*10**6, step = 10**6, value = N, title = 'N', sizing_mode='stretch_width')
slider_N.on_change('value_throttled', callback_N)

curdoc().add_root( column( row( column( Div(text='Initial % of infected individuals'), row(column(slider_I, width=400)) ), column( Div(text='Probability of infection'), row(column(slider_beta, width=400)) ) ), row( column( Div(text='Total number of individuals'), row(column(slider_N, width=400)) ), column( Div(text='Probability of recovery'), row(column(slider_gamma, width=400)) ) ), row( fig, width=1000 ) ) ) 

#poetry run bokeh serve --show .\app.py





