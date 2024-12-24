from flask import render_template, session, redirect, url_for, request, Blueprint,jsonify
from wtforms.fields.simple import BooleanField

from app.models.Flight import FlightModel
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wtforms import StringField, IntegerField, FloatField, DateTimeField

from app.models.Plane import PlaneModel
from app.models.Player import PlayerModel
import json
main = Blueprint('main', __name__)
@main.before_app_request
def before_request():
    if 'user_name' not in session and request.endpoint not in ['login_page','login','register_page','register','static']:
        return redirect(url_for('login'))   
def home_page():
    user_name = session.get('user_name')
    return render_template('home.html',user_name=user_name)
    
def flight_page():
    form = FlightForm()
    states = load_states()
    if request.method == "GET":
        return render_template('flights.html',states=states,form=form)
    form = FlightForm(request.form)
    flights = []
    transfered_flights=[]
    if form.validate():
        if not request.form.get('is_direct'):
            transfered_flights.extend(FlightModel().get_transfered_flights(form.origin_city.data, form.dest_city.data, form.flight_time.data))
            return jsonify(flights)
        flights.extend(FlightModel().get_direct_flights(form.origin_city.data, form.dest_city.data, form.flight_time.data))
        
        flights = [
            {
                'id': flight[0],
                'origin_city': flight[1],
                'dest_city': flight[2],
                'origin_code':flight[3],
                'dest_code':flight[4],
                'flight_time': flight[5],
                'travel_time': flight[6],
                'player_plane_id': flight[7],
                'passengers':flight[8],
                'economy_ticket_price': flight[9],
                'business_ticket_price': flight[10],
            }
            for flight in flights
        ]
    return render_template('flights.html',states=states,form=form,errors=form.errors,flights=flights)
def plane_page():
    planes = PlaneModel().get_all_planes()
    return render_template('planes.html',planes=planes)
def buy_plane(plane_id):
    plane = PlaneModel().get_plane_by_id(plane_id)
    player_id = session.get('player_id')
    PlayerModel().add_plane_to_player(plane.id,player_id)
    return redirect(url_for('plane_page'))

def load_states():
    with open('app/helpers/states.json', 'r') as file:
        states = json.load(file)
    return states
def get_states():
    filter_term = request.args.get('filter', '').lower()
    states = load_states()
    if filter_term:
        states = [state for state in states if filter_term in state.lower()]
    return states

class FlightForm(FlaskForm):
    origin_city = StringField('origin City', validators=[DataRequired(), Length(min=2, max=20)])
    dest_city = StringField('dest City', validators=[DataRequired(), Length(min=2, max=20)])
    flight_time = DateTimeField('flight Time', format='%Y-%m-%d')