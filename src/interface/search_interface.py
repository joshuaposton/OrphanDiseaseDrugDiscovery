import streamlit as st
import pandas as pd
import os

RESULTS_PATH = os.path.join("results", "disease_compound_matches.csv")

@st.cache_data
def load_results():
    df = pd.read_csv(RESULTS_PATH)
    return df

CHEMBL_META = os.path.join("data_files", "chembl_cleaned.csv")

@st.cache_data
def load_metadata():
    return pd.read_csv(CHEMBL_META)[[
        "molecule_chembl_id", "structure_type", "molecule_type",
        "mechanism_of_action", "first_approval", "target_name"
    ]].drop_duplicates()

def make_clickable_link(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/compound_report_card/{chembl_id}/"
    return f"[🔗 {chembl_id}]({url})"

def main():
    st.set_page_config(page_title="OrphaMine | AI-Powered Drug Discovery", layout="centered")

    st.title("🔍 OrphaMine")
    st.markdown("Discover AI-predicted compounds for **rare and orphan diseases**.")

    df = load_results()
    meta_df = load_metadata()
    diseases = sorted(df["disease"].unique())

    st.sidebar.header("Search")
    selected_disease = st.sidebar.selectbox("Select a disease:", diseases)

    st.sidebar.markdown("### Similarity Filter")
    min_score = st.sidebar.slider("Minimum similarity score", min_value=0.0, max_value=1.0, value=0.0, step=0.01)


    st.subheader(f"Top predicted compounds for:")
    st.markdown(f"### 🧬 *{selected_disease}*")

    filtered = df[df["disease"] == selected_disease].sort_values("compound_rank")
    filtered = filtered[filtered["similarity_score"] >= min_score]

    search_term = st.text_input("🔎 Filter by compound name:")
    if search_term:
        filtered = filtered[filtered["compound_name"].str.contains(search_term, case=False, na=False)]

    st.markdown(f"**{len(filtered)} compound(s) found**")


    # Format similarity & ChEMBL links
    filtered["similarity_score"] = filtered["similarity_score"].round(3)
    filtered["ChEMBL"] = filtered["compound_chembl_id"].apply(make_clickable_link)
    # Add PubMed search link
    filtered["PubMed"] = filtered.apply(
    lambda row: (
        f"[📰 PubMed](https://pubmed.ncbi.nlm.nih.gov/?term="
        f"{(row['compound_name'] if row['compound_name'] != 'N/A' else row['compound_chembl_id']).replace(' ', '+')})"
    ),
    axis=1
)
        



    # -- Add download button --
    st.download_button(
        label="📥 Download these results as CSV",
        data=filtered.to_csv(index=False),
        file_name=f"{selected_disease.replace(' ', '_')}_compound_predictions.csv",
        mime="text/csv"
    )

    # Rename and select columns
    display_df = filtered.rename(columns={
    "compound_rank": "Rank",
    "compound_name": "Compound Name",
    "similarity_score": "Score"
    })[["Rank", "Compound Name", "Score", "ChEMBL", "PubMed"]]

    st.write(display_df.to_markdown(index=False), unsafe_allow_html=True)

    st.markdown("### 🧪 Compound Details")

    for _, row in filtered.iterrows():
        with st.expander(f"{row['compound_name']} ({row['compound_chembl_id']})"):
            meta = meta_df[meta_df["molecule_chembl_id"] == row["compound_chembl_id"]]
            if meta.empty:
                st.write("No metadata available.")
            else:
                st.write({
                    "Structure Type": meta["structure_type"].values[0],
                    "Molecule Type": meta["molecule_type"].values[0],
                    "Mechanism of Action": meta["mechanism_of_action"].values[0],
                    "First Approval": int(meta["first_approval"].values[0]) if pd.notna(meta["first_approval"].values[0]) else "N/A",
                    "Target Name": meta["target_name"].values[0],
                })

    st.markdown("---")
    st.caption("This is a research prototype built with BioBERT and ChemBERTa. Results are exploratory and not clinically validated.")

if __name__ == "__main__":
    main()
