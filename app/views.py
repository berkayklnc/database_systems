from datetime import datetime
from flask import render_template, jsonify

from app.models.User import UserModel,User

def home_page():
    NewUser = User('Berkay', 'Kılınç','male')
    user_model = UserModel()
    #user_model.add_user(NewUser) denemek için açın sayfayı browserda güncelleyin
    users = user_model.get_all_users()
    return jsonify(users)
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template('home.html',day=day_name)