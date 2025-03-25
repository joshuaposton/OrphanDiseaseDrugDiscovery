import requests
import pandas as pd
import os
from time import sleep

OUTPUT_PATH = os.path.join('data_files', 'chembl_compounds.csv')
BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

def fetch_chembl_compounds(limit=100):
    """
    Fetches a list of molecules from the ChEMBL API.
    """
    url = f"{BASE_URL}/molecule.json?max_phase=4&limit={limit}"
    print(f"Fetching ChEMBL data from {url}")
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f'Failed to fetch ChEMBL data: {response.status_code}')
    
    data = response.json()['molecules']
    print(f"Fetched {len(data)} compounds.")
    return data
    

def fetch_mechanism_of_action(chembl_id):
    url = f"{BASE_URL}/mechanism.json?molecule_chembl_id={chembl_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return response.json().get("mechanisms", [])

    

def parse_and_enrich(compounds):
    enriched_rows = []
    for compound in compounds:
        chembl_id = compound.get("molecule_chembl_id")
        mechanisms = fetch_mechanism_of_action(chembl_id)
        sleep(0.2)  # Be nice to the API
        
        if mechanisms:
            for mech in mechanisms:
                enriched_rows.append({
                    "molecule_chembl_id": chembl_id,
                    "pref_name": compound.get("pref_name"),
                    "molecule_type": compound.get("molecule_type"),
                    "structure_type": compound.get("structure_type"),
                    "max_phase": compound.get("max_phase"),
                    "first_approval": compound.get("first_approval"),
                    "mechanism_of_action": mech.get("mechanism_of_action"),
                    "action_type": mech.get("action_type"),
                    "target_chembl_id": mech.get("target_chembl_id"),
                    "target_name": mech.get("target_name")
                })
        else:
            enriched_rows.append({
                "molecule_chembl_id": chembl_id,
                "pref_name": compound.get("pref_name"),
                "molecule_type": compound.get("molecule_type"),
                "structure_type": compound.get("structure_type"),
                "max_phase": compound.get("max_phase"),
                "first_approval": compound.get("first_approval"),
                "mechanism_of_action": None,
                "action_type": None,
                "target_chembl_id": None,
                "target_name": None
            })
    
    return pd.DataFrame(enriched_rows)


def save_to_csv(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved data to {path}")

def main():
    print("[...] Fetching base compound list...")
    compounds = fetch_chembl_compounds(limit=50)
    
    print("[...] Fetching mechanisms of action for each compound...")
    enriched_df = parse_and_enrich(compounds)
    
    save_to_csv(enriched_df, OUTPUT_PATH)

if __name__ == "__main__":
    main()