from db.connection import get_connection
import psycopg2


class UsersRepo:
    def get_by_login(self, login: str):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    u.user_id,
                    u.login,
                    u.password,
                    u.login_attempts,
                    u.is_blocked,
                    r.role_name,
                    u.last_name,
                    u.first_name,
                    u.middle_name
                FROM users u
                JOIN roles r ON r.role_id = u.role_id
                WHERE u.login = %s;
                """,
                (login,)
            )
            return cur.fetchone()

    def fail(self, user_id: int):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET login_attempts = login_attempts + 1,
                    is_blocked = (login_attempts + 1 >= 3)
                WHERE user_id = %s
                RETURNING login_attempts, is_blocked;
                """,
                (user_id,)
            )
            return cur.fetchone()

    def reset_attempts(self, user_id: int):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET login_attempts = 0
                WHERE user_id = %s;
                """,
                (user_id,)
            )

    def list_users(self):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    u.user_id,
                    u.login,
                    u.last_name,
                    u.first_name,
                    u.middle_name,
                    r.role_name,
                    u.login_attempts,
                    u.is_blocked
                FROM users u
                JOIN roles r ON r.role_id = u.role_id
                ORDER BY u.user_id;
                """
            )
            return cur.fetchall()

    def create_user(
        self,
        login: str,
        password: str,
        role_name: str,
        last_name: str,
        first_name: str,
        middle_name: str
    ):
        with get_connection() as conn, conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    INSERT INTO users (
                        login,
                        password,
                        role_id,
                        last_name,
                        first_name,
                        middle_name
                    )
                    VALUES (
                        %s,
                        %s,
                        (SELECT role_id FROM roles WHERE role_name = %s),
                        %s,
                        %s,
                        %s
                    );
                    """,
                    (login, password, role_name, last_name, first_name, middle_name)
                )
                return True
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                return False

    def update_user(
        self,
        user_id: int,
        login: str,
        role_name: str,
        password: str,
        last_name: str,
        first_name: str,
        middle_name: str
    ):
        with get_connection() as conn, conn.cursor() as cur:
            try:
                if password == "":
                    cur.execute(
                        """
                        UPDATE users
                        SET
                            login = %s,
                            role_id = (SELECT role_id FROM roles WHERE role_name = %s),
                            last_name = %s,
                            first_name = %s,
                            middle_name = %s
                        WHERE user_id = %s;
                        """,
                        (login, role_name, last_name, first_name, middle_name, user_id)
                    )
                else:
                    cur.execute(
                        """
                        UPDATE users
                        SET
                            login = %s,
                            password = %s,
                            role_id = (SELECT role_id FROM roles WHERE role_name = %s),
                            last_name = %s,
                            first_name = %s,
                            middle_name = %s
                        WHERE user_id = %s;
                        """,
                        (login, password, role_name, last_name, first_name, middle_name, user_id)
                    )
                return True
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                return False

    def unblock_user(self, user_id: int):
        with get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET is_blocked = FALSE,
                    login_attempts = 0
                WHERE user_id = %s;
                """,
                (user_id,)
            )