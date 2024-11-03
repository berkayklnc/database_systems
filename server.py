from flask import Flask
from app import views
from app.helpers.execute_sql import setup_database
from flask_mysqldb import MySQL


def create_app():
    app = Flask(__name__,template_folder='app/templates')
    app.config.from_object('settings')
    app.add_url_rule('/', view_func=views.home_page)
    db = MySQL(app)
    app.config["DB"] = db

    with app.app_context():
        setup_database()

    return app

if __name__ == '__main__':
    app = create_app()
    port = app.config.get('PORT', 8080)
    app.run(host='0.0.0.0',port=port, debug=True)