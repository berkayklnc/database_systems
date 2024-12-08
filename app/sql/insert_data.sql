INSERT INTO game_modes (id, chance, coin_multiplier, first_balance)
VALUES('EASY', 0.90, 2.0, 1000);

INSERT INTO game_modes (id, chance, coin_multiplier, first_balance)
VALUES('MEDIUM', 0.75, 1.5, 750);

INSERT INTO game_modes (id, chance, coin_multiplier, first_balance)
VALUES('HARD', 0.50, 1.0, 500);

INSERT INTO users (name, surname, gender)
VALUES ('Test', 'Test', 'male');

INSERT INTO players (balance, user_id, password, user_name)
VALUES (1500, (SELECT id FROM users WHERE name = 'Test' AND surname = 'Test'), 'scrypt:32768:8:1$IaMiHGPAYlQOvk33$1e7861e65c06baf878b0028e412c0efa019587e9d6db3b78a5ba0b378b81f08d83e42907631a668ee426c8d0437f0eab5dbc7292f7fe66cb54bfecf314abf9f0', 'Test');

