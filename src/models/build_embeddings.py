import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import os
import numpy as np

INPUT_PATH = os.path.join("data_files", "chembl_cleaned.csv")
OUTPUT_EMBEDDINGS = os.path.join("data_files", "compound_embeddings.npy")
OUTPUT_IDS = os.path.join("data_files", "compound_id_map.csv")

# Use pretrained ChemBERTa from HuggingFace
MODEL_NAME = "seyonec/ChemBERTa-zinc-base-v1"

def get_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def smiles_to_embedding(smiles, tokenizer, model):
    inputs = tokenizer(smiles, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    # Take mean of the last hidden state (pooled embedding)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def main():
    df = pd.read_csv(INPUT_PATH)

    # Use unique compound IDs
    compound_ids = df["molecule_chembl_id"].unique()
    print(f"Found {len(compound_ids)} unique compounds")

    tokenizer, model = get_model_and_tokenizer()

    embeddings = []
    id_map = []

    for chembl_id in tqdm(compound_ids, desc="Generating embeddings"):
        # We'll use SMILES from the ChEMBL API
        url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
        response = requests.get(url)
        if response.status_code != 200:
            continue
        smiles = response.json().get("molecule_structures", {}).get("canonical_smiles", None)
        if not smiles:
            continue

        try:
            emb = smiles_to_embedding(smiles, tokenizer, model)
            embeddings.append(emb)
            id_map.append(chembl_id)
        except Exception as e:
            print(f"Failed to embed {chembl_id}: {e}")
            continue

    # Save embeddings and ID map
    np.save(OUTPUT_EMBEDDINGS, np.array(embeddings))
    pd.DataFrame({"molecule_chembl_id": id_map}).to_csv(OUTPUT_IDS, index=False)
    print(f"[Saved {len(embeddings)} embeddings to {OUTPUT_EMBEDDINGS}")

if __name__ == "__main__":
    import requests  # Only needed here
    main()