# 01_first_server.py
# Our FIRST MCP server. It offers two TOOLS (things the AI can DO).
#
# IMPORTANT: Do not use print() inside an MCP server.
# The server talks to the client through the terminal's output channel,
# so a stray print() would corrupt the messages.

from mcp.server.fastmcp import FastMCP

# 1. Create the server and give it a name
mcp = FastMCP("My First Server")


# 2. Add a tool.
#    - The function name  -> becomes the tool's "name"
#    - The docstring      -> becomes the tool's "description"
#    - The type hints     -> become the tool's "inputSchema"
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


# 3. Add a second tool (this is the "umbrella in Delhi" example from the video)
@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the weather forecast for a city."""
    # Fake data, so the demo works without internet
    forecasts = {
        "delhi": "Rainy, 28 degrees. Take an umbrella!",
        "mumbai": "Cloudy, 31 degrees. Light rain possible.",
        "bangalore": "Sunny, 26 degrees. No umbrella needed.",
    }
    return forecasts.get(city.lower(), "Sorry, no forecast available for " + city)


# 4. Start the server
if __name__ == "__main__":
    mcp.run()
