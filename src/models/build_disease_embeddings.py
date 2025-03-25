import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import os

MODEL_NAME = "dmis-lab/biobert-base-cased-v1.1"

# Example disease list (replace this with dynamic input later)
DISEASES = [
    "Duchenne Muscular Dystrophy",
    "Cystic Fibrosis",
    "Spinal Muscular Atrophy",
    "Fabry Disease",
    "Gaucher Disease",
    "ALS",
    "Huntington's Disease",
    "Batten Disease",
    "Sickle Cell Anemia",
    "Dravet Syndrome"
]


OUTPUT_EMBEDDINGS = os.path.join("data_files", "disease_embeddings.npy")
OUTPUT_NAMES = os.path.join("data_files", "disease_names.csv")

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def disease_to_embedding(disease, tokenizer, model):
    inputs = tokenizer(disease, return_tensors='pt', padding = True, truncation = True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def main():
    tokenizer, model = load_model()

    embeddings = []
    clean_diseases = []

    for disease in tqdm(DISEASES, desc="Embedding diseases"):
        try:
            emb = disease_to_embedding(disease, tokenizer, model)
            embeddings.append(emb)
            clean_diseases.append(disease)
        except Exception as e:
            print(f"Failed on {disease}: {e}")

    # Save results
    np.save(OUTPUT_EMBEDDINGS, np.array(embeddings))
    pd.DataFrame({"disease": clean_diseases}).to_csv(OUTPUT_NAMES, index=False)
    print(f"[✓] Saved {len(embeddings)} disease embeddings")

if __name__ == "__main__":
    main()