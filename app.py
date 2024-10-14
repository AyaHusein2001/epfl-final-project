
from flask import Flask , request,redirect,session
from components.user import User
from components.booking import Booking
from components.flight import Flight
from datetime import timedelta

app = Flask('app')
app.secret_key='IloveSecurity2001'
app.permanent_session_lifetime = timedelta(days=15)

def get_html(page_name):
    '''
    Utility function to read html page .
    '''
    html_file=open(page_name+'.html')
    content=html_file.read()
    html_file.close()
    return content

def get_flights():
    '''
    Utility function to dynamically render flights from the csv file .
    '''
    all_flights = Flight.get_all_flights('components/flights.csv')
    
    actual_flights=''
    if all_flights:
        actual_flights+="<div id='content'>"
        for flight in all_flights:
            actual_flights+='<div class="flight-card">'+'<div class="flight-card-content"> <p> Flight Number </p> <span class="flight-number">'+ flight['flight_number'] +'</span></div>'
            actual_flights+='<div class="flight-card-content"><p> Airplane Name  </p><span >'+ flight['airplane_name'] +'</span></div>'
            actual_flights+='<div class="flight-card-content"><p> Departure Airport </p><span>'+ flight['departure_airport'] +'</span></div>'
            actual_flights+='<div class="flight-card-content"><p> Arrival Airport</p> <span>'+ flight['arrival_airport'] +'</span></div>'
            actual_flights+='<div class="flight-card-content"><p> Departure Time </p><span>'+ flight['departure_time'] +'</span></div>'
            actual_flights+='<div class="flight-card-content"><p> Arrival Time </p><span>'+ flight['arrival_time'] +'</span></div>'
        
            actual_flights+='<div class="flight-card-content"><p> Flight Duration </p> <span>'+ flight['flight_duration'] +'</span></div> </div>' 
        actual_flights+="</div>"
    else:
            actual_flights+="<h1 style='padding-top: 60px; margin: 20px;'> There is no flights in the system yet !</h1>"
  
    return actual_flights


def add_bookings_to_the_page(bookings):
    '''
    Utility function to dynamically render user bookings .
    '''
    actual_bookings=''
    if bookings:
        actual_bookings+="<div id='content'>"
        for booking in bookings:
            
            actual_bookings+='<div class="flight-card">'+'<div class="flight-card-content"> <p> Flight Number </p> <span class="flight-number">'+ booking['flight_number'] +'</span></div>'
            actual_bookings+='<div class="flight-card-content"><p> Airplane Name  </p><span >'+ booking['airplane_name'] +'</span></div>'
            actual_bookings+='<div class="flight-card-content"><p> Departure Airport </p><span>'+ booking['departure_airport'] +'</span></div>'
            actual_bookings+='<div class="flight-card-content"><p> Arrival Airport</p> <span>'+ booking['arrival_airport'] +'</span></div>'
            actual_bookings+='<div class="flight-card-content"><p> Departure Time </p><span>'+ booking['departure_time'] +'</span></div>'
            actual_bookings+='<div class="flight-card-content"><p> Arrival Time </p><span>'+ booking['arrival_time'] +'</span></div>'
     
            actual_bookings+='<div class="flight-card-content"><p> Flight Duration </p> <span>'+ booking['flight_duration'] +'</span></div>' 
    
            actual_bookings+='<hr style="border: 1px solid #ccc; margin: 10px 0;">'
            actual_bookings+='<div class="flight-card-content"><p> Reservation Number :</p><span>'+ booking['reservation_id'] +'</span></div>' 
            actual_bookings+='<div class="flight-card-content"><p> Name :</p><span>'+ booking['name'] +'</span></div>' 
            actual_bookings+='<div class="flight-card-content"><p> Age : </p><span>'+ booking['age'] +'</span></div>' 
            actual_bookings+='<div class="flight-card-content"><p> Phone Number : </p><span>'+ booking['phone_number'] +'</span></div>' 
 
            actual_bookings += f"<div class='cancel-button'><a href='/delete-booking?reservation_id={booking['reservation_id']}'>Cancel</a></div></div>"
        actual_bookings+="</div>"
    else:
            actual_bookings+="<h1 style='padding-top: 60px; margin: 20px;' > You havn't booked  any flights yet , go book flights !</h1>"
         
    return actual_bookings

@app.route("/")
def homepage():
    """
    This function handles the routing for the home page of the web application.

    Route:
    - GET /

    Functionality:
    - Returns the home page HTML content.
    - The placeholder string `$$FLIGHTS$$` in the HTML template is replaced with the actual flights.
    
    """
    return get_html('Home').replace('$$FLIGHTS$$',get_flights())


@app.route("/signup")
def signuppage():
    """
    This function handles the routing for the signup page of the web application.
    Route:
    - GET /signup

    Functionality:
    - Returns the HTML content for the signup page.
    """
    
    return get_html('signup')

@app.route("/login")
def loginpage():
    """
    This function handles the routing for the login page of the web application.
    Route:
    - GET /login

    Functionality:
    - Returns the HTML content for the login page.
    """
    return get_html('login')

@app.route("/logout")
def logoutpage():
    """
    This function logs out user of the web application.
    Route:
    - GET /logout

    Functionality:
    - removes user id from the session
    """
    session.pop('user',None)
    return redirect('/')

@app.route("/book")
def bookpage():
    """
    This function handles the routing for the flight booking page of the web application.

    Route:
    - GET /book
    
    Functionality:
    - Returns the HTML content for the booking page.
    - The placeholders `$$flight_number$$` in the HTML template are replaced with the corresponding values from the request query parameters.
    """
    return get_html('book').replace('$$flight_number$$',request.args.get('flight_number'))


@app.route("/book-flight", methods=['POST'])
def bookflightpage():
    """
    This function handles the flight booking form submission.

    Route:
    - POST /book-flight

    Functionality:
    - Extracts the user details and flight information from the form submission.
    - Saves the booking details to the CSV file specified .
    - Redirects the user to the reservations page .
    
   """
    name = request.form['name']
    age = request.form['age']
    phone_number = request.form['phone_number']
    flight_number = request.form.get('flight_number')
    user_id = session['user']

    
    booking = Booking(flight_number=flight_number,user_id=user_id,name=name, age=age,phone_number=phone_number)
    booking.save_booking('components/bookings.csv')

    return redirect('/reservations')  

@app.route("/reservations")
def reservationspage():
    """
    This function handles the routing for the user's reservations page.

    Route:
    - GET /reservations

    Functionality:
    - Retrieves the user's bookings .
    - The bookings are fetched from the specified CSV files .
    - The placeholder `$$RESERVATIONS$$` in the HTML template is replaced with the user's bookings .
    """
    user_id = session['user']
    booking=Booking()
    bookings = booking.getbookings('components/bookings.csv','components/flights.csv',user_id)
    return get_html('reservations').replace('$$RESERVATIONS$$',add_bookings_to_the_page(bookings))


@app.route("/delete-booking")
def deletebookingpage():
    """
    This function handles the deletion of a specific booking for a user.

    Route:
    - GET /delete-booking

    Functionality:
    - Retrieves the  `reservation_id` from the query string.
    - Calls the `delete_booking` method of the `Booking` class to remove the booking .
    - After deleting the booking, redirects the user back to the reservations page .

    """
    reservation_id = request.args.get('reservation_id')
    
    booking=Booking()
    deleted = booking.delete_booking('components/bookings.csv',reservation_id)
    
    return redirect('/reservations') 


@app.route("/deleteflight")
def deleteflightpage():

    
    """
    This function handles the deletion of a specific flight.

    Route:
    - GET /deleteflight

    Functionality:
    - Retrieves the  `flight_number` from the query string.
    - Calls the `delete_flight` method of the `Flight` class to remove the booking .
    - After deleting the booking, redirects the user back to the home page .

    """
    flight_number = request.args.get('flight_number')
    
    flight=Flight()
    deleted = flight.delete_flight('components/flights.csv',flight_number)
    
    
    
    return redirect('/')

@app.route("/addflight")
def addflightpage():
    """
    This function handles the rendering of the flight addition page.

    Route:
    - GET /addflight

    Functionality:
    - Returns the rendered HTML content to be displayed in the user's browser.

    """
    return get_html('addflight')
    
@app.route("/editflight")
def editflightpage():
    """
    This function handles the rendering of the flight editing page.

    Route:
    - GET /editflight

    Functionality:
    - Retrieves the `flight_number` from the query string.
    - Creates an instance of the `Flight` class and retrieves the flight details .
    - Replaces placeholders in the HTML template with the actual flight details .
    - Returns the updated HTML content .

    """
    
    flight_number = request.args.get('flight_number')
    flight=Flight()
    flight= flight.get_flight('components/flights.csv',flight_number)
    editflightpage=get_html('editflight')
    
    editflightpage= editflightpage.replace('$$flight_number$$',flight.flight_number)
    editflightpage=editflightpage.replace('$$airplane_name$$',flight.airplane_name)
    editflightpage=editflightpage.replace('$$departure_airport$$',flight.departure_airport)
    editflightpage=editflightpage.replace('$$arrival_airport$$',flight.arrival_airport)
    editflightpage=editflightpage.replace('$$departure_time$$',flight.departure_time)
    editflightpage=editflightpage.replace('$$arrival_time$$',flight.arrival_time)
    editflightpage=editflightpage.replace('$$flight_duration$$',flight.flight_duration)
    return editflightpage

@app.route("/edit-flight")
def saveeditedflightpage():
    """
    This function handles the saving of edited flight details.

    Route:
    - GET /edit-flight

    Functionality:
    - Retrieves all necessary flight details from the query string.
    - If a `flight_number` is provided, update the flight details in 'components/flights.csv'.
    - After saving the changes, redirects the user to the homepage.

    """
    flight_number = request.args.get('flight_number')
    airplane_name = request.args.get('airplane_name')
    departure_airport = request.args.get('departure_airport')
    arrival_airport = request.args.get('arrival_airport')
    departure_time = request.args.get('departure_time')
    arrival_time = request.args.get('arrival_time')
    flight_duration = request.args.get('flight_duration')
    if flight_number:     
        flight=Flight()
        flight.edit_flight('components/flights.csv', flight_number, airplane_name, departure_airport, arrival_airport, departure_time, arrival_time, flight_duration)
    return redirect('/')


@app.route('/insert-user', methods=['POST'])
def insertuserpage():
    """
    This function handles the insertion of a new user into the system.

    Route:
    - POST /insert-user
    Functionality:
    - Retrieves all the user details from the form submission.
    - Attempts to save the user to the 'components/users.csv' file.
    - If the user is successfully saved, returns a success response with the user's details.
    - If the email already exists in the system, returns a failure response with an appropriate error message.
    
    """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    phone_number = request.form['phone_number']
    address = request.form['address']
    user_type = request.form['user_type']
    
    user = User(first_name, last_name, email, password, phone_number, address, user_type)
    user = user.save_user('components/users.csv')
    
    if user:
        session.permanent=True
        session['user']=user.user_id
        return {"success": True, "user": user.to_dict()}
        
    else:
        return {"success": False, "error": " Email already exists,Try another one ."}
    
    
    
    
@app.route("/insert-flight",methods=['POST'])
def insertflightpage():
    """
    This function handles the insertion of a new flight into the system.

    Route:
    - POST /insert-flight

    Functionality:
    - Retrieves all necessary flight details from the form submission.
    - Validates that all required fields (flight number, airplane name, airports, times, and duration) are provided.
    - If valid, creates a new `Flight` object and saves it to the 'components/flights.csv' file.
    - Returns a success response with the flight details if the flight is successfully saved.
    - If the flight number already exists, returns a failure response with an appropriate error message.
    
    
    """
    flight_number = request.form['flight_number']
    airplane_name = request.form['airplane_name']
    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    departure_time = request.form['departure_time']
    arrival_time = request.form['arrival_time']
    flight_duration = request.form['flight_duration']
    
    if flight_number and airplane_name and departure_airport and arrival_airport and departure_time and arrival_time and flight_duration:
        flight = Flight(flight_number, airplane_name, departure_airport, arrival_airport, departure_time, arrival_time, flight_duration)
        flight = flight.save_flight('components/flights.csv')
    
    if flight:
            return {"success": True, "flight": flight.to_dict()}
    else:
            return {"success": False, "error": " Flight Number already exists,Try another one ."}

    
@app.route("/login-user", methods=["POST"])
def loginuserpage():
    """
    This function handles the login process for users.

    Route:
    - POST /login-user

    Functionality:
    - Retrieves the user's email and password from the form data.
    - If both the email and password are provided:
        - Calls the `login` method of the `User` class to verify the credentials against the 'components/users.csv' file.
        - If the credentials match, returns a success response with the user details.
        - If the credentials are invalid, returns a failure response with an error message.
    - If either email or password is missing, returns a failure response with an appropriate error message.
    
    """
    email = request.form.get('email')  
    password = request.form.get('password')
    

    if email and password:
        user = User()
        user = user.login('components/users.csv', email, password)
        session.permanent=True
        session['user']=user.user_id
        
        
        if user:
            return {"success": True, "user": user.to_dict()}
        else:
            return {"success": False, "error": "Invalid email or password"}
    else:
        return {"success": False, "error": "Missing email or password"}

