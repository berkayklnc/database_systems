USE db_systems;
CREATE TABLE IF NOT EXISTS game_modes (
    id ENUM('EASY','MEDIUM','HARD') PRIMARY KEY,
    chance FLOAT(3,2) NOT NULL CHECK(chance>0),
    coin_multiplier FLOAT,
    first_balance INT UNSIGNED 

);