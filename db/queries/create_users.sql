-- SQLite
INSERT INTO users (first_name, second_name, email, phone, username, password,create_date, role_id)
VALUES ('Yola','Dova','dola@gmail.com','+38032423423','dova','dova123', '2022-05-19 15:35:15',3);

DELETE FROM users WHERE users.id == 1;