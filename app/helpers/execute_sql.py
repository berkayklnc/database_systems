from flask import current_app
from flask_mysqldb import MySQL


def execute_sql_file(filename):
    mysql = current_app.config['mysql']
    with open(filename, 'r') as file:
        sql_statements = file.read()
        cur = mysql.connection.cursor()
        try:
            for statement in sql_statements.split(';'):
                if statement.strip():
                    cur.execute(statement.strip())
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            print(f"Error executing SQL statements: {e}")
        finally:
            cur.close()
def setup_database():
        execute_sql_file('app/sql/create_database.sql')

        current_app.config['MYSQL_DB'] = 'db_systems'
        mysql = current_app.config['mysql']
        mysql.connection.select_db(current_app.config['MYSQL_DB'])

        execute_sql_file('app/sql/create_users_table.sql')
        execute_sql_file('app/sql/create_planes_table.sql')
        execute_sql_file('app/sql/create_game_mode_table.sql')
        execute_sql_file('app/sql/create_players_table.sql')
