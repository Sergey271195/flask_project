from flask import Flask, render_template, url_for, request, redirect, session, flash
import requests, json
from db_connect import DbConnection, Statistics, LocationInfo
from wtforms import Form
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
from forms import validate_route, validate_form
from search import Route
import pandas as pd
import gc
import tracemalloc

tracemalloc.start()

app = Flask(__name__)

app.config['SECRET_KEY'] = '7e9755c74055db14a98f61bc7cd243aa'

db_connection = DbConnection()
#db_connection.show_table()
#db_connection.show_trips_table()

route_data = Route()
#db_connection.insert_route(data)
#db_connection.create_table()
#db_connection.delete_user('5')

def format_datetime(value):
    return value.strftime('%d.%m.%Y %H:%M')

app.jinja_env.filters['datetime'] = format_datetime

def round_number(value):
    return round(value, 2)

app.jinja_env.filters['datetime'] = format_datetime
app.jinja_env.filters['round'] = round_number


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
    if request.method == 'POST':
        print(request.form)
        if 'delete' in request.form:
            db_connection.delete_route(request.form['delete'])
        else:
            validate_route(db_connection, request, session)
    routes = db_connection.get_routes(str(session['id']))
    statistics = Statistics(db_connection, str(session['id']))

    #countries_list =  db_connection.get_cities_select_options()
    #currency_list = open('currencies.txt', 'r')
    #location = LocationInfo(statistics.curr_location)
    #pie_plot = statistics.plot
    countries_list = None
    currency_list = None
    location = None
    get_metric()
    gc.collect()
    return render_template('trips.html', routes = routes, statistics = statistics, countries = countries_list,
     currencies = currency_list, location = location, title = 'Travel', stats = None)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/test/', methods = ['GET', 'POST'])
def test():
    if request.method == 'POST':
        print(request.form)

    return render_template('test.html', title = 'Test')    

@app.route('/getData/', methods = ['GET', 'POST'])
def getData():
    result = request.args.get('info')
    db_connection.connect()
    df = pd.read_sql_query('SELECT * FROM trips WHERE uid = (%s) ORDER BY arrival DESC', con=db_connection.connection, params = (str(session['id']), ))
    returned_json = df[df.apply(lambda row: row.astype(str).str.contains(result).any(), axis = 1)].to_json(orient = 'index')
    print(returned_json)
    
    db_connection.close()
    gc.collect()
    return json.dumps({'status':'OK','info': returned_json})


def get_metric():

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats[:10]:
        print(stat)  


if __name__ == '__main__':
    app.run(debug = True)