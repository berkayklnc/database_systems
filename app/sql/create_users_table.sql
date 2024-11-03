USE db_systems;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    surname VARCHAR(20) NOT NULL,
    gender ENUM('male', 'female'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
