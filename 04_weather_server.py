# 04_weather_server.py
# An MCP server that gets REAL weather from the internet.
# Data source: Open-Meteo (free, no API key needed).
# Weather data by Open-Meteo.com (CC BY 4.0). Free tier is for non-commercial use.
#
# IMPORTANT: Do not use print() inside an MCP server.
# Use the returned text instead. print() would corrupt the messages.

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Server")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# The weather API gives a NUMBER (a "weather code"). This table turns it into words.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Heavy drizzle",
    56: "Freezing drizzle",
    57: "Freezing drizzle",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Freezing rain",
    71: "Light snow",
    73: "Snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

# Codes where an umbrella is a good idea
WET_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}


@mcp.tool()
async def get_weather(city: str) -> str:
    """Returns the current REAL weather for a city, and whether to take an umbrella."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            # Step 1: city name -> latitude and longitude
            geo_response = await client.get(
                GEOCODING_URL, params={"name": city, "count": 1}
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if "results" not in geo_data:
                return "Sorry, I couldn't find a city called " + city

            place = geo_data["results"][0]

            # Step 2: latitude and longitude -> current weather
            weather_response = await client.get(
                FORECAST_URL,
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": "temperature_2m,weather_code,wind_speed_10m",
                    "timezone": "auto",
                },
            )
            weather_response.raise_for_status()
            current = weather_response.json()["current"]

    except httpx.HTTPError:
        return "Sorry, I couldn't reach the weather service right now."

    # Step 3: turn the numbers into a friendly sentence
    code = current["weather_code"]
    description = WEATHER_CODES.get(code, "Unknown conditions")
    umbrella = "Take an umbrella!" if code in WET_CODES else "No umbrella needed."

    return (
        f"{place['name']}, {place.get('country', '')}: {description}, "
        f"{current['temperature_2m']} degrees C, "
        f"wind {current['wind_speed_10m']} km/h. {umbrella} "
        f"(Weather data by Open-Meteo.com)"
    )


if __name__ == "__main__":
    mcp.run()
