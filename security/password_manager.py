from passlib.context import CryptContext


myctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    gets a password and returns password hashed with bcrypt
    """
    return myctx.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    gets plain password and verify with saved hash_password
    """
    return myctx.verify(plain_password, hashed_password)