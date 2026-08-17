# FastMCP is a framework for building MCP Servers with tools, prompts and resources
from json import tool
import requests

from fastmcp import FastMCP

# the name of the server
mcp = FastMCP("Math and Weather Server")


# Let's have the first tool for adding
@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together."""
    print(f"Adding {a} and {b}")
    return a + b


# now the second tool for subtracting
@mcp.tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    print(f"Subtracting {b} from {a}")
    return a - b


@mcp.tool
def weather_tool(latitude: str, longitude: str):
    """
    use this tool to get weather info for a valid city
    """
    print("Geocoordinates :" + latitude + " and  " + longitude)

    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_output = requests.get(weather_api_url)
    current_weather = weather_output.json()
    return current_weather


if __name__ == "__main__":
    # Run with HTTP transport -- remote connection is possible
    mcp.run(transport="http", host="127.0.0.1", port=9001)
    # run over stdio
    # mcp.run(transport="stdio")
