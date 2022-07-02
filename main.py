from fastapi import FastAPI, status

from auth import auth_router
from converter import converter_router
from serializers import Welcome
from settings import settings


def initialize_app():
    return FastAPI(
        version=settings.API_VERSION,
        title="Shake's Currency Converter API Assessment",
        description="This is a currency converter API assessment.",
    )


app = initialize_app()


@app.get(
    f"/{settings.API_VERSION}",
    status_code=status.HTTP_200_OK,
    summary="Welcome message",
    response_model=Welcome,
)
async def root():
    return Welcome().dict()


app.include_router(router=auth_router)
app.include_router(router=converter_router)
