INSERT INTO roles (role_name) VALUES ('admin');
INSERT INTO roles (role_name) VALUES ('user');

INSERT INTO users (
    login,
    password,
    login_attempts,
    is_blocked,
    role_id,
    last_name,
    first_name,
    middle_name
) VALUES
('admin', 'password', 0, FALSE, 1, 'Админов', 'Админ', 'Админович'),
('user', 'password', 0, FALSE, 2, 'Пользов', 'Иван', 'Иванович'),
('guest', 'password', 0, FALSE, 2, 'Гостьев', 'Петр', 'Сергеевич'),
('123', '123', 3, TRUE, 2, 'Тестов', 'Тест', 'Тестович');