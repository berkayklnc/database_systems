from flask import Flask
from app import views
from app.auth import views as auth_views
from app.auth.views import logout
from app.helpers.execute_sql import setup_database
from flask_mysqldb import MySQL
from app.views import main

def create_app():
    app = Flask(__name__,template_folder='app/templates')
    app.json.ensure_ascii = False
    app.config.from_object('settings')
    app.add_url_rule('/', view_func=views.home_page)
    app.add_url_rule('/flights', view_func=views.flight_page)
    app.add_url_rule('/planes', view_func=views.plane_page)
    app.add_url_rule('/login', view_func=auth_views.login_page)
    app.add_url_rule('/login', 'login', auth_views.handle_login, methods=['POST'])
    app.add_url_rule('/register',view_func=auth_views.register_page)
    app.add_url_rule('/register','register',auth_views.handle_register,methods=['POST'])
    app.add_url_rule('/logout','logout',auth_views.logout)
    app.add_url_rule('/plane/<int:plane_id>','buy_plane', views.buy_plane)
    mysql = MySQL(app)
    app.config["mysql"] = mysql
    app.register_blueprint(main)
    with app.app_context():
        setup_database()
    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get('PORT', 8080)
    app.run(host='0.0.0.0',port=port, debug=True)