CREATE TABLE IF NOT EXISTS players(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    balance INT,
    user_id INT UNSIGNED NOT NULL,
    password VARCHAR(256) NOT NULL,
    user_name VARCHAR(15) UNIQUE NOT NULL,
    game_mode_id ENUM('EASY','MEDIUM','HARD') NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    FOREIGN KEY (game_mode_id) REFERENCES game_modes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

ALTER TABLE players
MODIFY COLUMN balance FLOAT(10, 2);