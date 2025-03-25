import pandas as pd
import os

INPUT_PATH = os.path.join('data_files', 'chembl_compounds.csv')
OUTPUT_PATH = os.path.join('data_files', 'chembl_cleaned.csv')

def load_data(path):
    print(f"Loading data from {path}")
    return pd.read_csv(path)

def clean_data(df):
    print('Cleaning data...')


    df['pref_name'] = df['pref_name'].str.upper().fillna("UNKNOWN")
    df['molecule_type'] = df['molecule_type'].str.lower()
    df['structure_type'] = df['structure_type'].str.upper()
    df['mechanism_of_action'] = df['mechanism_of_action'].fillna("N/A")
    df['action_type'] = df['action_type'].fillna("N/A")
    df['target_name'] = df['target_name'].fillna("Unknown Target")

    # Fill missing numeric values
    df['max_phase'] = df['max_phase'].fillna(0)
    df['first_approval'] = df['first_approval'].fillna(0)

    # Drop duplicates
    df.drop_duplicates(subset=["molecule_chembl_id", "mechanism_of_action"], inplace=True)

    # Optional: filter out rows with no mechanism for training a model
    # df = df[df['mechanism_of_action'] != 'N/A']

    return df


def save_data(df, path):
    df.to_csv(path, index=False)
    print(f"Saved data to {path}")


def main():
    df = load_data(INPUT_PATH)
    cleaned_df = clean_data(df)
    save_data(cleaned_df, OUTPUT_PATH)

if __name__ == '__main__':
    main()

