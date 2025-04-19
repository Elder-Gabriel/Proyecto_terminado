import requests, os
from urllib.parse import urlencode

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

def search_topic(topic: str) -> str:
    params = {"q": topic, "key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID}
    url = "https://www.googleapis.com/customsearch/v1?" + urlencode(params)
    resp = requests.get(url)
    resp.raise_for_status()
    return "\n".join(item.get("snippet", "") for item in resp.json().get("items", []))