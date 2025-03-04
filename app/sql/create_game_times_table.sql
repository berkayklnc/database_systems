CREATE TABLE IF NOT EXISTS game_times(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    player_id INT UNSIGNED NOT NULL,
    game_mode_id ENUM('EASY','MEDIUM','HARD') NOT NULL,
    game_time TIMESTAMP,
    game_name VARCHAR(30),

    FOREIGN KEY (player_id) REFERENCES players(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    FOREIGN KEY (game_mode_id) REFERENCES game_modes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);