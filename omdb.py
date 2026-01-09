import time
import requests
import numpy as np
import matplotlib.pyplot as plt
from rapidfuzz import fuzz
import tkinter as tk
from tkinter import messagebox, simpledialog
import os


# =========================
# Configuration
# =========================

API_KEY = os.getenv("OMDB_API_KEY")
if not API_KEY:
    raise RuntimeError("OMDB_API_KEY environment variable is not set")
BASE_URL = "http://www.omdbapi.com/"
REQUEST_DELAY = 0.5

# =========================
# OMDb API helpers
# =========================


def search_series(query: str) -> list[dict]:
    """Search for TV series by name using OMDb."""
    params = {"apikey": API_KEY, "s": query, "type": "series"}
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("Response") == "False":
        return []
    return data.get("Search", [])


def fetch_season(imdb_id: str, season: int) -> dict:
    """Fetch episode list for a specific season."""
    params = {"apikey": API_KEY, "i": imdb_id, "Season": season}
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_all_episodes(imdb_id: str) -> list[dict]:
    """Fetch all episodes for all seasons of a series."""
    episodes = []
    first_season = fetch_season(imdb_id, 1)
    if first_season.get("Response") == "False":
        raise RuntimeError(first_season.get("Error"))

    total_seasons = int(first_season["totalSeasons"])

    for season in range(1, total_seasons + 1):
        season_data = fetch_season(imdb_id, season)
        for ep in season_data.get("Episodes", []):
            episodes.append(
                {
                    "season": season,
                    "episode": ep.get("Episode"),
                    "title": ep.get("Title"),
                    "released": ep.get("Released"),
                    "imdb_id": ep.get("imdbID"),
                    "imdb_rating": ep.get("imdbRating"),
                }
            )
        time.sleep(REQUEST_DELAY)
    return episodes


# =========================
# Visualization
# =========================


def plot_episode_heatmap(episodes: list[dict], title: str) -> None:
    """Plot a season × episode IMDb rating heatmap."""
    data = {}
    for ep in episodes:
        if ep.get("imdb_rating") in (None, "N/A"):
            continue
        try:
            season = int(ep["season"])
            episode = int(ep["episode"])
            rating = float(ep["imdb_rating"])
        except (ValueError, TypeError):
            continue
        data.setdefault(season, {})
        data[season][episode] = rating

    if not data:
        messagebox.showerror("Error", "No valid episode ratings available.")
        return

    seasons = sorted(data.keys())
    max_episode = max(max(eps.keys()) for eps in data.values())
    heatmap = np.full((len(seasons), max_episode), np.nan)

    for i, season in enumerate(seasons):
        for ep, rating in data[season].items():
            heatmap[i, ep - 1] = rating

    plt.figure(figsize=(14, 6))
    img = plt.imshow(heatmap, aspect="auto", cmap="RdYlGn", vmin=5.0, vmax=9.5)
    plt.colorbar(img, label="IMDb Rating")
    plt.yticks(range(len(seasons)), [f"Season {s}" for s in seasons])
    plt.xticks(range(max_episode), [f"E{n}" for n in range(1, max_episode + 1)])
    plt.xlabel("Episode")
    plt.ylabel("Season")
    plt.title(title)

    for i in range(len(seasons)):
        for j in range(max_episode):
            if not np.isnan(heatmap[i, j]):
                plt.text(
                    j, i, f"{heatmap[i, j]:.1f}", ha="center", va="center", fontsize=9
                )

    plt.tight_layout()
    plt.show()


# =========================
# GUI
# =========================


class SeriesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TV Series IMDb Heatmap")
        self.geometry("500x400")

        self.label = tk.Label(self, text="Enter series name:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, width=50)
        self.entry.pack(pady=5)

        self.search_button = tk.Button(self, text="Search", command=self.search_series)
        self.search_button.pack(pady=5)

        self.listbox = tk.Listbox(self, width=60)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        self.plot_button = tk.Button(
            self, text="Plot Heatmap", command=self.plot_selected
        )
        self.plot_button.pack(pady=5)

        self.series_results = []

    def search_series(self):
        query = self.entry.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a series name.")
            return

        results = search_series(query)
        if not results:
            messagebox.showinfo("No results", f"No series found for '{query}'.")
            return

        # Rank with fuzzy matching
        scored = [
            (fuzz.partial_ratio(query.lower(), r["Title"].lower()), r) for r in results
        ]
        scored.sort(reverse=True, key=lambda x: x[0])
        self.series_results = [r for _, r in scored[:10]]

        self.listbox.delete(0, tk.END)
        for r in self.series_results:
            self.listbox.insert(tk.END, f"{r['Title']} ({r['Year']})")

    def plot_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a series from the list.")
            return

        idx = selection[0]
        imdb_id = self.series_results[idx]["imdbID"]
        title = self.series_results[idx]["Title"]

        try:
            episodes = fetch_all_episodes(imdb_id)
            plot_episode_heatmap(episodes, title)
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = SeriesApp()
    app.mainloop()
