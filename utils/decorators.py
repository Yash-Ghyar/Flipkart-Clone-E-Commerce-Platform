# utils/decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("You must log in first.", "warning")
            return redirect(url_for("users.login"))
        return view(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user_role = session.get("role")

            if user_role not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("home"))
            return view(*args, **kwargs)
        return wrapper
    return decorator
