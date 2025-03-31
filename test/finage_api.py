import asyncio
import httpx
import os
import json
import yaml
import datetime as dt
from dotenv import load_dotenv
from typing import Any
from pathlib import Path

load_dotenv()

def parse_url(endpoint: str, *args) -> str:
    """
    Helper function to build url, e.g.
    https://api.finage.co.uk/last/stock/{symbol}?apikey=*******
    https://api.finage.co.uk/agg/stock/AAPL/1/day/2020-02-05/2020-02-07?apikey=*******
    """
    FINAGE_API_KEY = os.environ.get("FINAGE_API_KEY", "")
    FINAGE_API_BASE = os.environ.get("FINAGE_API_BASE", "")

    config_dir = Path(__file__).parents[1] / "config"

    with open(f"{config_dir}/endpoint.yaml", "r") as f:
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
    Get Ask, Bid, Ask Size, Bid Size and Timestamp for a US stock

    Args:
        symbol: The symbol of a US stock, e.g. AAPL
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
        limit: int = None,
        sort: str = None,
        dbt_filter: bool = None,
        start_time: str = None,
        end_time: str = None,
        date_format: str = None,
        ) -> dict[str, Any] | None:
    """
    Get OHLCVT info for a US stock
    o: Open Price
    h: Highest Price
    l: Lowest Price
    c: Close Price
    v: Volume
    t: Timestamp

    Parameters:
    -----------
    symbol: Symbol Name to retrieve data for.
    multiply: Time Multiplier.
    time_size: Size of the time. Options: 'minute', 'hour', 'day', 'week', 'month', 'quarter', 'year'.
    from_date: Start date.
    to_date : End date.
    limit: optional, default 100
        Limit of the results. Maximum allowed limit is 50000.
    sort : optional, default "asc"
        Sort results by timestamp.
    dbt_filter : optional, default False
        Daily-based time filter. If True, allows time filters to filter on a daily basis.
        Otherwise, the filter will only trim the start and end of the output.
    st: optional
        Start time in UTC (e.g., "17:30").
    et: optional
        End time in UTC (e.g., "17:45").
    date_format : optional, default "ts"
        Choose date format: 'dt' for datetime or 'ts' for timestamp.
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

with open(f"fiange_{dt.datetime.today().strftime('%Y-%m-%d')}.json", "w") as f:
    data = asyncio.run(
        #us_last_stock("AMZN") # AAPL
        us_agg_stock("AMZN", 1, "day", "2025-03-24", "2025-03-31")
    )
    json.dump(data, f)
