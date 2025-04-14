import json
from mcp.server.fastmcp import FastMCP

server = FastMCP("finage")

from finage_mcp.api import (
    us_last_stock,
    us_agg_stock
)

@server.tool()
async def get_last_stock(symbol: str) -> str:
    """
    Get Ask, Bid, Ask Size, Bid Size and Timestamp for a US stock
    """
    data = await us_last_stock(symbol)
    return json.dumps(data)

@server.tool()
async def get_agg_stock(
    symbol: str, 
    multiply: int, 
    time_size: str, 
    from_date: str, 
    to_date: str,
) -> str:
    """
    Get OHLCVT info for a US stock
    """
    data = await us_agg_stock(
        symbol,
        multiply,
        time_size,
        from_date,
        to_date,
        )
    return json.dumps(data)

def run():
    server.run(transport='stdio')