import os
import csv
import time
import requests
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config
CHUNKSIZE = 100
MAX_COMPOUNDS = 50000
OUTPUT_FILE = os.path.join("data_files", "chembl_raw_compounds.csv")

FIELDS = [
    "molecule_chembl_id", "pref_name", "molecule_type", "max_phase", "structure_type",
    "first_approval", "alogp", "psa", "qed_weighted", "mw_freebase", "full_mwt",
    "hba", "hbd", "num_ro5_violations", "cx_logp", "smiles", "inchi"
]

# Load already-saved IDs to skip
def load_checkpoint_ids():
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE, usecols=["molecule_chembl_id"])
        return set(df["molecule_chembl_id"])
    return set()

def fetch_compound_data(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
    try:
        res = requests.get(url, timeout=10)

        if res.status_code != 200 or "application/json" not in res.headers.get("Content-Type", ""):
            return None

        try:
            data = res.json()
        except Exception:
            return None

        if not isinstance(data, dict):
            return None

        props = data.get("molecule_properties", {}) or {}
        struct = data.get("molecule_structures", {}) or {}

        return {
            "molecule_chembl_id": data.get("molecule_chembl_id"),
            "pref_name": data.get("pref_name"),
            "molecule_type": data.get("molecule_type"),
            "max_phase": data.get("max_phase"),
            "structure_type": data.get("structure_type"),
            "first_approval": data.get("first_approval"),
            "alogp": props.get("alogp"),
            "psa": props.get("psa"),
            "qed_weighted": props.get("qed_weighted"),
            "mw_freebase": props.get("mw_freebase"),
            "full_mwt": props.get("full_mwt"),
            "hba": props.get("hba"),
            "hbd": props.get("hbd"),
            "num_ro5_violations": props.get("num_ro5_violations"),
            "cx_logp": props.get("cx_logp"),
            "smiles": struct.get("canonical_smiles"),
            "inchi": struct.get("standard_inchi"),
        }

    except Exception:
        return None

def write_chunk(compound_list, file_exists):
    df = pd.DataFrame(compound_list)
    if not file_exists:
        df.to_csv(OUTPUT_FILE, mode='w', index=False)
    else:
        df.to_csv(OUTPUT_FILE, mode='a', index=False, header=False)

def main():
    processed_ids = load_checkpoint_ids()
    file_exists = os.path.exists(OUTPUT_FILE)

    offset = len(processed_ids)
    base_url = "https://www.ebi.ac.uk/chembl/api/data/molecule.json"
    total_written = len(processed_ids)

    pbar = tqdm(total=MAX_COMPOUNDS, initial=total_written, desc="Ingesting compounds")

    while total_written < MAX_COMPOUNDS:
        url = f"{base_url}?limit=100&offset={offset}"
        try:
            res = requests.get(url)
            if res.status_code != 200:
                time.sleep(5)
                continue
            results = res.json().get("molecules", [])
        except Exception:
            time.sleep(5)
            continue

        if not results:
            break

        chembl_ids = [mol["molecule_chembl_id"] for mol in results if mol["molecule_chembl_id"] not in processed_ids]
        compounds = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_id = {executor.submit(fetch_compound_data, cid): cid for cid in chembl_ids}
            for future in as_completed(future_to_id):
                cid = future_to_id[future]
                try:
                    result = future.result()
                    if result:
                        compounds.append(result)
                        processed_ids.add(cid)
                except:
                    continue

        if compounds:
            write_chunk(compounds, file_exists)
            file_exists = True
            total_written += len(compounds)
            pbar.update(len(compounds))

        offset += 100

    print(f"Done. Total compounds saved: {total_written}")

if __name__ == "__main__":
    main()
