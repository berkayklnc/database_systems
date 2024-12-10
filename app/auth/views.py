from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.player import PlayerModel,Player
from app.models.User import UserModel,User

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
        if request.form['mode']=='Easy':
            balance=100000000
        elif request.form['mode']=='Medium':
            balance=50000000
        else:
            balance=25000000
        user=User(name=request.form['name'],surname=request.form['surname'],gender=request.form['gender'])
        usr=UserModel()
        last_id=usr.add_user(user=user)
        password=generate_password_hash(password=request.form['password'])
        player=Player(balance=balance,user_id=last_id,password=password,user_name=request.form['username'],game_mode_id=request.form['mode'])
        plyr.add_player(player=player)
    else:
        return render_template('auth/register.html',error=f"Username '{request.form['username']}' already exists.")
    return redirect(url_for('login'))