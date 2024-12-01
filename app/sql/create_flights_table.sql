CREATE TABLE IF NOT EXISTS flights (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    origin_city VARCHAR(20) NOT NULL,
    dest_city VARCHAR(20) NOT NULL,
    flight_time datetime NOT NULL,
    travel_time INT,
    plane_id INT UNSIGNED,
    player_id INT UNSIGNED,
    economy_ticket_price FLOAT(6,2),
    business_ticket_price FLOAT(6,2),
    FOREIGN KEY (player_id) REFERENCES players(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    FOREIGN KEY (plane_id) REFERENCES planes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
