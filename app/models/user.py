"""
app/auth.py — Authentication Helpers & Session Management
"""
from datetime import datetime, timedelta
import re
from flask import session, current_app
import werkzeug.security as security


def hash_password(password: str) -> str:
    """Securely hash a plain-text password using modern defaults."""
    return security.generate_password_hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain-text password against a hashed match from the database."""
    if not hashed:
        return False
    return security.check_password_hash(hashed, password)


def login_user(user: dict) -> None:
    """
    Log a user into the active session.
    Aligns with the updated database schema using 'name'.
    """
    session.clear()
    session['user_id'] = user.get('id')
    session['email'] = user.get('email')
    session['role'] = user.get('role', 'user')

    # Safely checks for 'name' first, falls back to 'full_name' or 'User'
    session['full_name'] = user.get('name') or user.get('full_name') or 'User'

    session.permanent = True


def logout_user() -> None:
    """Clear all session data to log out the user."""
    session.clear()


def is_authenticated() -> bool:
    """Check if a valid user session is active."""
    return 'user_id' in session


def get_current_user_id():
    """Retrieve the logged-in user's primary key ID."""
    return session.get('user_id')


def is_admin() -> bool:
    """Check if the current session belongs to an administrator."""
    return session.get('role') == 'admin'


def validate_password_strength(password: str) -> bool:
    """
    Validates password strength:
    - Minimum 8 characters
    - Contains at least one number
    - Contains at least one uppercase letter
    """
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[A-Z]", password):
        return False
    return True
