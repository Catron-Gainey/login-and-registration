from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import Person # import entire file, rather than class, to avoid circular imports
from flask_bcrypt import Bcrypt
import re 
bcrypt = Bcrypt(app)
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller
@app.route('/create', methods=['POST'])
def create_person():
    if not Person.validate_user(request.form):
        # redirect to the route where it is rendered.
        return redirect('/')
    # else no errors:
    email_data = { "email" : request.form["email"] }
    user_in_db = Person.get_by_email(email_data)
    # user is not registered in the db
    if user_in_db:
        flash("That email is already being used")
        return redirect("/")
    # create the hash
      # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    Person.save(data)
    # store user id into session
    session.update(request.form)
    return redirect("/dashboard")


# Read Users Controller
@app.route('/')
@app.route('/reg/log')
def index():
    return render_template('reg_log.html')

@app.route('/dashboard')
def show_dashboard():
    if not session:
        return redirect('/')
    print(session)
    return render_template('dashboard.html')

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = Person.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")



