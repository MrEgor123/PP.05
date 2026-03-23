INSERT INTO users (login, password, role) VALUES ('admin', 'password', 'admin');
INSERT INTO users (login, password, role) VALUES ('user', 'password', 'user');
INSERT INTO users (login, password, role, login_attempts, is_blocked)
VALUES ('guest', 'password', 'user', 3, TRUE);