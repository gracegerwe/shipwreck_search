from fastapi import FastAPI, Query
import requests

app = FastAPI()

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

@app.get("/wiki-summary")
@app.get("/wiki-summary")
def get_wiki_summary(query: str = Query(..., description="Shipwreck or topic name")):
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    search_resp = requests.get(WIKI_API_URL, params=search_params)
    search_data = search_resp.json()

    results = search_data["query"]["search"]
    if not results:
        return {"error": "No results found"}

    # Loop through top 5 results to find a non-disambiguation page
    for result in results[:5]:
        title = result["title"]
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title,
            "format": "json"
        }
        extract_resp = requests.get(WIKI_API_URL, params=extract_params)
        extract_data = extract_resp.json()
        page = next(iter(extract_data["query"]["pages"].values()))
        summary = page.get("extract", "")

        if "may refer to:" not in summary.lower():
            return {
                "query": query,
                "title": title,
                "summary": summary
            }

    return {
        "query": query,
        "error": "Only disambiguation pages found"
    }
