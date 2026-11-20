"""Bookshop support agent: retrieval, an LLM, and tools over MCP. No telemetry."""

import asyncio
import json
import os
import sys

from mcp import ClientSession, StdioServerParameters, stdio_client
from openai import OpenAI

import retrieval

MODEL = os.environ.get("DEMO_MODEL", "deepseek/deepseek-v4-flash")
QUESTION = (
    "I want to learn how to observe my AI agents. Which book should I buy, is it in stock, "
    "and where is my order ORD-1044?"
)
SYSTEM_PROMPT = (
    "You are a bookshop support agent. Recommend books only from the catalog excerpt you are given, "
    "use the tools to check stock and order status, and answer in at most five sentences."
)

llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
mcp_server = StdioServerParameters(command=sys.executable, args=["bookshop_mcp.py"])


async def call_tool(session: ClientSession, call) -> str:
    name, arguments = call.function.name, json.loads(call.function.arguments)
    result = await session.call_tool(name, arguments)
    return "\n".join(block.text for block in result.content if block.type == "text")


async def run(question: str) -> str:
    async with stdio_client(mcp_server) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = [
            {
                "type": "function",
                "function": {"name": t.name, "description": t.description, "parameters": t.input_schema},
            }
            for t in (await session.list_tools()).tools
        ]

        books = retrieval.search(question)
        excerpt = "\n".join(f"- {b['title']} (ISBN {b['isbn']}): {b['summary']}" for b, _ in books)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Catalog excerpt:\n{excerpt}\n\nCustomer: {question}"},
        ]

        for _ in range(5):
            response = llm.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            message = response.choices[0].message
            if not message.tool_calls:
                return message.content
            messages.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                output = await call_tool(session, call)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": output})
        return "Sorry, I could not finish that request."


if __name__ == "__main__":
    print(asyncio.run(run(QUESTION)))
