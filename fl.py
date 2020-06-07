from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from graphs import Plot
import requests, json
from datetime import datetime, date
from db_connect import DbConnection, Statistics, LocationInfo
from wtforms import Form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
from forms import validate_route, validate_form, validate_accom
import pandas as pd
import gc
import tracemalloc

tracemalloc.start()

class SessionData():
    def __init__(self, connection):
        self.connection = connection
        self.ip_address = None
        self.logged_in = False
        self.user_id = None
        self.countries_list = None
        with open('currencies.txt', 'r') as f:
            self.currency_list = f.readlines()
        self.location = None
        self.routes = None
        self.statistics = None
        self.plot = None
        self.housing = None
    
    def loggin(self, user_id):
        self.user_id = str(user_id)
        self.logged_in = True
        self.get_data()

    def logout(self):
        self.housing = None
        self.ip_address = None
        self.user_id = None
        self.countries_list = None
        self.currency_list = None
        self.location = None
        self.routes = None
        self.statistics = None
        self.user_id = None
        self.logged_in = False
        self.plot = None

    def get_data(self):
        if self.logged_in:
            self.routes = list(self.connection.get_routes(self.user_id))
            self.housing = list(self.connection.get_housing(self.user_id))
            self.statistics = Statistics(self.connection, self.user_id)
            self.plot = self.statistics.plot
            if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
                self.ip_address = request.environ['REMOTE_ADDR']
            else:
                self.ip_address = request.environ['HTTP_X_FORWARDED_FOR']
            self.location = LocationInfo(self.statistics.curr_location, self.ip_address, self.connection)
            get_metric()
            gc.collect()

        



app = Flask(__name__)

app.config['SECRET_KEY'] = '7e9755c74055db14a98f61bc7cd243aa'

db_connection = DbConnection()
db_connection.show_table()

mysession = SessionData(db_connection)
session_plot = Plot()


def format_datetime(value, period):
    if period == 'D':
        return value.strftime('%d.%m.%Y')
    elif period == 'delta':
        if value <= 0:
            return 'Expired'
        else:
            if value == 1:
                return str(value) + ' day'
            else:
                return str(value) + ' days'
    else:
        return value.strftime('%d.%m.%Y %H:%M')


def get_rate_jinja(value, currency):
    #PASS FOR NOW. REACHED API LIMIT
    return value
        


def round_number(value):
    return round(value, 2)

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['rate'] = get_rate_jinja
app.jinja_env.filters['round'] = round_number
app.jinja_env.globals['TODAY'] = datetime.now().date()


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to be logged in.')
            return redirect(url_for('login'))
    return wrap



@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('main.html', title = 'Welcomepage')


@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            if db_connection.login(request.form['username'], request.form['password']):
                session['logged_in'] = True 
                session['id'], session['username'], user_email = db_connection.get_userdata(request.form['username'])
                mysession.loggin(session['id'])
                print(mysession)
                return redirect(url_for('trips'))
            else:
                return render_template('login.html', title = 'Loginpage', invalid_data = 'Ooops. Wrong credentials. Try again.')

        except Exception as e:
            return render_template('login.html', title = 'Loginpage', invalid_data = 'Something went wrong.')
    else:
        return render_template('login.html', title = 'Loginpage')
    

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        confirm, invalids = validate_form(db_connection, request)
        if confirm:
            try:
                username = request.form['username']
                password = sha256_crypt.encrypt(str(request.form['password']))
                email = request.form['email']
                db_connection.insert_user(username, password, email)
                session['logged_in'] = True
                session['id'], session['username'], user_email = db_connection.get_userdata(username)
                mysession.loggin(session['id'])
                return redirect(url_for('trips'))

            except Exception as e:
                return render_template('register.html', title = 'Registerpage')
        else:
            session.clear()
            return render_template('register.html', title = 'Registerpage', invalids = invalids)        
    
    else:        
        return render_template('register.html', title = 'Registerpage')


@app.route('/trips/', methods = ['GET', 'POST'])
@login_required
def trips():

    if not mysession.logged_in:
            mysession.loggin(session['id'])

    if request.method == 'POST':
        
        print(request.form)
        if 'delete' in request.form:
            db_connection.delete_route(request.form['delete'])
        elif 'delete_housing' in request.form:
            db_connection.delete_housing(request.form['delete_housing'])
        elif 'country' in request.form:
            validate_accom(db_connection, request, session, mysession.location)
        else:
            validate_route(db_connection, request, session)
        mysession.get_data()

    routes = mysession.routes
    statistics = mysession.statistics
    currency_list = mysession.currency_list
    location = mysession.location
    pie_plot = mysession.plot

    return render_template('trips.html', routes = routes, statistics = statistics,
     currencies = currency_list, plot = pie_plot, location = location, title = 'Travel', mysession = mysession)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    mysession.logout()
    return redirect(url_for('login'))


@app.route('/test/', methods = ['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)

    return render_template('test.html', title = 'Test')    


@app.route('/getData/', methods = ['GET', 'POST'])
def getData():
    result = request.args.get('data')
    if request.args.get('info') == 'city':
        if len(result) > 2:
            countries_list = db_connection.get_cities_select_options(str(result))
            return json.dumps(countries_list, ensure_ascii=False, default=str)
        else:
            return None
    elif request.args.get('info') == 'country':
        if len(result) > 1:
            countries_list = db_connection.get_countries_select_options(str(result))
            return json.dumps(countries_list, ensure_ascii=False, default=str)
        else:
            return None
    else:
        return json.dumps(mysession.currency_list, ensure_ascii=False, default=str)


def get_metric():
    pass

    """ snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:10]:
        print(stat)  """ 

from test import unique_signals as uq, get_plot, get_empty_plot
@app.route('/plots/', methods = ['GET', 'POST'])
def plots():
    return render_template('plots.html', s_plot = session_plot)


@app.route('/getPlot/', methods = ['GET', 'POST'])
def getPlot():
    #result = json.loads(request.args.get('signal'))
    result = request.args.get('signal')
    print(result)
    response = session_plot.get_traces(result)
    return json.dumps(response)


if __name__ == '__main__':
    app.run(debug = True)