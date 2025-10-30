import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Establish and return a MySQL database connection.
    Update the credentials to match your local MySQL setup.
    """
    try:
        conn = mysql.connector.connect(
            #add your own details
        )
        return conn
    except Error as e:
        print(f"[DB ERROR] Could not connect to MySQL: {e}")
        return None

def get_user(username):
    """
    Fetch a single user by username.
    Returns a dictionary or None if not found.
    """
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_all_users():
    """Return all users (for admin use)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_patient(name, contact, diagnosis, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO patients (name, contact, diagnosis, last_modified_by)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, contact, diagnosis, user_id))
    conn.commit()
    conn.close()


def update_patient(patient_id, name, contact, diagnosis, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE patients
        SET name = %s, contact = %s, diagnosis = %s, last_modified_by = %s
        WHERE patient_id = %s
    """
    cursor.execute(query, (name, contact, diagnosis, user_id, patient_id))
    conn.commit()
    conn.close()


def delete_patient(patient_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        DELETE FROM patients WHERE patient_id = %s
    """
    cursor.execute(query, (patient_id,))
    conn.commit()
    conn.close()


def get_all_patients():
    """Return all patient records (for admin view)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.patient_id, p.name, p.contact, p.diagnosis, p.date_added, 
               u.username AS modified_by
        FROM patients p
        LEFT JOIN users u ON p.last_modified_by = u.user_id
        ORDER BY p.patient_id DESC
    """)
    patients = cursor.fetchall()
    conn.close()
    return patients


def get_anonymized_patients():
    """Return only anonymized patient data (for doctor view)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT patient_id, anonymized_name AS name, anonymized_contact AS contact, diagnosis, date_added
        FROM patients
        ORDER BY patient_id DESC
    """)
    patients = cursor.fetchall()
    conn.close()
    return patients

def get_logs():
    """Return all logs ordered by latest first."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT log_id, user_id, role, action, timestamp, details
        FROM logs
        ORDER BY log_id DESC
    """)
    logs = cursor.fetchall()
    conn.close()
    return logs

def update_anonymized_data(patient_id, anonymized_name, anonymized_contact, user_id):
    """
    Store anonymized version of name/contact in the patients table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        UPDATE patients
        SET anonymized_name = %s,
            anonymized_contact = %s,
            last_modified_by = %s
        WHERE patient_id = %s
    """
    cursor.execute(query, (anonymized_name, anonymized_contact, user_id, patient_id))
    conn.commit()
    conn.close()