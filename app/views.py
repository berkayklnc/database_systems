from datetime import datetime
from flask import render_template, jsonify

from app.models.User import UserModel,User
from app.models.Plane import PlaneModel,Plane

def home_page():
    NewUser = User('Berkay', 'Kılınç','male')
    NewPlane=Plane('U317',120,1000000)

    plane_model=PlaneModel()
    user_model = UserModel()

    user_model.add_user(NewUser) 
    users = user_model.get_all_users()

    plane_model.add_plane(NewPlane)
    planes=plane_model.get_all_planes()
    #return jsonify(planes)
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template('home.html',day=day_name)