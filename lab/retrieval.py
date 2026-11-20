"""Keyword retrieval over the book catalog, standing in for a vector store."""

import json
import re
from pathlib import Path

CATALOG = json.loads((Path(__file__).parent / "data" / "catalog.json").read_text())


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def search(query: str, top_k: int = 3) -> list[tuple[dict, float]]:
    """Return the top_k catalog entries with a relevance score between 0 and 1."""
    query_tokens = _tokens(query)
    scored = []
    for book in CATALOG:
        book_tokens = _tokens(" ".join([book["title"], book["summary"], *book["topics"]]))
        overlap = len(query_tokens & book_tokens)
        if overlap:
            scored.append((book, round(overlap / len(query_tokens), 3)))
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]
