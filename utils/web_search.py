import requests
from typing import List, Dict


def search_web(query: str, max_results: int = 5) -> List[Dict]:
    """Search DuckDuckGo and return results with citations."""
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
        )
        data = resp.json()
    except Exception:
        return []

    results = []

    if data.get("AbstractText"):
        results.append({
            "title": data.get("Heading", query),
            "snippet": data["AbstractText"],
            "url": data.get("AbstractURL", ""),
        })

    for item in data.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if isinstance(item, dict) and item.get("Text") and item.get("FirstURL"):
            results.append({
                "title": item.get("Text", "")[:80],
                "snippet": item.get("Text", ""),
                "url": item["FirstURL"],
            })

    return results


def format_citations(results: List[Dict]) -> str:
    if not results:
        return ""
    lines = ["\n\n## References"]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['title']} — {r['url']}")
    return "\n".join(lines)


def format_search_context(results: List[Dict]) -> str:
    if not results:
        return ""
    lines = ["### Web Search Results"]
    for i, r in enumerate(results, 1):
        lines.append(f"[{i}] {r['snippet']} (Source: {r['url']})")
    return "\n".join(lines)
