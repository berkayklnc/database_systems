INSERT INTO users (name, surname, gender)
VALUES ('Test22', 'Test', 'male');

INSERT INTO users (name, surname, gender)
VALUES ('Test', 'Test', 'male');

INSERT INTO players (balance, user_id, password, user_name)
VALUES (1500, (SELECT id FROM users WHERE name = 'Test22' AND surname = 'Test'), 'scrypt:32768:8:1$IaMiHGPAYlQOvk33$1e7861e65c06baf878b0028e412c0efa019587e9d6db3b78a5ba0b378b81f08d83e42907631a668ee426c8d0437f0eab5dbc7292f7fe66cb54bfecf314abf9f0', 'root');


