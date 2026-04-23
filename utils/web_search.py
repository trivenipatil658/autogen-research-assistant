import requests  # Used to make HTTP requests to the DuckDuckGo API
from typing import List, Dict  # Type hints for function signatures


def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """Search DuckDuckGo and return results with citations."""
    try:
        # Send a GET request to DuckDuckGo's Instant Answer API with the search query
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={
                "q": query,           # The search query (research topic)
                "format": "json",     # Request response in JSON format
                "no_html": 1,         # Strip HTML tags from the response
                "skip_disambig": 1,   # Skip disambiguation pages
            },
            timeout=10,  # Fail after 10 seconds if no response
        )
        data = resp.json()  # Parse the JSON response body
    except Exception:
        return []  # Return empty list if the request fails for any reason

    results = []  # List to collect all search result dictionaries

    # If DuckDuckGo returns a main abstract (summary), add it as the first result
    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", query),       # Use the heading or fall back to the query
            "snippet": data["AbstractText"],            # The main summary text
            "url": data.get("AbstractURL", ""),         # The source URL for the abstract
        })

    # Loop through related topics and add them as additional results
    for item in data.get("RelatedTopics", []):
        if len(results) >= max_results:  # Stop once we have enough results
            break
        # Only include items that have both text and a URL (skip group headers)
        if isinstance(item, dict) and item.get("Text") and item.get("FirstURL"):
            results.append({
                "title": item.get("Text", "")[:80],  # Truncate title to 80 characters
                "snippet": item.get("Text", ""),      # Full snippet text
                "url": item["FirstURL"],              # Direct URL to the related topic
            })

    return results  # Return the list of search result dictionaries


def format_citations(results: List[Dict]) -> str:
    # Formats the raw search results into a numbered references/citations section
    if not results:
        return ""  # Return empty string if there are no results
    lines = ["\n\n## References"]  # Start with a markdown heading
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']} — {r['url']}")  # Format each result as [n] title — url
    return "\n".join(lines)  # Join all lines into a single string


def format_search_context(results: List[Dict]) -> str:
    # Formats the raw search results into a context block to inject into the research agent's prompt
    if not results:
        return ""  # Return empty string if there are no results
    lines = ["### Web Search Results"]  # Start with a markdown heading
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['snippet']} (Source: {r['url']})")  # Format each result with its source URL
    return "\n".join(lines)  # Join all lines into a single string
