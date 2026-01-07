# validators.py
import re

# Simple email regex (good enough for project)
EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email))


def is_strong_password(password: str) -> bool:
    """
    Basic rule:
    - At least 6 characters
    - You can extend later (uppercase, special char, etc.)
    """
    if not password:
        return False
    return len(password) >= 6
