from flask import current_app

class User:
    def __init__(self, name, surname,gender):
        self.name = name
        self.surname = surname
        self.gender = gender

class UserModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_all_users(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users

    def get_user_by_id(self, user_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    def add_user(self, user):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, surname, gender) VALUES (%s, %s, %s)",(user.name, user.surname, user.gender))
        self.mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id