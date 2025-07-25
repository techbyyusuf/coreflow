from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta | None): Optional expiration time override.

    Returns:
        str: Encoded JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
