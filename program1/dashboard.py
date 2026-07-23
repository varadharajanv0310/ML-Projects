"""
21CSC305P - Machine Learning Lab
Program 1 (extension): Dashboard for the Most Streamed Spotify Songs 2024 dataset.

Reads the same CSV as program1.py (running program1.py first if the file is
missing, which also generates the synthetic stand-in) and renders a
self-contained HTML dashboard at output/dashboard.html.
"""

import json
import os
import re
import subprocess
import sys

import pandas as pd

DATA_PATH = os.path.join("data", "Most Streamed Spotify Songs 2024.csv")
TEMPLATE_PATH = "dashboard_template.html"
OUTPUT_PATH = os.path.join("output", "dashboard.html")

if not os.path.exists(DATA_PATH):
    print("Data file missing - running program1.py to generate it...\n")
    subprocess.run([sys.executable, "program1.py"], check=True)

af = pd.read_csv(DATA_PATH, encoding="unicode_escape")

# resolve needed columns case-insensitively (same approach as program1.py)
header_map = {c.strip().lower(): c for c in af.columns}
def col(name):
    key = name.strip().lower()
    if key not in header_map:
        raise SystemExit(
            f"ERROR: column '{name}' not found in the CSV.\n"
            f"Available columns: {list(af.columns)}"
        )
    return af[header_map[key]]

def numeric(name):
    return pd.to_numeric(
        col(name).astype(str).str.replace(",", ""), errors="coerce"
    )

track = col("Track").astype(str)
artist = col("Artist").astype(str)
streams = numeric("Spotify Streams")
views = numeric("YouTube Views")
reach = numeric("Spotify Playlist Reach")
year = pd.to_datetime(
    col("Release Date"), format="mixed", dayfirst=True, errors="coerce"
).dt.year

df = pd.DataFrame({
    "track": track, "artist": artist, "streams": streams,
    "views": views, "reach": reach, "year": year,
})

synthetic = bool(track.str.fullmatch(r"Song \d+").all())

by_artist = df.groupby("artist")["streams"].agg(["sum", "count"])
top_artist = by_artist["sum"].idxmax()

top_tracks = df.dropna(subset=["streams"]).nlargest(10, "streams")
by_year = df.dropna(subset=["year"]).groupby("year").size()
by_year = by_year.reindex(range(int(by_year.index.min()), int(by_year.index.max()) + 1),
                          fill_value=0)
scatter = df.dropna(subset=["reach", "views"])

data = {
    "source": os.path.basename(DATA_PATH),
    "synthetic": synthetic,
    "kpis": {
        "tracks": len(df),
        "totalStreams": int(streams.sum()),
        "totalViews": int(views.sum()),
        "topArtist": top_artist,
        "topArtistStreams": int(by_artist.loc[top_artist, "sum"]),
        "topArtistTracks": int(by_artist.loc[top_artist, "count"]),
    },
    "topTracks": [
        {"track": r.track, "artist": r.artist, "streams": int(r.streams)}
        for r in top_tracks.itertuples()
    ],
    "byYear": [
        {"year": int(y), "count": int(c)} for y, c in by_year.items()
    ],
    "scatter": [
        {"track": r.track, "artist": r.artist,
         "reach": int(r.reach), "views": int(r.views)}
        for r in scatter.itertuples()
    ],
}

with open(TEMPLATE_PATH, encoding="utf-8") as f:
    template = f.read()

# </script> inside a JSON string would end the script block early
payload = json.dumps(data).replace("</", "<\\/")
html = template.replace("__DATA__", payload)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dashboard written to {OUTPUT_PATH}"
      + (" (synthetic data)" if synthetic else ""))
