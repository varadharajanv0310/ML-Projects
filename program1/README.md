# Program 1 — Load and View Dataset (21CSC305P ML Lab)

**Aim:** Load a dataset, create a duplicate, select a column subset, and view it.

Dataset: [Most Streamed Spotify Songs 2024](https://www.kaggle.com/datasets/nelgiriyewithana/most-streamed-spotify-songs-2024) (Kaggle).

## Run

```bash
pip install -r requirements.txt
python program1.py
```

That's it. If the real Kaggle CSV is not present, the script prints a notice and
generates a **synthetic CSV with the same schema** so the program still runs
end-to-end.

## Using the real dataset

1. Download the CSV from Kaggle.
2. Place it at `data/Most Streamed Spotify Songs 2024.csv` (delete the synthetic
   one if it's already there).
3. Run again — the script loads it with `encoding='unicode_escape'`, which the
   real file needs.

## What it does

1. Loads the CSV into a DataFrame `af`.
2. Duplicates it: `new_af = af.copy()`.
3. Selects the subset: Artist, Release Date, All Time Rank,
   Spotify Playlist Reach, YouTube Views (column names are matched
   case-insensitively against the CSV headers; a missing column fails with a
   clear error listing the available headers).
4. Prints `head(10)`, `info()`, `shape`, `describe()`, and saves the head(10)
   table to `output/head10.csv` for pasting into the lab record.

A Jupyter version is in `program1.ipynb` (`jupyter notebook program1.ipynb`).

## Dashboard

```bash
python dashboard.py
```

Generates `output/dashboard.html` — a self-contained interactive dashboard
(KPI tiles, top 10 tracks by streams, releases by year, playlist reach vs.
YouTube views, with hover tooltips, per-chart data tables, and light/dark
themes). It reads the same CSV as `program1.py` (running it first if the data
file is missing) and works identically with the real Kaggle download. Open the
generated file in any browser.

## Fixes vs. the lab manual code

- `matplotlib.pylot` → `matplotlib.pyplot`
- Smart quotes (`“ ”`) → straight quotes
- Lowercase column names (`"release date"`, …) → matched to the real headers
  (`Release Date`, …) via case-insensitive mapping
- Numeric columns with thousands separators (`"1,234,567"`) converted to
  numbers so `describe()` gives real statistics
