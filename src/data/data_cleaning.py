import pandas as pd
import os

INPUT_PATH = "data_files/chembl_raw_compounds.csv"
OUTPUT_PATH = "data_files/chembl_cleaned.csv"

def clean_compounds(path):
    df = pd.read_csv(path)

    # Drop rows with missing SMILES or critical modeling features
    critical_cols = [
        "smiles", "qed_weighted", "alogp", "mw_freebase", 
        "psa", "num_ro5_violations", "cx_logp"
    ]
    
    # Drop rows with missing SMILES and key modeling fields
    df.dropna(subset=["smiles", "qed_weighted", "alogp", "mw_freebase"], inplace=True)

    # Clean SMILES and InChI safely
    df["smiles"] = df["smiles"].apply(lambda x: x.strip() if isinstance(x, str) else x)
    df["inchi"] = df["inchi"].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert numerics
    for col in ["qed_weighted", "alogp", "mw_freebase", "psa", "num_ro5_violations", "cx_logp"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Optional second drop for remaining junk
    df.dropna(subset=["qed_weighted", "alogp", "mw_freebase"], inplace=True)


    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Cleaned and saved {len(df)} compounds to {OUTPUT_PATH}")

if __name__ == "__main__":
    clean_compounds(INPUT_PATH)
