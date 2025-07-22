from passlib.context import CryptContext

myctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plain-text password.

    Returns:
        str: The hashed password.
    """
    return myctx.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain password provided by the user.
        hashed_password (str): The stored hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return myctx.verify(plain_password, hashed_password)
