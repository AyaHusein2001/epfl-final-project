from flask import Flask, request, redirect, session,render_template
from datetime import timedelta
from datetime import datetime
from db import db 
from models.user import User  
from models.flight import Flight  
from models.booking import Booking  

app = Flask('app')

app.secret_key = 'IloveSecurity2001'
app.permanent_session_lifetime = timedelta(days=15)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flightbookingsystem.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)  

@app.route("/")
def homepage():
    """
    This function handles the routing for the home page of the web application.
    """
    with app.app_context():
        db.create_all()
        if session:
            user_type = session['user_type']
        else:
            user_type = '1'
        all_flights = Flight.get_all_flights(user_type)
        
        
        return render_template('home.html', flights=all_flights, search=False)

@app.route("/sort")
def sortpage():
    """
    This function handles flight sort based on the flight number,takes sort type as an arguement.
    """
    
    if session:
        user_type=session['user_type']
    else:
        user_type='1'
    
    type = request.args.get('type')
    
    all_flights = Flight.get_all_flights(user_type,type)
    return render_template('home.html', flights=all_flights, search=False)



@app.route("/search")
def searchpage():
    """
    This function handles flight search based on the arrival airport .
    """
    if session:
        user_type=session['user_type']
    else:
        user_type='1'
    arrival_airport=request.args.get('q')
    flights= Flight.search_flights(arrival_airport=arrival_airport,user_type=user_type)
        
    return render_template('home.html', flights=flights, search=True)

@app.route("/about")
def aboutpage():
    """
    This function handles the routing for the about page .
    """
    return render_template('about.html')     
#-----------------------------------User-----------------------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def insertuserpage():
    """
    This function handles the routing for the signup page and the insertion of a new user into the system.
    """
    
    if request.method == 'GET':
        return render_template('signup.html')
    
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']
    address = request.form['address']
    user_type = request.form['user_type']
    employee_number = request.form['employee_number'] if request.form['employee_number'] else ''
    
    user = User(first_name, last_name, email, password, phone_number, address, user_type)
    
    user, flag = user.save_user(employee_number)
    
    # -1: wrong email , 0: not allowed to be admin , 1: signed up successfully
    if user and flag == 1:
        session.permanent = True
        session['user'] = user.user_id
        session['user_type'] = user.user_type
        
        return {"success": True, "user": user.to_dict()}
 
    elif user is None and flag == 0:
        return {"success": False, "error": "You are not authorized to be admin"}
    
    elif user is None and flag == -1:
        return {"success": False, "error": "Email already exists. Try another one."}
    
    
@app.route("/login", methods=["GET","POST"])
def loginuserpage():
    """
    This function handles the routing for the login page and the login process for users.
    """
    
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')  
    password = request.form.get('password')
    

    if email and password:
        user = User(email=email,password=password)
        user = user.login()
        if user:
            session.permanent=True
            session['user']=user.user_id
            session['user_type']=user.user_type
            return {"success": True, "user": user.to_dict()}
        else:
            return {"success": False, "error": "Invalid email or password"}
    else:
        return {"success": False, "error": "Missing email or password"}



@app.route("/logout")
def logoutpage():
    """
    This function logs out user of the web application by removing his credintials from the session.
    """
    session.pop('user',None)
    session['user_type']='1'
    return redirect('/')
    

@app.route("/addadmin",methods=['GET','POST'])
def addnewadminpage():
    """
    This function This function handles the routing for the addnewadmin page and adds a new admin
    by saving the employee number to a text file.      
    """
    if request.method == 'GET':
        return render_template('addnewadmin.html')
    
    employee_number=request.form['employee_number']
    with open('data/employeesnumbers.txt', 'r+') as file:
        employees_numbers = file.read().split('\n')
        response=''          
        if employee_number in employees_numbers:
            response=' already exists !'
        else:
            file.write(employee_number+"\n")
            response=' added successfully ! <br>He can sign up now with that employee number '
        
    return render_template('adminadded.html',employee_number=employee_number,response=response)

#-----------------------------------Flight-----------------------------------------------    
@app.route("/addflight",methods=['GET','POST'])
def insertflightpage():
    """
    This function handles the rendering of the flight addition page,
    and the insertion of a new flight into the system.        
    """
    if request.method == 'GET':
        
        return render_template('addflight.html')
    
    flight_number = request.form['flight_number']
    airplane_name = request.form['airplane_name']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time_str = request.form['departure_time']
    arrival_time_str = request.form['arrival_time']
    flight_duration = request.form['flight_duration']
    flight_price = request.form['flight_price']
    
    departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M')
    arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M')
    
    if flight_number and airplane_name and departure_airport and arrival_airport and departure_time and arrival_time and flight_duration and flight_price:
        flight = Flight(flight_number, airplane_name, departure_airport, arrival_airport.lower(), departure_time, arrival_time, flight_duration,flight_price)
        flight = flight.save_flight()
    
    if flight:
            return {"success": True}
    else:
            return {"success": False, "error": " Flight Number already exists,Try another one ."}
    


@app.route("/editflight", methods=['GET', 'POST'])
def saveeditedflightpage():
    """
    This function handles the rendering of the flight editing page, and saving of edited flight details.
    """
    if request.method == 'GET':
        flight_number = request.args.get('flight_number')
        flight = Flight.check_if_flight_exists(flight_number)
        if flight:
            
            return render_template('editflight.html', flight=flight)
        else:
            return redirect('/')
    
    
    flight_number = request.form['flight_number']
    airplane_name = request.form['airplane_name']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time_str = request.form['departure_time']
    arrival_time_str = request.form['arrival_time']
    flight_duration = request.form['flight_duration']
    flight_price = request.form['flight_price']
    
    departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M')
    arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M')
    
    if flight_number:
        flight = Flight()
        flight.edit_flight(flight_number, airplane_name, departure_airport, arrival_airport,
                           departure_time, arrival_time, flight_duration, flight_price)
    
    return redirect('/')



@app.route("/deleteflight")
def deleteflightpage():    
    """
    This function handles the deletion of a specific flight.

    """
    flight_number = request.args.get('flight_number')
    
    flight=Flight(flight_number=flight_number)
    deleted = flight.delete_flight()
    
    return redirect('/')

#-----------------------------------Booking-----------------------------------------------
@app.route("/book", methods=['GET', 'POST'])
def bookflightpage():
    """
    This function handles the routing for the flight booking page and the flight booking form submission.
    """
    if request.method == 'GET':
        flight_number = request.args.get('flight_number')  
        if not flight_number:
            return "Flight number not found!", 400 
        
        return render_template('book.html', flight_number=flight_number)

    name = request.form['name']
    age = request.form['age']
    phone_number = request.form['phone_number']
    flight_number = request.form.get('flight_number')
    user_id = session['user']

    booking = Booking(flight_number=flight_number, user_id=user_id, name=name, age=age, phone_number=phone_number)
    booking.save_booking()

    return redirect('/reservations')


@app.route("/reservations")
def reservationspage():
    """
    This function handles the routing for the user's reservations page.
    """
    user_id = session['user']
    booking = Booking(user_id=user_id)
    bookings = booking.get_bookings()
    
    return render_template('reservations.html', bookings=bookings, admin=False, search=False,flight_number='')


@app.route("/viewreservations")
def viewreservationspage():
    """
    This function handles the routing for the admin to view reservations for a specific flight.
    """
    flight_number = request.args.get('flight_number')
    
    if session:
        user_type=session['user_type']
    else:
        user_type='1'
        
    if user_type=='1':
       return redirect('/')
    
    bookings = Booking.get_bookings_of_flight(flight_number)
    
    return render_template('reservations.html', bookings=bookings, admin=True, search=False,flight_number=flight_number)



@app.route("/search-reservation")
def searchbookingpage():
    """
    This function handles the routing for searching a specific reservation by ID.
    """
    if session:
        user_type=session['user_type']
        
    else:
        user_type='1'
        
    user_id=session['user']
    id= request.args.get('q')
    
    flight_number= request.args.get('flight_number')
    
    booking=Booking(flight_number=flight_number)
    booking=booking.find_booking(id,user_type,user_id,flight_number)
    
    bookings=[booking]

        
    return render_template('reservations.html', bookings=bookings, admin=False, search=True,flight_number=flight_number)
    



@app.route("/delete-booking")
def deletebookingpage():
    """
    This function handles the deletion of a specific booking for a user.
    """
    reservation_id = request.args.get('reservation_id')
    flight_number = request.args.get('flight_number')
    
    booking=Booking(flight_number=flight_number)
    deleted = booking.delete_booking(id=reservation_id)
    if deleted:
        return redirect('/reservations')
    else:
        return 'Could not delete this reservation , try again later'