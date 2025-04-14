import os
import httpx
import yaml
from typing import Any
import datetime as dt
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def parse_url(endpoint: str, *args) -> str:
    """
    Helper function to build url, e.g.
    https://api.finage.co.uk/last/stock/{symbol}?apikey=*******
    https://api.finage.co.uk/agg/stock/AAPL/1/day/2020-02-05/2020-02-07?apikey=*******
    """
    FINAGE_API_KEY = os.environ.get("FINAGE_API_KEY", "")
    FINAGE_API_BASE = os.environ.get("FINAGE_API_BASE", "")

    config_dir = Path(__file__).parent

    with open(f"{config_dir}/endpoints.yaml", "r") as f:
        endpoints = yaml.safe_load(f)

    ENDPOINT = endpoints.get(endpoint)

    if ENDPOINT:
        url = f"{FINAGE_API_BASE}{ENDPOINT}"
    else:
        raise Exception(f"Endpoint expected, {ENDPOINT} provided")
    if args:
        url += "/".join(args)
    
    url += f"?apikey={FINAGE_API_KEY}"

    return url

def epoch_to_date(epoch: int) -> str:
    return dt.datetime.fromtimestamp(epoch / 1e3, tz=dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

async def us_last_stock(symbol: str) -> dict[str, Any] | None:
    """
    Make HTTP request to finage for last stock data
    """
    url = parse_url("last-stock", symbol)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        data["date"] = epoch_to_date(data["timestamp"])
    return data

async def us_agg_stock(
        symbol: str, 
        multiply: int, 
        time_size: str, 
        from_date: str, 
        to_date: str,
        ) -> dict[str, Any] | None:
    """
    Get OHLCVT info for a US stock from finage API
    """
    url = parse_url(
        'agg-stock', 
        symbol,
        str(multiply),
        time_size,
        from_date,
        to_date
        )
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        for result in data["results"]:
            result["date"] = epoch_to_date(result["t"])
    return data