INSERT INTO users (user_name, password, is_old_customer)
VALUES 
  ('testuser', 'testpassword', TRUE),
  ('testuser2', 'testpassword', FALSE),
  ('alice', 'password123', TRUE),
  ('bob', 'password456', FALSE),
  ('charlie', 'password789', FALSE);

INSERT INTO teams (team_name)
VALUES 
  ('Team A'),
  ('Team B');

INSERT INTO scores (team_id, team_name, score)
VALUES 
  (1, 'Team A', 100),
  (2, 'Team B', 50);

INSERT INTO team_members (user_id, team_id, user_name, team_name)
VALUES 
  (1, 1, 'testuser', 'Team A'),
  (2, 2, 'testuser2', 'Team B');
INSERT INTO checkins (user_id, team_id, user_name, team_name, post_url)
VALUES 
  (1, 1, 'testuser', 'Team A', 'http:1234'),
  (2, 2, 'testuser2', 'Team B', 'http:555555');
