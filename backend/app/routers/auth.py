from datetime import timedelta

from app.api import Token, TokenData, UserCreate, UserLogin
from app.auth import authenticate_user, create_access_token, get_password_hash
from app.db import SessionLocal
from app.dependencies import valid_jwt_token
from app.models import UserModel
from app.utils import create_user
from fastapi import APIRouter, Depends, HTTPException, status
from settings import conf
from sqlalchemy.orm import Session


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post(
    "/users/token",
    summary="start login flow",
    response_model=Token,
    tags=["auth"],
)
async def login_for_access_token(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    """
    API endpoint for user authentication,
    returns an authorization token to used with subsequent requests
    :param data:
    :return: access_token
    """
    user = await authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=conf.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/users/create",
    summary="create a user",
    response_model=TokenData,
    tags=["auth"],
)
async def user_create(data: UserCreate, db: Session = Depends(get_db)):
    """
    API endpoint for creating a new user and returns the username
    :param data:
    :return: usernmame
    """
    user = UserModel(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        hashed_password=get_password_hash(data.password),
    )
    user_db = await create_user(db, user)
    return TokenData(username=user_db.username)


@router.get(
    "/users/me/",
    summary="check current user",
    response_model=TokenData,
    tags=["auth"],
)
async def read_users_me(token_data: TokenData = Depends(valid_jwt_token)):
    """
    API endpoint for checking current user
    :param token:
    :return username:
    """
    return token_data
