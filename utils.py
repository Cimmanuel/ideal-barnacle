"""
Helper classes and functions are defined here.
"""

import re
from datetime import datetime, timedelta
from enum import Enum

import requests
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from settings import settings


class PasswordContext(object):
    def __init__(self, schemes: list = ["bcrypt"]) -> None:
        """
        Create a PassLib context to hash and verify passwords
        """

        self.password_context = CryptContext(schemes=schemes, deprecated="auto")

    def make_password(self, password: str):
        """
        Turn a plain-text password into a hash for secure storage.
        """

        return self.password_context.hash(password)

    def check_password(self, password: str, hash: str):
        """
        Return a boolean when the raw password matches the hash.
        """

        return self.password_context.verify(password, hash)


password_context = PasswordContext()


class Authentication(object):
    def __init__(self, token_url: str) -> None:
        self.token_url = token_url
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.token_url)

    def generate_access_token(self, data: dict):
        """
        Generate a new access token
        """

        secret_key = settings.SECRET_KEY
        algorithm = settings.JWT_ALGORITHM
        token_expiry = settings.ACCESS_TOKEN_MINUTELY_EXPIRY

        if not secret_key or not algorithm or not token_expiry:
            message = "Ensure that `SECRET_KEY`, `JWT_ALGORITHM` and \
                `ACCESS_TOKEN_MINUTELY_EXPIRY` are defined in the Settings class \
                    and assign a value in .env"
            raise ValueError(re.sub(" +", " ", message))

        to_encode = data.copy()
        expiry = datetime.utcnow() + timedelta(minutes=token_expiry)

        to_encode.update(
            {"exp": expiry, "iat": datetime.utcnow(), "type": "access_token"}
        )
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)


# For some weird reason, settings.TOKEN_URL keeps returning "".
# This is a workaround to use a default value of `v1/auth/token`.
token_url = settings.TOKEN_URL if settings.TOKEN_URL else "v1/auth/login"
authentication = Authentication(token_url)


class Tag(Enum):
    """
    Tags are used to categorize endpoints.
    """

    AUTH = "auth"
    CONVERTER = "converter"


class APILayer(object):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.headers = {"apikey": settings.APILAYER_API_KEY}

    def get_symbols(self) -> dict:
        """
        Get all supported currencies
        """

        response = requests.get(
            f"{self.base_url}/symbols", headers=self.headers
        )

        return {"status_code": response.status_code, "data": response.json()}

    def get_latest_rates(self) -> dict:
        """
        Get latest exchange rates
        """

        response = requests.get(f"{self.base_url}/latest", headers=self.headers)

        return {"status_code": response.status_code, "data": response.json()}

    def get_historical_rates(self, start_date: str, end_date) -> dict:
        """
        Get historical exchange rates for a certain date range
        """

        response = requests.get(
            f"{self.base_url}/timeseries?start_date={start_date}&end_date={end_date}",
            headers=self.headers,
        )

        return {"status_code": response.status_code, "data": response.json()}

    def convert_currency(
        self, amount: float, from_currency: str, to_currency: str
    ) -> dict:
        """
        Convert certain amount from one currency to another
        """

        response = requests.get(
            f"{self.base_url}/convert?from={from_currency}&to={to_currency}&amount={amount}",
            headers=self.headers,
        )

        return {"status_code": response.status_code, "data": response.json()}

    def api_error(self, response: dict) -> HTTPException:
        raise HTTPException(
            status_code=response.get("status_code"), detail=response.get("data")
        )


api_layer = APILayer(settings.APILAYER_API_BASE_URL)
