# tv_heatmap/plotting.py
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict


def plot_episode_heatmap(episodes: List[Dict], title: str) -> None:
    data = {}

    for ep in episodes:
        try:
            season = int(ep["season"])
            episode = int(ep["episode"])
            rating = float(ep["imdb_rating"])
        except (TypeError, ValueError):
            continue

        data.setdefault(season, {})
        data[season][episode] = rating

    if not data:
        raise ValueError("No valid episode ratings available")

    seasons = sorted(data.keys())
    max_episode = max(max(eps) for eps in data.values())

    heatmap = np.full((len(seasons), max_episode), np.nan)

    for i, season in enumerate(seasons):
        for ep, rating in data[season].items():
            heatmap[i, ep - 1] = rating

    vmin, vmax = np.nanmin(heatmap), np.nanmax(heatmap)

    plt.figure(figsize=(14, 6))
    img = plt.imshow(heatmap, aspect="auto", cmap="RdYlGn", vmin=vmin, vmax=vmax)
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
