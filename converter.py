"""
Endpoints relating to currency conversion are defined here.
"""

from fastapi import APIRouter, Depends, status

from auth import current_user
from serializers import Converter, HistoricalRates, User
from settings import settings
from utils import Tag, api_layer

converter_router = APIRouter(
    prefix=f"/{settings.API_VERSION}/converter", tags=[Tag.CONVERTER]
)


@converter_router.get(
    "/currencies",
    summary="Get supported currencies",
    status_code=status.HTTP_200_OK,
)
async def get_currencies():
    """
    Get all supported currencies
    """

    response = api_layer.get_symbols()
    if response.get("status_code") == status.HTTP_200_OK:
        return response.get("data")
    else:
        api_layer.api_error(response)


@converter_router.get(
    "/latest",
    summary="Get latest exchange rates",
    status_code=status.HTTP_200_OK,
)
async def get_latest_rates():
    """
    Get latest exchange rates
    """

    response = api_layer.get_latest_rates()
    if response.get("status_code") == status.HTTP_200_OK:
        return response.get("data")
    else:
        api_layer.api_error(response)


@converter_router.post(
    "/convert",
    summary="Convert certain amount from one currency to another",
    status_code=status.HTTP_200_OK,
)
async def convert_currency(
    convert: Converter, user: User = Depends(current_user)
):
    """
    Convert certain amount from one currency to another
    """

    response = api_layer.convert_currency(
        convert.amount, convert.from_currency, convert.to_currency
    )
    if response.get("status_code") == status.HTTP_200_OK:
        return response.get("data")
    else:
        api_layer.api_error(response)


@converter_router.post(
    "/historical",
    summary="Daily historical rates between two chosen dates",
    status_code=status.HTTP_200_OK,
)
async def get_historical_rates(
    dates: HistoricalRates, user: User = Depends(current_user)
):
    """
    Get historical exchange rates for a certain date range
    """

    response = api_layer.get_historical_rates(dates.start_date, dates.end_date)
    if response.get("status_code") == status.HTTP_200_OK:
        return response.get("data")
    else:
        api_layer.api_error(response)
