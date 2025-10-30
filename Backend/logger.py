from DB_Util import get_connection
from datetime import datetime

def log_action(user_id, role, action, details):
    """
    Inserts a log record into the logs table.
    Called internally by all other log_* functions.
    """
    conn = get_connection()
    if not conn:
        print("[LOG ERROR] Database connection failed.")
        return

    cursor = conn.cursor()
    query = """
        INSERT INTO logs (user_id, role, action, details, timestamp)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, role, action, details, datetime.now()))
    conn.commit()
    conn.close()

def log_login(user_id, role, username):
    """Logs a successful login event."""
    details = f"User '{username}' ({role}) logged in."
    log_action(user_id, role, "LOGIN", details)
    print(f"[LOG] {details}")


def log_logout(user_id, role, username):
    """Logs a logout event."""
    details = f"User '{username}' ({role}) logged out."
    log_action(user_id, role, "LOGOUT", details)
    print(f"[LOG] {details}")

def log_failed_login(username):
    """Logs a failed login attempt (invalid username/password)."""
    conn = get_connection()
    if not conn:
        print("[LOG ERROR] Database connection failed.")
        return

    cursor = conn.cursor()
    query = """
        INSERT INTO logs (user_id, role, action, details, timestamp)
        VALUES (NULL, 'unknown', 'FAILED_LOGIN', %s, %s)
    """
    details = f"Failed login attempt for username: '{username}'"
    cursor.execute(query, (details, datetime.now()))
    conn.commit()
    conn.close()
    print(f"[LOG] {details}")

def log_view(user_id, role, username, data_viewed):
    """
    Logs whenever a user views a dataset.
    For example: viewing patient list, anonymized records, or logs.
    """
    details = f"User '{username}' ({role}) viewed: {data_viewed}"
    log_action(user_id, role, "VIEW", details)
    print(f"[LOG] {details}")
