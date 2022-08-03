from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(raw_password: str):
    return ctx.hash(raw_password)
