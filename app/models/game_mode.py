from flask import current_app

class GameMode:
    def __init__(self, id, chance, coin_multiplier, first_balance):
        self.id = id  # 'EASY', 'MEDIUM', or 'HARD'
        self.chance = chance
        self.coin_multiplier = coin_multiplier
        self.first_balance = first_balance

class GameModeModel:
    
    def __init__(self):
        self.mysql = current_app.config['mysql']

    def get_all_game_modes(self):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM game_modes")
        game_modes = cursor.fetchall()
        cursor.close()
        return game_modes

    def get_game_mode_by_id(self, game_mode_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("SELECT * FROM game_modes WHERE id = %s", (game_mode_id,))
        game_mode = cursor.fetchone()
        cursor.close()
        return game_mode

    def add_game_mode(self, game_mode):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO game_modes (id, chance, coin_multiplier, first_balance) VALUES (%s, %s, %s, %s)",
            (game_mode.id, game_mode.chance, game_mode.coin_multiplier, game_mode.first_balance)
        )
        self.mysql.connection.commit()
        cursor.close()
        return game_mode.id

    def update_game_mode(self, game_mode_id, updated_game_mode):
        cursor = self.mysql.connection.cursor()
        cursor.execute(
            "UPDATE game_modes SET chance = %s, coin_multiplier = %s, first_balance = %s WHERE id = %s",
            (updated_game_mode.chance, updated_game_mode.coin_multiplier, updated_game_mode.first_balance, game_mode_id)
        )
        self.mysql.connection.commit()
        cursor.close()
        return game_mode_id

    def delete_game_mode(self, game_mode_id):
        cursor = self.mysql.connection.cursor()
        cursor.execute("DELETE FROM game_modes WHERE id = %s", (game_mode_id,))
        self.mysql.connection.commit()
        cursor.close()
        return game_mode_id
