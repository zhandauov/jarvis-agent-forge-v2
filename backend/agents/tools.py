import asyncio

import httpx
from bs4 import BeautifulSoup

WEB_TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for current information on a topic. Returns titles, URLs, and snippets.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "fetch_url",
        "description": "Fetch and read the text content of a web page by URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Full URL to fetch"}
            },
            "required": ["url"],
        },
    },
]


async def execute_tool(name: str, inputs: dict) -> str:
    if name == "web_search":
        return await _web_search(inputs["query"])
    if name == "fetch_url":
        return await _fetch_url(inputs["url"])
    return f"Unknown tool: {name}"


async def _web_search(query: str) -> str:
    def _sync_search():
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=6))

    try:
        results = await asyncio.get_event_loop().run_in_executor(None, _sync_search)
    except Exception as exc:
        return f"Search failed: {exc}"

    if not results:
        return "No results found."

    parts = [f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}" for r in results]
    return "\n\n---\n\n".join(parts)


async def _fetch_url(url: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"})
            resp.raise_for_status()
    except Exception as exc:
        return f"Failed to fetch {url}: {exc}"

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    # Trim to avoid flooding the context window
    return text[:8000] if len(text) > 8000 else text