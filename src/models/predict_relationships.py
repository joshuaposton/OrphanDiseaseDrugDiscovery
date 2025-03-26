import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.utils.pubmed_utils import get_pubmed_article_count


# Input paths
DISEASE_EMBEDDINGS = os.path.join("data_files", "disease_embeddings.npy")
DISEASE_NAMES = os.path.join("data_files", "disease_names.csv")
COMPOUND_EMBEDDINGS = os.path.join("data_files", "compound_embeddings.npy")
COMPOUND_IDS = os.path.join("data_files", "compound_id_map.csv")
COMPOUND_META = os.path.join("data_files", "chembl_cleaned.csv")

# Output path
OUTPUT_PATH = os.path.join("results", "disease_compound_matches.csv")
TOP_N = 15

def load_embeddings():
    disease_embeddings = np.load(DISEASE_EMBEDDINGS)
    compound_embeddings = np.load(COMPOUND_EMBEDDINGS)
    disease_names = pd.read_csv(DISEASE_NAMES)["disease"].tolist()
    compound_ids = pd.read_csv(COMPOUND_IDS)["molecule_chembl_id"].tolist()
    compound_df = pd.read_csv(COMPOUND_META)[["molecule_chembl_id", "pref_name"]].drop_duplicates()
    return disease_embeddings, disease_names, compound_embeddings, compound_ids, compound_df

def rank_compound_matches(d_embs, d_names, c_embs, c_ids, compound_df, top_n):
    results = []
    sim_matrix = cosine_similarity(d_embs, c_embs)

    for i, disease in enumerate(d_names):
        sim_scores = sim_matrix[i]
        top_indices = np.argsort(sim_scores)[::-1][:top_n]

        for rank, idx in enumerate(top_indices, start=1):
            chembl_id = c_ids[idx]
            name = compound_df.loc[compound_df["molecule_chembl_id"] == chembl_id, "pref_name"].values
            name = name[0] if len(name) > 0 else "N/A"

            pubmed_count = get_pubmed_article_count(name)

            results.append({
                "disease": disease,
                "compound_rank": rank,
                "compound_chembl_id": chembl_id,
                "compound_name": name,
                "similarity_score": sim_scores[idx],
                "pubmed_articles": pubmed_count
            })

    return pd.DataFrame(results)

def main():
    os.makedirs("results", exist_ok=True)

    print("[...] Loading embeddings and metadata...")
    d_embs, d_names, c_embs, c_ids, compound_df = load_embeddings()

    print("[...] Ranking compound matches...")
    results_df = rank_compound_matches(d_embs, d_names, c_embs, c_ids, compound_df, TOP_N)

    results_df.to_csv(OUTPUT_PATH, index=False)
    print(f"[✓] Saved enriched matches to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
