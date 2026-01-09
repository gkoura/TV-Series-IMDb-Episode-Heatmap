# TV Series IMDb Episode Heatmap

## Overview

**TV Series IMDb Episode Heatmap** is a Python desktop application that visualizes IMDb episode ratings for television series as an intuitive season-by-episode heatmap. The tool makes it easy to identify trends in show quality over time, highlight standout episodes, and spot declines or resurgences across seasons.

The application uses the OMDb API as its data source and presents results via a Tkinter-based GUI with Matplotlib visualizations.

---

## Features

* Search for TV series by name using the OMDb API
* Intelligent fuzzy matching to surface the most relevant results
* Automatic retrieval of all seasons and episodes
* Color-coded heatmap of IMDb ratings (season × episode)
* Numeric rating overlays for precise inspection
* Responsive GUI with background threading (no UI freezing)
* Modular, production-quality codebase

---

## Screenshot
Example:

![Heatmap Example](assets/example.jpeg)

---

## Installation

### Prerequisites

* Python **3.9 or later**
* An OMDb API key (free tier is sufficient)

### Clone the Repository

```bash
git clone https://github.com/gkoura/tv-series-imdb-heatmap.git
cd tv-series-imdb-heatmap
```

### Create and Activate a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\\Scripts\\activate         # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The application requires an OMDb API key to function.

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your API key:

```
OMDB_API_KEY=your_actual_api_key_here
```

3. Ensure the environment variable is loaded before running the app.

> **Note:** Never commit your `.env` file to version control.

---

## Usage

Run the application from the project root:

```bash
python -m tv_heatmap.main
```

### Workflow

1. Enter the name of a TV series
2. Click **Search**
3. Select the correct series from the results list
4. Click **Plot Heatmap**
5. Explore episode ratings visually

---

## Technical Notes

* The OMDb API search endpoint is paginated; the application automatically retrieves multiple pages when necessary
* IMDb ratings marked as `N/A` are excluded from the visualization
* Specials and missing episode numbers are ignored
* Heatmap color scaling is dynamic, based on available ratings

---

## Project Structure

```
tv-series-imdb-heatmap/
├── tv_heatmap/
│   ├── api.py        # OMDb API interaction
│   ├── plotting.py   # Heatmap generation
│   ├── gui.py        # Tkinter GUI
│   └── main.py       # Application entry point
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Future Improvements

* Export heatmaps as PNG or PDF
* Command-line (CLI) mode
* Local caching of OMDb responses
* Support for episode air dates and trends over time
* Unit and integration test coverage

---

## License

This project is released under the **MIT License**. You are free to use, modify, and distribute it.

---

## Acknowledgments

* [OMDb API](https://www.omdbapi.com/) for IMDb data
* Matplotlib and NumPy for visualization
* RapidFuzz for fuzzy string matching
