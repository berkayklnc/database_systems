from flask import render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.Player import PlayerModel

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