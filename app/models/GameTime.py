from flask import current_app

class GameTime:
    def __init__(self, name, surname,gender):
        self.name = name
        self.surname = surname
        self.gender = gender

class GameTimeModel:
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_gametime(self,player_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT game_time FROM game_times WHERE player_id = %s",(player_id,))
        game_time = cursor.fetchone()
        cursor.close()
        return game_time[0]
    def update_gametime(self,player_id):
        query = """
        UPDATE game_times 
        SET game_time = (
            SELECT DATE_ADD(game_time, INTERVAL 1 DAY) 
            FROM (SELECT * FROM game_times) AS temp 
            WHERE player_id = %s
        )
        WHERE player_id = %s;
        """
        cursor = self.mysql.connection.cursor()
        cursor.execute(query, (player_id, player_id))
        self.mysql.connection.commit()
        return self.get_gametime(player_id)
        