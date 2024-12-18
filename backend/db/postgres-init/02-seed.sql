INSERT INTO users (user_name, password, is_old_customer, last_update)
VALUES 
  ('testuser', 'testpassword', TRUE, '2023-12-15'),
  ('testuser2', 'testpassword', FALSE, '2023-12-02'),
  ('alice', 'password123', TRUE, '2023-12-02'),
  ('bob', 'password456', FALSE, '2023-12-02'),
  ('charlie', 'password789', FALSE, '2023-12-02'),
  ('澤哥', '123', FALSE, '2023-12-12');


INSERT INTO teams (team_name)
VALUES 
  ('Team A'),
  ('Team B'),
  ('莊家軍'),
  ('披薩派對'),
  ('星星幫');

INSERT INTO team_members (user_id, team_id, user_name, team_name)
VALUES 
  (1, 1, 'testuser', 'Team A'),
  (2, 2, 'testuser2', 'Team B'),
  (6, 2, '澤哥', 'Team B'),
  (1, 3, 'testuser', '莊家軍'),
  (2, 3, 'testuser2', '莊家軍'),
  (3, 3, 'alice', '莊家軍'),
  (4, 3, 'bob', '莊家軍'),
  (5, 3, 'charlie', '莊家軍'),
  (6, 3, '澤哥', '莊家軍');
INSERT INTO checkins (user_id, user_name, content, timestamp)
VALUES 
  (1, 'testuser', 'today 1202 is a good day', '2024-12-02'),
  (2, 'testuser2', 'hi everyone I am testuser2', '2024-12-02'),
  (1, 'testuser', 'today 1215 is another good day', '2024-12-15'),
  (6, '澤哥', '刀下留人', '2024-12-12');

INSERT INTO scores (team_id, team_name, score)
VALUES 
  (1, 'Team A', 6),
  (2, 'Team B', 7),
  (3, '莊家軍', 60),
  (4, '披薩派對', 0),
  (5, '星星幫', 0);

