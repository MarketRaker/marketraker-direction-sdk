import requests
from fastapi import APIRouter
from decouple import config
from app.utils.MarketRaker_Functions import *
from datetime import datetime, timezone
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey


router = APIRouter()

BASE_URL = config("MARKETRAKER_API_URL")
APPLICATION_ID = config("APPLICATION_ID")
SIGNING_KEY = config("SIGNING_KEY")



@router.get("/generate_market_indicator")
async def get_market_direction():

    # Constructing the request URL
    request_url: str = f"{BASE_URL}/v1/trading_pairs/market_direction"

    # Current Unix timestamp
    current_unix_timestamp_seconds: int = int(datetime.now(timezone.utc).timestamp())

    # Concatenating the string to be signed
    string_to_sign: str = (
        f"{current_unix_timestamp_seconds}{APPLICATION_ID}"
    )

    # Sign the string using the signing key
    signing_key = SigningKey(SIGNING_KEY, encoder=HexEncoder)
    signature: str = signing_key.sign(
        string_to_sign.encode(), encoder=HexEncoder
    ).signature.decode()

    # Preparing request headers
    request_headers = {
        "X-Signature": signature,
        "X-Signature-Timestamp": str(current_unix_timestamp_seconds),
        "X-Application-Id": APPLICATION_ID,
        "Content-Type": "application/json",
    }

    # Add the intraday data to be send to the MarketRaker API here.
    # This example uses a csv file for the for modular file management. 
    # A minimum of 20 datapoints are required.
    trading_history_data = {}
    trading_history_data.update(format_to_market_direction_format("BTC_USD_Intraday_Data.csv","BTC_USD"))
    trading_history_data.update(format_to_market_direction_format("SOL_USD_Intraday_Data.csv","SOL_USD"))

    # Making a POST request to the API endpoint
    response = requests.post(
        url=request_url,
        headers=request_headers,
        json=trading_history_data,
    )

    # Parsing the response to JSON
    response_json = response.json()

    # Extracting response data
    MSG_TYPES = ["Success", "Error", "Warning", "Notice"]

    response_success: bool = response_json["success"]
    response_msg: str = response_json["msg"]
    response_msgType: str = response_json["msgType"]
    response_records: list[dict] = response_json["records"]

    # Handling the response
    if response_success and response_records:
        # Process the response records
        for record in response_records:
            # Extract the trading pair and the generated market direction
            trading_pair = record["currency"]
            market_direction = record["market_direction"]

            # Print the trading pair and the generated market direction
            print(f"{trading_pair} - Market Direction: {market_direction}")
        return response_json
    else:
        print(f"Response Message: {response_msg}")
        return response_json


