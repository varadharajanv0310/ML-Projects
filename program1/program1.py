"""
21CSC305P - Machine Learning Lab
Program 1: Load a dataset, create a duplicate, select a column subset and view it.

Dataset: Most Streamed Spotify Songs 2024 (Kaggle)

ALGORITHM
Step 1: Import the pandas library and load the dataset CSV file into a
        DataFrame `af` (using encoding='unicode_escape').
Step 2: Create a duplicate of the DataFrame using new_af = af.copy().
Step 3: Select the required subset of columns (Artist, Release Date,
        All Time Rank, Spotify Playlist Reach, YouTube Views).
Step 4: View the data using head(10), info(), shape and describe().
"""

import os
import random

import pandas as pd
import matplotlib.pyplot as plt  # manual had 'matplotlib.pylot' - fixed

DATA_PATH = os.path.join("data", "Most Streamed Spotify Songs 2024.csv")
OUTPUT_PATH = os.path.join("output", "head10.csv")

# Full schema of the real Kaggle dataset
SCHEMA = [
    "Track", "Album Name", "Artist", "Release Date", "ISRC",
    "All Time Rank", "Track Score", "Spotify Streams",
    "Spotify Playlist Count", "Spotify Playlist Reach",
    "Spotify Popularity", "YouTube Views", "YouTube Likes",
    "TikTok Posts", "TikTok Likes", "TikTok Views",
]

# Columns required for this program (as they appear in the real CSV)
SUBSET_COLUMNS = [
    "Artist", "Release Date", "All Time Rank",
    "Spotify Playlist Reach", "YouTube Views",
]


def make_synthetic_csv(path):
    """Generate a synthetic CSV with the same schema as the real dataset,
    so the program runs end-to-end even without the Kaggle download."""
    random.seed(42)
    artists = ["Taylor Swift", "The Weeknd", "Bad Bunny", "Drake", "Dua Lipa",
               "Ed Sheeran", "Ariana Grande", "Billie Eilish", "Post Malone",
               "Olivia Rodrigo"]
    rows = []
    for rank in range(1, 51):
        artist = random.choice(artists)
        rows.append({
            "Track": f"Song {rank}",
            "Album Name": f"Album {random.randint(1, 20)}",
            "Artist": artist,
            "Release Date": f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(2015, 2024)}",
            "ISRC": f"US{random.randint(100, 999)}{random.randint(1000000, 9999999)}",
            "All Time Rank": f"{rank:,}",
            "Track Score": round(random.uniform(100, 800), 1),
            "Spotify Streams": f"{random.randint(100_000_000, 4_000_000_000):,}",
            "Spotify Playlist Count": f"{random.randint(10_000, 600_000):,}",
            "Spotify Playlist Reach": f"{random.randint(10_000_000, 300_000_000):,}",
            "Spotify Popularity": random.randint(60, 100),
            "YouTube Views": f"{random.randint(50_000_000, 2_500_000_000):,}",
            "YouTube Likes": f"{random.randint(500_000, 30_000_000):,}",
            "TikTok Posts": f"{random.randint(10_000, 5_000_000):,}",
            "TikTok Likes": f"{random.randint(1_000_000, 500_000_000):,}",
            "TikTok Views": f"{random.randint(10_000_000, 5_000_000_000):,}",
        })
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pd.DataFrame(rows, columns=SCHEMA).to_csv(path, index=False)


# ---- Step 1: Load the dataset ----
if not os.path.exists(DATA_PATH):
    print("=" * 70)
    print("NOTICE: Real Kaggle CSV not found at:", DATA_PATH)
    print("Generating SYNTHETIC data with the same schema so the program")
    print("runs end-to-end. Replace the file with the real Kaggle download")
    print("('Most Streamed Spotify Songs 2024') to use actual data.")
    print("=" * 70)
    make_synthetic_csv(DATA_PATH)

af = pd.read_csv(DATA_PATH, encoding="unicode_escape")

# ---- Step 2: Create a duplicate of the DataFrame ----
new_af = af.copy()

# ---- Step 3: Select the subset of columns ----
# Match wanted columns against the actual CSV headers case-insensitively,
# so lowercase names from the manual (e.g. "release date") still resolve.
header_map = {c.strip().lower(): c for c in new_af.columns}
missing = [c for c in SUBSET_COLUMNS if c.strip().lower() not in header_map]
if missing:
    raise SystemExit(
        f"ERROR: column(s) {missing} not found in the CSV.\n"
        f"Available columns: {list(new_af.columns)}"
    )
subset = new_af[[header_map[c.strip().lower()] for c in SUBSET_COLUMNS]]

# Numeric columns are stored as text with thousands separators
# (e.g. "1,234,567") - convert them so describe() gives real statistics.
for col in ["All Time Rank", "Spotify Playlist Reach", "YouTube Views"]:
    subset[col] = pd.to_numeric(
        subset[col].astype(str).str.replace(",", ""), errors="coerce"
    )

# ---- Step 4: View the data ----
pd.set_option("display.width", 120)

print("\n--- head(10) ---")
print(subset.head(10).to_string())

print("\n--- info() ---")
subset.info()

print("\n--- shape ---")
print(subset.shape)

print("\n--- describe() ---")
print(subset.describe().to_string())

# Save head(10) for the lab record
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
subset.head(10).to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved head(10) to {OUTPUT_PATH}")
