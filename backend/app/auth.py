from datetime import datetime, timedelta
from typing import Optional

from app.api import TokenData
from app.utils import get_user
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from settings import conf

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_token(token: str) -> TokenData:
    """
    valid token
    raise jwt.exceptions.InvalidTokenError If token is invalid
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            conf.SECRET_KEY,
            algorithms=[conf.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token


def verify_password(plain_password, hashed_password):
    """
    verify user password
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    create a hashed password
    :param password:
    :return:
    """
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    """
    authenticate username/password
    :param username:
    :param password:
    :return:
    """
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    create an access token
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        conf.SECRET_KEY,
        algorithm=conf.ALGORITHM,
    )
    return encoded_jwt
