# tv_heatmap/api.py
import os
import time
import requests
from typing import List, Dict

BASE_URL = "http://www.omdbapi.com/"
REQUEST_DELAY = 0.5

API_KEY = os.getenv("OMDB_API_KEY")
if not API_KEY:
    raise RuntimeError("OMDB_API_KEY environment variable is not set")


def search_series(query: str, max_results: int = 20) -> List[Dict]:
    results = []
    page = 1

    while len(results) < max_results:
        params = {
            "apikey": API_KEY,
            "s": query,
            "type": "series",
            "page": page,
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            break

        results.extend(data.get("Search", []))
        page += 1
        time.sleep(REQUEST_DELAY)

    return results[:max_results]


def fetch_season(imdb_id: str, season: int) -> Dict:
    params = {"apikey": API_KEY, "i": imdb_id, "Season": season}
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_all_episodes(imdb_id: str) -> List[Dict]:
    episodes = []

    first = fetch_season(imdb_id, 1)
    if first.get("Response") == "False":
        raise RuntimeError(first.get("Error", "Unknown API error"))

    total_seasons = int(first["totalSeasons"])

    for season in range(1, total_seasons + 1):
        data = fetch_season(imdb_id, season)
        for ep in data.get("Episodes", []):
            episodes.append(
                {
                    "season": season,
                    "episode": ep.get("Episode"),
                    "title": ep.get("Title"),
                    "imdb_rating": ep.get("imdbRating"),
                }
            )
        time.sleep(REQUEST_DELAY)

    return episodes
