INSERT INTO users (name, surname, gender)
VALUES ('Test22', 'Test', 'male');

INSERT INTO game_modes (id, chance, coin_multiplier, first_balance)
VALUES('EASY', 0.90, 2.0, 100000),
      ('MEDIUM', 0.75, 1.5, 75000),
      ('HARD', 0.50, 1.0, 50000);

INSERT INTO users (name, surname, gender)
VALUES ('Test', 'Test', 'male');

INSERT INTO players (balance, user_id, password, user_name)
VALUES (1500, (SELECT id FROM users WHERE name = 'Test' AND surname = 'Test'), 'scrypt:32768:8:1$IaMiHGPAYlQOvk33$1e7861e65c06baf878b0028e412c0efa019587e9d6db3b78a5ba0b378b81f08d83e42907631a668ee426c8d0437f0eab5dbc7292f7fe66cb54bfecf314abf9f0', 'Test');

INSERT INTO planes (name, chair_number, price)
VALUES
  ('Boeing 737', 180, 1000),
  ('Airbus A320', 150, 950),
  ('Boeing 747', 366, 3800),
  ('Airbus A380', 555, 4450),
  ('Embraer E190', 100, 580),
  ('Bombardier CRJ900', 76, 480),
  ('Cessna Citation X', 12, 230),
  ('Gulfstream G650', 18, 650),
  ('Concorde', 92, 1200),
  ('Boeing 777', 396, 3900);

INSERT INTO players_plane (plane_id, player_id)
Values (1, (SELECT id FROM users WHERE name = 'Test' AND surname = 'Test'));

