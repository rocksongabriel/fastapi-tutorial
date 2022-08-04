from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str):
    """Take a raw password and return a hashed password"""
    return ctx.hash(raw_password)


def verify_password(raw_password: str, hashed_password):
    """
    Compare user's raw password to hashed_password
    and return True if they match
    """
    return ctx.verify(raw_password, hashed_password)
