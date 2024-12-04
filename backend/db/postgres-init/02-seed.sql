INSERT INTO users (username, password, is_old_customer)
VALUES 
  ('testuser', 'testpassword', TRUE),
  ('testuser2', 'testpassword', FALSE),
  ('alice', 'password123', TRUE),
  ('bob', 'password456', FALSE),
  ('charlie', 'password789', FALSE);

INSERT INTO teams (name)
VALUES 
  ('Team A'),
  ('Team B');

INSERT INTO scores (team_id, score)
VALUES 
  (1, 100),
  (2, 50);

INSERT INTO checkins (user_id, team_id)
VALUES 
  (1, 1),
  (2, 2);
