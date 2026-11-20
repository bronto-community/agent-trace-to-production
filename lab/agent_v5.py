"""Bookshop support agent, as Session 1 left it, plus what Session 2 needs.

Changes from agent_v4.py:
- the run knows which customer is asking (CUSTOMER_ID, on the run span);
- the question comes from QUESTION, so customers can ask different things;
- the run span records which tools the run called, in order (bookshop.run.tools);
- CHECKS=on adds one outcome check: did the order the agent looked up belong to this customer?
- FAILURE switches one production failure on: slow, loop, wrong (see README).
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client
from openai import OpenAI
from opentelemetry.util.genai.handler import TelemetryHandler
from opentelemetry.util.genai.types import Error, RetrievalDocument

import retrieval

MODEL = os.environ.get("DEMO_MODEL", "deepseek/deepseek-v4-flash")
FAILURE = os.environ.get("FAILURE", "")
CUSTOMER_ID = os.environ.get("CUSTOMER_ID", "cus_2291")  # owns order ORD-1043
CHECKS = os.environ.get("CHECKS") == "on"
QUESTION = os.environ.get("QUESTION") or (
    "I want to learn how to observe my AI agents. Which book should I buy, is it in stock, "
    + ("and where is my order?" if FAILURE == "wrong" else "and where is my order ORD-1043?")
)
AGENT_NAME = "bookshop-support"
SYSTEM_PROMPT = (
    "You are a bookshop support agent. Recommend books only from the catalog excerpt you are given, "
    "use the tools to check stock and order status, and answer in at most five sentences."
)
if FAILURE == "loop":
    # A product requirement someone added to the prompt. Reasonable, until the order system is slow.
    SYSTEM_PROMPT += " Never tell a customer their order is pending: keep checking until you have a final status."

llm = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["OPENROUTER_API_KEY"])
# Stdio MCP servers only inherit a small allowlist of environment variables, so pass OTEL_* explicitly.
mcp_server = StdioServerParameters(
    command=str(Path(sys.executable).with_name("opentelemetry-instrument")),
    args=[sys.executable, "bookshop_mcp.py"],
    env={k: v for k, v in os.environ.items() if k.startswith("OTEL_")}
    | {"OTEL_SERVICE_NAME": "bookshop-mcp", "FAILURE": FAILURE},
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
        if CHECKS and name == "get_order_status" and not result.is_error:
            # An outcome check: the tool answered, but was it this customer's order?
            order = json.loads(output)
            tool.attributes["bookshop.check.order_owned"] = order["customer"] == CUSTOMER_ID
        if result.is_error:
            tool.fail(Error(message=output, type="tool_error"))
        return output


async def run(question: str) -> str:
    with telemetry.invoke_local_agent(agent_name=AGENT_NAME, request_model=MODEL) as agent:
        agent.input_tokens = 0
        agent.output_tokens = 0
        agent.attributes["bookshop.llm.cost_usd"] = 0.0
        agent.attributes["bookshop.run.tools"] = ""
        agent.attributes["bookshop.customer.id"] = CUSTOMER_ID
        return await run_agent(question, agent)


def record_usage(agent, usage) -> None:
    agent.input_tokens += usage.prompt_tokens
    agent.output_tokens += usage.completion_tokens
    # OpenRouter reports what the call was billed; there is no semantic convention for cost yet.
    agent.attributes["bookshop.llm.cost_usd"] += usage.model_extra.get("cost", 0.0)


async def run_agent(question: str, agent) -> str:
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
            if FAILURE == "slow":
                time.sleep(8)  # the vector store is having a bad day
            books = retrieval.search(question, top_k=search.top_k)
            search.documents = [RetrievalDocument(id=b["isbn"], score=score) for b, score in books]
        excerpt = "\n".join(f"- {b['title']} (ISBN {b['isbn']}): {b['summary']}" for b, _ in books)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Catalog excerpt:\n{excerpt}\n\nCustomer: {question}"},
        ]

        for _ in range(5):
            response = llm.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            record_usage(agent, response.usage)
            message = response.choices[0].message
            if not message.tool_calls:
                return message.content
            messages.append(message.model_dump(exclude_none=True))
            for call in message.tool_calls:
                agent.attributes["bookshop.run.tools"] += call.function.name + " "
                output = await call_tool(session, call)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": output})
        return "Sorry, I could not finish that request."


if __name__ == "__main__":
    print(asyncio.run(run(QUESTION)))
