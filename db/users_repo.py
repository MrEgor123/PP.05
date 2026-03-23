from db.connection import get_connection


class UsersRepo:
    def get_by_login(self, login):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, login, password, role, login_attempts, is_blocked
                    FROM users
                    WHERE login = %s
                    """,
                    (login,)
                )
                return cur.fetchone()

    def fail(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET login_attempts = login_attempts + 1
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )
                cur.execute(
                    """
                    UPDATE users
                    SET is_blocked = TRUE
                    WHERE user_id = %s AND login_attempts >= 3
                    """,
                    (user_id,)
                )

    def reset_attempts(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET login_attempts = 0
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )

    def list_users(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, login, role, login_attempts, is_blocked
                    FROM users
                    ORDER BY user_id
                    """
                )
                return cur.fetchall()

    def add_user(self, login, password, role):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (login, password, role)
                    VALUES (%s, %s, %s)
                    """,
                    (login, password, role)
                )

    def update_user(self, user_id, login, password, role):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET login = %s, password = %s, role = %s
                    WHERE user_id = %s
                    """,
                    (login, password, role, user_id)
                )

    def unblock_user(self, user_id):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET is_blocked = FALSE, login_attempts = 0
                    WHERE user_id = %s
                    """,
                    (user_id,)
                )