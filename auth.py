from flask import Blueprint, render_template, request, redirect, session, url_for

auth_routes = Blueprint('auth', __name__)

# Dummy credentials (for testing purposes)
USERNAME = "admin"
PASSWORD = "password"

@auth_routes.route('/')
def login_page():
    return render_template('index.html')

@auth_routes.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == USERNAME and password == PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('lock.dashboard'))
    else:
        return "Invalid Credentials. Please try again."

@auth_routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_page'))
