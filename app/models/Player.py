from flask import current_app

class Player:
    def __init__(self, balance, user_id, password, user_name,game_mode_id,id=0):
        self.id = id
        self.balance = balance
        self.user_id = user_id
        self.password = password
        self.user_name = user_name
        self.game_mode_id = game_mode_id

class PlayerModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_all_players(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players")
        players = cursor.fetchall()
        cursor.close()
        return players

    def add_player(self, player):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO players (balance, user_id, password, user_name, game_mode_id) VALUES (%s, %s, %s, %s,%s)", (player.balance, player.user_id, player.password,player.user_name,player.game_mode_id))
        self.mysql.connection.commit()
    def get_player_by_user_name(self, user_name):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players WHERE user_name=%s", (user_name,))
        player = cursor.fetchone()
        cursor.close()
        if player:
            player = Player( player[1], player[2], player[3],player[4],player[5],player[0])
            return player
        else:
            return None