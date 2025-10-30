from DB_Util import get_user
from logger import log_login, log_logout, log_failed_login

def authenticate_user(username, password):
    user = get_user(username)

    if user and user["password"] == password:
        # ✅ Successful login
        role = user["role"]
        log_login(user["user_id"], role, user["username"])

        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": role,
            "allowed_actions": get_role_permissions(role)
        }

    else:
        log_failed_login(username)
        return None

def logout_user(user):
    """Logs the logout event."""
    if user:
        log_logout(user["user_id"], user["role"], user["username"])

def get_role_permissions(role):
    role_permissions = {
        "admin": [
            "View all patient data",
            "Add new patients",
            "Edit patient records",
            "Delete patient records",
            "Anonymize patient data",
            "View system logs",
            "Export backup to CSV"
        ],
        "doctor": [
            "View anonymized patient data",
            "Add diagnosis or notes",
            "View assigned patients only"
        ],
        "receptionist": [
            "Add new patients",
            "Edit patient records (non-sensitive info only)"
        ]
    }

    return role_permissions.get(role, [])

def is_admin(user): return user and user.get("role") == "admin"
def is_doctor(user): return user and user.get("role") == "doctor"
def is_receptionist(user): return user and user.get("role") == "receptionist"