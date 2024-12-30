from flask import render_template, session, redirect, url_for, request, Blueprint,jsonify
from wtforms.fields.simple import BooleanField

from app.models.Flight import FlightModel,Flight
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from wtforms import StringField, IntegerField, FloatField, DateTimeField

from app.models.Plane import PlaneModel
from app.models.PlayerPlane import PlayerPlaneModel
from app.models.Player import PlayerModel
from app.models.User import UserModel
from app.models.GameTime import GameTimeModel
import json
import random
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
    direct_flights = []
    transfered_flights=[]
    if form.validate():
        if not request.form.get('is_direct'):
            transfered_flights=FlightModel().get_transfered_flights(form.origin_city.data, form.dest_city.data, form.flight_time.data)
        direct_flights=FlightModel().get_direct_flights(form.origin_city.data, form.dest_city.data, form.flight_time.data)
        transfered_flights=[
            {
                'id_1':tranfered[0],
                'id_2':tranfered[1],
                'origin_city':tranfered[2],
                'transfer':tranfered[3],
                'dest_city':tranfered[4],
                'origin_code':tranfered[5],
                'dest_code':tranfered[6],
                'first_flight_time':tranfered[7],
                'second_flight_time':tranfered[8],
                'first_pp_id':tranfered[9],
                'second_pp_id':tranfered[10],
                'f1_passenger':tranfered[11],
                'f2_passenger':tranfered[12],
                'first_economy_ticket_price':tranfered[13],
                'second_economy_ticket_price':tranfered[14],
                'first_business_ticket_price':tranfered[15],
                'second_business_ticket_price':tranfered[16],
                'first_travel_time': tranfered[17],
                'second_travel_time':tranfered[18],
                'first_plane_name': tranfered[19],
                'first_plane_chair_number': tranfered[20],
                'second_plane_name': tranfered[21],
                'second_plane_chair_number': tranfered[22]
            }
            for tranfered in transfered_flights
        ]
        direct_flights = [
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
                'plane_name': flight[11],
                'chair_number': flight[12],
            }
            for flight in direct_flights
        ]
    return render_template('flights.html',states=states,form=form,errors=form.errors,direct_flights=direct_flights,transfered_flights=transfered_flights)
def plane_page(errors={}):
    planes = PlaneModel().get_all_planes()
    return render_template('planes.html',planes=planes,errors=errors)
def buy_plane(plane_id):
    plane = PlaneModel().get_plane_by_id(plane_id)
    player_id = session.get('player_id')
    balance=PlayerModel().get_balance(player_id=player_id)
    errors={}
    if balance>=plane.price:
        PlayerModel().update_balance(player_id=player_id,add=False,amount=plane.price)
        update_balance_text()
        PlayerModel().add_plane_to_player(plane.id,player_id)
    else: 
        errors={'balance': ['Is not enough']}
    return plane_page(errors=errors)

def profile_page():
    user_name = session.get('user_name')
    player=PlayerModel().get_player_by_user_name(user_name)
    user = UserModel().get_user_by_id(player.user_id)
    return render_template('profile.html',player=player,user=user)
def update_time():
    updated_time = GameTimeModel().update_gametime(session.get('player_id'))
    session['game_time'] = updated_time.strftime('%Y-%m-%d %H:%M')
    return 'success'

def get_pause_status():
    is_paused = session.get('is_paused', False)  # Varsayılan olarak False
    return jsonify({'is_paused': is_paused})

def toggle_pause():
    current_status = session.get('is_paused', False)
    new_status = not current_status
    session['is_paused'] = new_status
    return jsonify({'is_paused': new_status})

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

def myplanes_page():
    allmyplanes=PlayerPlaneModel().get_planes_by_user_id(session.get("player_id"))
    return render_template('myplanes.html',planes=allmyplanes)
def update_balance_text():
    player=PlayerModel().get_player_by_user_name(session["user_name"])
    session["player_balance"]=player.balance
def create_new_flight():
    player_id=session.get('player_id')
    player_id=int(player_id)
    origin_city=request.form.get("origin_search")
    origin_code=request.form.get("origin_code_search")
    dest_city=request.form.get("dest_search")
    dest_code=request.form.get("dest_code_search")
    departure_date=request.form.get("departure-date")
    departure_time=request.form.get("departure-time")
    economy_price=request.form.get("economy-price")
    business_price=request.form.get("business-price")
    player_plane_id=request.form.get("plane_id")
    if origin_city==None or origin_code==None or dest_city==None or dest_code==None or departure_date==None or departure_time==None or economy_price==None or business_price==None:
        return myplanes_page()
    plane_id=PlayerPlaneModel().get_plane_id(player_plane_id=player_plane_id)
    price=PlaneModel().get_plane_price(plane_id=plane_id)
    print(type(price))
    price=price/200
    PlayerModel().update_balance(player_id=player_id,add=False,amount=price)
    update_balance_text()
    flight_time=departure_date+' '+departure_time+':00'
    travel_time=random.randint(100, 300)
    my_flight=Flight(
        origin_city=origin_city,
        dest_city=dest_city,
        origin_code=origin_code,
        dest_code=dest_code,
        flight_time=flight_time,
        travel_time=travel_time,
        player_plane_id=player_plane_id,
        passengers=0,
        economy_ticket_price=economy_price,
        business_ticket_price=business_price
    )
    flight_id=FlightModel().add_flight(my_flight)
    base,chance=PlayerModel().get_base_and_chance(player_id=player_id)
    print(base)
    print(chance)
    FlightModel().fill_flight(origin_code=origin_code,dest_code=dest_code,base=base,chance=chance,flight_id=flight_id,player_id=player_id)
    update_balance_text()
    return myplanes_page()