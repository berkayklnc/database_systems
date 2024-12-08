from datetime import datetime
from flask import render_template, jsonify

from app.models.User import UserModel,User
from app.models.Plane import PlaneModel,Plane
from app.models.Player import Player,PlayerModel
def home_page():
    user_model = UserModel()
    NewUser = User('Berkay', 'Kılınç','male')
    user_id = user_model.add_user(NewUser)    

    NewPlane=Plane('U317',120,1000000)
    NewPlayer=Player(balance=1500, user_id=user_id, password="secure123", user_name="Berkay")

    #plane_model=PlaneModel()
    
    player_model = PlayerModel()

    
    #users = user_model.get_all_users()
    #player_model.add_player(NewPlayer)
    #plane_model.add_plane(NewPlane)
    #planes=plane_model.get_all_planes()
    #players = player_model.get_all_players()   TRY AFTER GAMEMODE MODEL

    #return jsonify(players)
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template('home.html',day=day_name)
    
def flight_page():
    return render_template('flights.html')

