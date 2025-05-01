from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔓 allow all (change later if needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

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

            supabase.table("search_logs").insert({
                "query": query,
                "title": title,
                "summary": summary
            }).execute()

            return {
                "query": query,
                "title": title,
                "summary": summary
            }

    return {
        "query": query,
        "error": "Only disambiguation pages found"
    }
