from jose import jwt
from typing import Union, Any
from pydantic import ValidationError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.helpers.database import db
from app.core.config import settings
from app.models.auth import UserModel
from app.models.token import TokenPayload


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_current_user(token: str = Depends(oauth)) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        data = TokenPayload(**payload)

        if datetime.fromtimestamp(data.expiration) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get_user(username=data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any]) -> str:
    to_encode = {
        "expiration": datetime.utcnow().timestamp() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE).total_seconds(),
        "username": str(subject)
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    to_encode = {
        "expiration": datetime.utcnow().timestamp() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE).total_seconds(),
        "username": str(subject)
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def validate_refresh_token(token: str = Depends(oauth)) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        data = TokenPayload(**payload)

        if datetime.fromtimestamp(data.expiration) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get_user(username=data.username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
