from datetime import datetime
from search import Route

route_data = Route()

def turn_to_date(nums):
    dates = []
    for num in nums:
        if len(num) == 1:
            new_num = '0'+ num
        elif len(num) == 0:
            new_num = '00'
        else:
            new_num = num
        dates.append(new_num)
    separator = ':'
    departure_time = separator.join((dates[0], dates[1], '00')) 
    arrival_time = separator.join((dates[2], dates[3], '00')) 

    return departure_time, arrival_time



def validate_route(connection, request, session): 
    
    valid_route = False
    user_id = session['id']
    for el in request.form:
        print(el, ':', request.form[el])
    if any(request.form[el] == '' for el in request.form):
        return valid_route

    distance = route_data.count_miles([request.form['origin'], request.form['destination']])
    departure = datetime.strptime(request.form['departure'], '%d.%m.%Y %H:%M')
    arrival = datetime.strptime(request.form['arrival'], '%d.%m.%Y %H:%M')
    delta = arrival - departure 
    if delta.total_seconds() < 0:
        return valid_route

    #Route data for DB insertion
    insert_data = (request.form['origin'], request.form['destination'], str(departure), str(arrival), request.form['fare'], request.form['currency'],
     str(delta), str(user_id), distance)
    if connection.check_dublicate_routes(insert_data):
        return validate_route

    #Then insert
    connection.add_route(insert_data)


def validate_form(connection, request):
    username = request.form['username']
    password = request.form['password']
    confirmpassword = request.form['confirmpassword']
    email = request.form['email']
    

    confirm = False
    valid_password = valid_username = valid_email = valid_conditions = False
    invalid_password = invalid_username = invalid_email = invalid_conditions = None

    #Check username

    if len(username) == 0:
        invalid_username = 'Please enter username'
    elif len(username) in range(5, 20):
        check = connection.check_username(username)
        if not check:
            valid_username = True
        else:
            invalid_username = check
    else:
        invalid_username = 'Your username should be from 5 to 20 symbols long'

    #Check passwords

    if len(password) == 0:
        invalid_password = 'Please enter password'
    elif len(password) in range(5, 20):
        if password == confirmpassword:
            valid_password = True
        else:
            invalid_password = "Passwords don't match"
    else:
        invalid_password = 'Your password should be from 5 to 20 symbols long'

    #Check email

    if len(email) == 0:
        invalid_email = 'Please enter your email'
    elif len(email) in range(5, 20):
        valid_email = True
    else:
        invalid_email = "This email doesn't exist"

    #Check agreement to conditions
    if 'conditions' in request.form:
        valid_conditions = True
    else:
        invalid_conditions = "You should agree to our privacy police"

    if all([valid_password, valid_username, valid_email, valid_conditions]):
        confirm = True


    return (confirm, (invalid_username, invalid_password, invalid_email, invalid_conditions))