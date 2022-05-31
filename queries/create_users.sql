-- SQLite
INSERT INTO users (user_first_name, user_second_name, user_email, user_phone, user_username, user_password,user_create_date, role_id)
VALUES ('Yola','Dova','dola@gmail.com','+38032423423','dova','dova123', '2022-05-19 15:35:15',3);

DELETE FROM users WHERE users.user_id == 1;