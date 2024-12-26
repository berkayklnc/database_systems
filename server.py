from flask import Flask
from app import views
from app.auth import views as auth_views
from app.auth.views import logout
from app.helpers.execute_sql import setup_database
from app.helpers.insertion import insertData
from flask_mysqldb import MySQL
from app.views import main
from flask_cors import CORS
def create_app():
    app = Flask(__name__,template_folder='app/templates',static_folder='app/static')
    CORS(app)
    app.json.ensure_ascii = False
    app.config.from_object('settings')
    app.add_url_rule('/', view_func=views.home_page)
    app.add_url_rule('/flights', view_func=views.flight_page ,methods=['GET','POST'])
    app.add_url_rule('/planes', view_func=views.plane_page)
    app.add_url_rule('/login', view_func=auth_views.login_page)
    app.add_url_rule('/login', 'login', auth_views.handle_login, methods=['POST'])
    app.add_url_rule('/register',view_func=auth_views.register_page)
    app.add_url_rule('/register','register',auth_views.handle_register,methods=['POST'])
    app.add_url_rule('/logout','logout',auth_views.logout)
    app.add_url_rule('/plane/<int:plane_id>','buy_plane', views.buy_plane)
    app.add_url_rule('/states', view_func=views.get_states)
    app.add_url_rule('/flights/add',view_func=views.add_flight)
    app.add_url_rule('/profile', view_func=views.profile_page)
    app.add_url_rule('/update_time',view_func=views.update_time,methods=['POST'])
    app.add_url_rule('/get_pause_status', 'get_pause_status', view_func=views.get_pause_status, methods=['GET'])
    app.add_url_rule('/toggle_pause', 'toggle_pause', view_func=views.toggle_pause, methods=['POST'])

    mysql = MySQL(app)
    app.config["mysql"] = mysql
    app.register_blueprint(main)
    with app.app_context():
        setup_database()
        insertData()
    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get('PORT', 8080)
    app.run(host='0.0.0.0',port=port, debug=True)