# 03_client.py
# A tiny MCP CLIENT (the "waiter" from our restaurant analogy).
# It starts our server, asks what it offers, and uses it.

import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl

# How to start the server.
# sys.executable = "the same Python you are running right now",
# which avoids "wrong Python" problems on Windows.
server_params = StdioServerParameters(
    command=sys.executable,
    args=["02_full_server.py"],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            # Step 1: the handshake (the client says hello to the server)
            await session.initialize()
            print("Connected to the MCP server!\n")

            # Step 2: tools/list -> "what tools do you have?"
            print("--- TOOLS ---")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(tool.name, "->", tool.description)

            # Step 3: tools/call -> "please run this tool"
            print("\n--- CALLING get_weather for Delhi ---")
            result = await session.call_tool("get_weather", arguments={"city": "Delhi"})
            print(result.content[0].text)

            # Step 4: resources/list and resources/read
            print("\n--- RESOURCES ---")
            resources = await session.list_resources()
            for res in resources.resources:
                print(res.uri)

            content = await session.read_resource(AnyUrl("company://handbook/leave-policy"))
            print("\nReading the leave policy:")
            print(content.contents[0].text)

            # Step 5: prompts/list and prompts/get
            print("\n--- PROMPTS ---")
            prompts = await session.list_prompts()
            for p in prompts.prompts:
                print(p.name, "->", p.description)

            prompt = await session.get_prompt("review_code", arguments={"code": "x = 1 +"})
            print("\nThe prompt that was built:")
            print(prompt.messages[0].content.text)


asyncio.run(main())
