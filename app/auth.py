"""
app/auth.py — Authentication Helpers, Session Management & Password Hashing
"""
from functools import wraps
from flask import session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash a plaintext password for secure storage."""
    return generate_password_hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its stored hash."""
    return check_password_hash(hashed_password, password)

def login_required(fn):
    """Decorator to protect routes that require user authentication"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/auth/login')
        return fn(*args, **kwargs)
    return wrapper

def guest_only(fn):
    """Decorator to restrict logged-in users from viewing login/register pages"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return redirect('/dashboard/')
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    """Decorator to protect routes that require administrator privileges"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/auth/login')
        if session.get('role') != 'admin':
            flash('Unauthorized access. Administrators only.', 'error')
            return redirect('/dashboard/')
        return fn(*args, **kwargs)
    return wrapper

def login_user(user: dict) -> None:
    """
    Log a user into the active session safely.
    Handles both 'name' and 'full_name' database keys flawlessly.
    """
    session.clear()
    session['user_id'] = user.get('id')
    session['email'] = user.get('email')
    session['role'] = user.get('role', 'user')
    
    # Check for 'name' first, fall back to 'full_name', default to 'User'
    session['full_name'] = user.get('name') or user.get('full_name') or 'User'
    
    session.permanent = True

def logout_user() -> None:
    """Clear out the current session context to log out the user"""
    session.clear()