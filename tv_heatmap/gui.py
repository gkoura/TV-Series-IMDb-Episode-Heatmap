# tv_heatmap/gui.py
import threading
import tkinter as tk
from tkinter import messagebox
from rapidfuzz import fuzz

from .api import search_series, fetch_all_episodes
from .plotting import plot_episode_heatmap


class SeriesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TV Series IMDb Heatmap")
        self.geometry("500x400")

        self.entry = tk.Entry(self, width=50)
        self.entry.pack(pady=10)

        tk.Button(self, text="Search", command=self.search).pack()
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        tk.Button(self, text="Plot Heatmap", command=self.plot).pack()

        self.results = []

    def search(self):
        query = self.entry.get().strip()
        if not query:
            return

        self.listbox.delete(0, tk.END)
        results = search_series(query)

        scored = sorted(
            results,
            key=lambda r: fuzz.partial_ratio(query.lower(), r["Title"].lower()),
            reverse=True,
        )

        self.results = scored[:10]
        for r in self.results:
            self.listbox.insert(tk.END, f"{r['Title']} ({r.get('Year', 'N/A')})")

    def plot(self):
        if not self.listbox.curselection():
            messagebox.showwarning("Warning", "Select a series first")
            return

        idx = self.listbox.curselection()[0]
        imdb_id = self.results[idx]["imdbID"]
        title = self.results[idx]["Title"]

        threading.Thread(
            target=self._fetch_and_plot,
            args=(imdb_id, title),
            daemon=True,
        ).start()

    def _fetch_and_plot(self, imdb_id, title):
        try:
            episodes = fetch_all_episodes(imdb_id)
            plot_episode_heatmap(episodes, title)
        except Exception as e:
            messagebox.showerror("Error", str(e))
