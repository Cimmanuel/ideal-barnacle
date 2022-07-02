"""
Default settings/configuration used in the application are defined here.
"""

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Main configuration class for the application.
    """

    ACCESS_TOKEN_MINUTELY_EXPIRY: int = Field(
        ..., env="ACCESS_TOKEN_MINUTELY_EXPIRY"
    )
    APILAYER_API_BASE_URL: str = Field(..., env="APILAYER_API_BASE_URL")
    APILAYER_API_KEY: str = Field(..., env="APILAYER_API_KEY")
    API_VERSION: str = Field(..., env="API_VERSION")
    JWT_ALGORITHM: str = Field(..., env="JWT_ALGORITHM")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    TOKEN_URL: str = Field(..., env="TOKEN_URL")

    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


settings = Settings()
