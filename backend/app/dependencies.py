from app.api import TokenData
from app.auth import validate_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

auth = HTTPBearer()


async def jwt_token_str(
    crendentials: HTTPAuthorizationCredentials = Depends(auth),
) -> str:
    """
    Dependency to extract the raw JWT token
    as a string from the Authorization header
    :param crendentials:
    :return:
    """
    token = crendentials.credentials
    return token


async def valid_jwt_token(token: str = Depends(jwt_token_str)) -> TokenData:
    """
    Check if the user is authenticated(token exists and is valid)
    and return a token object
    :param token:
    :return:
    """
    try:
        token = validate_token(token)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(403)
    return token
