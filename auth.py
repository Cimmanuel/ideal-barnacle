"""
Endpoints relating to authentication are defined here.
"""

import json

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from serializers import Token, User
from settings import settings
from utils import Tag, authentication, password_context

store = list()
auth_router = APIRouter(prefix=f"/{settings.API_VERSION}/auth", tags=[Tag.AUTH])


async def authenticate(email: str, password: str, store: list = store):
    return [
        user.dict()
        for user in store
        if email == user.dict()["email"]
        and password_context.check_password(password, user.dict()["password"])
    ][0]


async def invalid_credentials():
    header = {"WWW-Authenticate": "Bearer"}
    detail = {
        "code": "invalid_credentials",
        "message": "Invalid username or password",
    }

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=header
    )


async def current_user(token: str = Depends(authentication.oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise await invalid_credentials()

    user = json.loads(payload.get("sub"))
    if not user:
        raise invalid_credentials

    return user


@auth_router.post(
    "/signup",
    response_model=User,
    summary="Create a new user",
    status_code=status.HTTP_201_CREATED,
)
async def create(user: User):
    """
    Create a new user.

    - **name**: the full name of the user
    - **email**: a valid email for the user
    - **password**: a strong but easy-to-remember password

    \f
    :param user: User input
    """

    store.append(user)
    return user


@auth_router.post(
    "/login",
    response_model=Token,
    summary="Get authentication token for a user",
    status_code=status.HTTP_200_OK,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate(form_data.username, form_data.password)
    except IndexError:
        raise await invalid_credentials()

    access_token = authentication.generate_access_token(
        data={"sub": json.dumps(user, sort_keys=True, default=str)}
    )
    return Token(access_token=access_token).dict()


@auth_router.get(
    "/profile",
    response_model=User,
    summary="Retrieve profile of an authenticated user.",
    status_code=status.HTTP_200_OK,
)
async def profile(user: User = Depends(current_user)):
    """
    Retrieve profile of an authenticated user.
    """

    return user
