from flask import current_app



class Player:
    def __init__(self, balance, user_id, password, user_name):
        self.balance = balance
        self.user_id = user_id
        self.password = password
        self.user_name = user_name

class PlayerModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_all_players(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players")
        players = cursor.fetchall()
        cursor.close()
        return players

    def add_user(self, user):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, surname, gender) VALUES (%s, %s, %s)",
                       (user.name, user.surname, user.gender))
        self.mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id

    def add_player(self, player):
        user_id = self.add_user(player)
        cursor = self.mysql.connection.cursor()
        cursor.execute(f"INSERT INTO players (balance, '{user_id}', password, user_name) VALUES (%s, %s, %s, %s)", (player.balance, player.user_id, player.password,player.user_name))


