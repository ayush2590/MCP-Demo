# 02_full_server.py
# The same server as before, now offering ALL THREE things
# an MCP server can expose: Tools, Resources and Prompts.
#
# Remember: no print() inside an MCP server.

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Full Server")


# ---------- TOOLS: things the AI can DO ----------

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_weather(city: str) -> str:
    """Returns the weather forecast for a city."""
    forecasts = {
        "delhi": "Rainy, 28 degrees. Take an umbrella!",
        "mumbai": "Cloudy, 31 degrees. Light rain possible.",
        "bangalore": "Sunny, 26 degrees. No umbrella needed.",
    }
    return forecasts.get(city.lower(), "Sorry, no forecast available for " + city)


# ---------- RESOURCES: things the AI can READ ----------
# A resource is identified by a URI (a unique address)

@mcp.resource("company://handbook/leave-policy")
def leave_policy() -> str:
    """The company leave policy."""
    return (
        "Leave Policy\n"
        "- 24 days of paid leave per year\n"
        "- 10 days of sick leave per year\n"
        "- Leave requests must be submitted 3 days in advance"
    )


# ---------- PROMPTS: reusable templates ----------

@mcp.prompt()
def review_code(code: str) -> str:
    """Ask the AI to review some code in simple language."""
    return (
        "Please review the code below. "
        "Explain any problems in simple language, like I am a beginner.\n\n"
        + code
    )


if __name__ == "__main__":
    mcp.run()
