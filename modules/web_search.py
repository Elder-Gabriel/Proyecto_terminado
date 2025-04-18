import requests
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def search_topic(query, num_results=5):
    if not GOOGLE_API_KEY or not GOOGLE_CSE_ID:
        print("⚠️ API de Google Search no configurada correctamente.")
        return []
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": GOOGLE_API_KEY, "cx": GOOGLE_CSE_ID, "q": query, "num": num_results}
    try:
        resp = requests.get(url, params=params)
        return resp.json().get("items", [])
    except Exception as e:
        print(f"❌ Error en búsqueda web: {e}")
        return []

