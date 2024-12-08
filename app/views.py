from flask import current_app, render_template, session, redirect, url_for, request, Blueprint

main = Blueprint('main', __name__)
@main.before_app_request
def before_request():
    if 'user_name' not in session and request.endpoint not in ['login_page','login', 'static']:
        return redirect(url_for('login'))
def home_page():
    user_name = session.get('user_name')
    return render_template('home.html',user_name=user_name)
    
def flight_page():
    return render_template('flights.html')

