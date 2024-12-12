CREATE TABLE IF NOT EXISTS flights (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    origin_city VARCHAR(20) NOT NULL,
    dest_city VARCHAR(20) NOT NULL,
    flight_time datetime NOT NULL,
    travel_time INT,
    player_plane_id INT UNSIGNED,
    economy_ticket_price FLOAT(6,2),
    business_ticket_price FLOAT(6,2),

    FOREIGN KEY (player_plane_id) REFERENCES players_plane(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);
