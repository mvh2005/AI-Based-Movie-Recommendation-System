"""
save_model.py — Run this ONCE to generate model_artifacts.pkl

Usage:
    python save_model.py

This script:
1. Loads the TMDB movie dataset
2. Builds TF-IDF vectors from combined_features
3. Computes cosine similarity matrix
4. Serializes everything to a pickle file for fast loading in Streamlit
"""

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Configuration ──────────────────────────────────────────────
DATASET_PATH = "TMDB_movie_dataset_v11.csv"
OUTPUT_PATH = "model_artifacts.pkl"
NUM_MOVIES = 5000  # Keep low for GitHub size limits; 5k → ~200MB pkl

# ── Load and preprocess ───────────────────────────────────────
print(f"Loading dataset from {DATASET_PATH}...")
movie_data = pd.read_csv(DATASET_PATH, encoding="latin1", on_bad_lines="skip")

# Fill NaN in the feature column used for TF-IDF
movie_data["combined_features"] = movie_data["combined_features"].fillna("")

# Subset to top N movies
subset = movie_data.head(NUM_MOVIES).reset_index(drop=True)

print(f"Using top {NUM_MOVIES} movies. Shape: {subset.shape}")

# ── Train TF-IDF ──────────────────────────────────────────────
print("Building TF-IDF matrix...")
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(subset["combined_features"])
print(f"TF-IDF Matrix Shape: {tfidf_matrix.shape}")

# ── Compute cosine similarity ─────────────────────────────────
print("Computing cosine similarity (this may take a moment)...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(f"Cosine Similarity Matrix Shape: {cosine_sim.shape}")

# ── Serialize ─────────────────────────────────────────────────
print(f"Saving artifacts to {OUTPUT_PATH}...")
with open(OUTPUT_PATH, "wb") as f:
    pickle.dump(
        {
            "cosine_sim": cosine_sim,
            "movie_data": subset,
            "tfidf": tfidf,
        },
        f,
    )

print(f"✅ Model saved successfully! File: {OUTPUT_PATH}")
