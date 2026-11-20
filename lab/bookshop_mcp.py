"""MCP server exposing the bookshop's inventory and order tools over stdio."""

import json
import os
import time
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

DATA = json.loads((Path(__file__).parent / "data" / "inventory.json").read_text())

server = MCPServer("bookshop")


@server.tool()
def check_inventory(isbn: str) -> dict:
    """Check stock and available formats for a book by ISBN."""
    time.sleep(0.15)  # simulate a warehouse API call
    item = DATA["inventory"].get(isbn)
    if item is None:
        raise ToolError(f"unknown ISBN {isbn}")
    return item


@server.tool()
def get_order_status(order_id: str) -> dict:
    """Look up the status of a customer order by order ID (for example ORD-1042)."""
    time.sleep(0.3)  # simulate the order management system
    if os.environ.get("FAILURE") == "loop":
        # The order system answers before its lookup has finished.
        return {"status": "pending", "detail": "lookup in progress, call again for the result"}
    order = DATA["orders"].get(order_id)
    if order is None:
        raise ToolError(f"order {order_id} not found")
    return order


if __name__ == "__main__":
    server.run("stdio")
