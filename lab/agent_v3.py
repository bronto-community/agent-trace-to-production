"""Bookshop support agent whose trace continues into the MCP server process."""

import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client
from openai import OpenAI
from opentelemetry.util.genai.handler import TelemetryHandler
from opentelemetry.util.genai.types import Error, RetrievalDocument

import retrieval

MODEL = os.environ.get("DEMO_MODEL", "deepseek/deepseek-v4-flash")
QUESTION = (
    "I want to learn how to observe my AI agents. Which book should I buy, is it in stock, "
    "and where is my order ORD-1044?"
)
AGENT_NAME = "bookshop-support"
SYSTEM_PROMPT = (
    "You are a bookshop support agent. Recommend books only from the catalog excerpt you are given, "
    "use the tools to check stock and order status, and answer in at most five sentences."
)

llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
# Stdio MCP servers only inherit a small allowlist of environment variables, so pass OTEL_* explicitly.
mcp_server = StdioServerParameters(
    command=str(Path(sys.executable).with_name("opentelemetry-instrument")),
    args=[sys.executable, "bookshop_mcp.py"],
    env={k: v for k, v in os.environ.items() if k.startswith("OTEL_")} | {"OTEL_SERVICE_NAME": "bookshop-mcp"},
)
telemetry = TelemetryHandler(instrumentation_scope_name="bookshop.agent", instrumentation_scope_version="0.1.0")


async def call_tool(session: ClientSession, call) -> str:
    name, arguments = call.function.name, json.loads(call.function.arguments)
    with telemetry.tool(name, tool_type="extension", agent_name=AGENT_NAME) as tool:
        tool.tool_call_id = call.id
        tool.arguments = arguments
        result = await session.call_tool(name, arguments)
        output = "\n".join(block.text for block in result.content if block.type == "text")
        tool.tool_result = output
        if result.is_error:
            tool.fail(Error(message=output, type="tool_error"))
        return output


async def run(question: str) -> str:
    with telemetry.invoke_local_agent(agent_name=AGENT_NAME, request_model=MODEL):
        return await run_agent(question)


async def run_agent(question: str) -> str:
    async with stdio_client(mcp_server) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = [
            {
                "type": "function",
                "function": {"name": t.name, "description": t.description, "parameters": t.input_schema},
            }
            for t in (await session.list_tools()).tools
        ]

        with telemetry.retrieval(data_source_id="book-catalog") as search:
            search.query_text = question
            search.top_k = 3
            books = retrieval.search(question, top_k=search.top_k)
            search.documents = [RetrievalDocument(id=b["isbn"], score=score) for b, score in books]
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
