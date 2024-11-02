from flask import current_app

def execute_sql_file(filename):
    mysql = current_app.config['DB']

    with open(filename, 'r') as file:
        sql_statements = file.read()
        print(sql_statements)
        cur = mysql.connection.cursor()
        print(cur)
        for statement in sql_statements.split(';'):
            print(statement)
        try:
            for statement in sql_statements.split(';'):
                if statement.strip():
                    cur.execute(statement.strip())
            mysql.connection.commit()  # Değişiklikleri kaydet
        except Exception as e:
            mysql.connection.rollback()  # Hata durumunda geri al
            print(f"Error executing SQL statements: {e}")
        finally:
            cur.close()  # Cursor'ı kapat
def setup_database():
    with current_app.app_context():
        execute_sql_file('sql/create_database.sql')
        execute_sql_file('sql/create_users_table.sql')
        execute_sql_file('sql/create_planes_table.sql')
