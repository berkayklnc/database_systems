USE db_systems;
CREATE TABLE IF NOT EXISTS players(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    balance INT,
    user_id INT UNSIGNED NOT NULL,
    password VARCHAR(100) NOT NULL,
    user_name VARCHAR(15) NOT NULL,
    game_mode_id ENUM('EASY','MEDIUM','HARD') NOT NULL,
    
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_game_mode_id FOREIGN KEY (game_mode_id) REFERENCES game_modes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);