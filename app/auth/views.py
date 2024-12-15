from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.Player import PlayerModel,Player
from app.models.User import UserModel,User
from app.models.Game_mode import GameModeModel
def login_page():
    return render_template('auth/login.html')
def handle_login():
    user_name = request.form['username']
    player_model = PlayerModel()
    player = player_model.get_player_by_user_name(user_name)
    if not player:
        return render_template('auth/login.html', error=f"Player with username '{user_name}' does not exist.")
    is_password_correct = check_password_hash(player.password, request.form['password'])
    if is_password_correct:
        session['user_name'] = user_name
        session['player_id'] = player.id
        return redirect(url_for('home_page'))
    else:
        return render_template('auth/login.html', error="Invalid password")
def logout():
    session.pop('user_name', None)
    return redirect(url_for('login_page'))
def register_page():
    return render_template("auth/register.html")
def handle_register():
    plyr=PlayerModel()
    player=plyr.get_player_by_user_name(request.form['username'])
    if player==None:
        game_mode=GameModeModel().get_game_mode_by_id(request.form['mode'])
        user=User(name=request.form['name'],surname=request.form['surname'],gender=request.form['gender'])
        last_id=UserModel().add_user(user=user)
        password=generate_password_hash(password=request.form['password'])
        player=Player(balance=game_mode.first_balance,user_id=last_id,password=password,user_name=request.form['username'],game_mode_id=request.form['mode'])
        plyr.add_player(player=player)
    else:
        return render_template('auth/register.html',error=f"Username '{request.form['username']}' already exists.")
    return redirect(url_for('login'))