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
        player_id = cursor.lastrowid
        cursor.close()
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO game_times (player_id,game_mode_id,game_time,game_name) VALUES (%s,%s,'2024-01-01','fun_game')",(player_id,player.game_mode_id))
        self.mysql.connection.commit()
        cursor.close()
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
    def add_plane_to_player(self,plane_id,player_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("INSERT INTO players_plane ( player_id,plane_id ) VALUES (%s,%s)", (player_id, plane_id))
        self.mysql.connection.commit()
        cursor.close()

    def update_balance(self,player_id,add,amount): 
        cursor=self.mysql.connection.cursor()
        if add:
            cursor.execute("UPDATE players SET balance=balance+%s WHERE id=%s",(amount,player_id))
        else:
            cursor.execute("UPDATE players SET balance=balance-%s WHERE id=%s",(amount,player_id))
        self.mysql.connection.commit()
        cursor.close()
    def get_balance(self,player_id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT balance FROM players WHERE id=%s",(player_id,))
        balance=cursor.fetchone()
        cursor.close()
        return balance[0]
    def get_base_and_chance(self,player_id):
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM players WHERE id=%s",(player_id,))
        player=cursor.fetchone()
        cursor.close()
        cursor=self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM game_modes WHERE id=%s",(player[5],))
        game_mode=cursor.fetchone()
        base=game_mode[2]
        chance=game_mode[1]
        print(base)
        print(chance)
        return base,chance
    