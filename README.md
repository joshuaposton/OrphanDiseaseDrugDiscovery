# 🧬 OrphaMine

**AI-Powered Drug Discovery for Rare and Orphan Diseases**

OrphaMine is a public, AI-assisted platform that helps researchers identify potential drug leads for rare and underfunded diseases—by analyzing relationships between chemical compounds and disease concepts using state-of-the-art transformer models.

---

## 🚨 The Problem

Orphan diseases affect fewer than 200,000 people in the U.S. and often receive little to no attention from pharmaceutical companies due to low ROI. As a result, treatments are limited, and scientific discovery is slow.

---

## 🎯 The Solution

OrphaMine uses **AI embeddings** from public biomedical data to:

- Match diseases to promising compounds
- Surface overlooked or repurposable drugs
- Enable small labs and nonprofits to run in silico pre-screening for rare disease research

---

## 🧠 How It Works

1. **Disease Embeddings**:  
   - Use [BioBERT](https://huggingface.co/dmis-lab/biobert-base-cased-v1.1) to encode disease names into vector space based on biomedical context.

2. **Compound Embeddings**:  
   - Use [ChemBERTa](https://huggingface.co/seyonec/ChemBERTa-zinc-base-v1) to convert SMILES strings into vector embeddings that represent molecular structure and properties.

3. **Matching Engine**:  
   - Compute cosine similarity between disease vectors and compound vectors.
   - Rank top matches and display them with metadata, PubMed links, and target profiles.

---

## 💻 Features

- 🔍 Searchable AI-predicted drug-disease matches
- 📊 Adjustable similarity score threshold
- 🧪 Expandable compound metadata: mechanism of action, approval phase, target
- 📰 PubMed links for literature review
- 📥 CSV export for lab collaboration

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/orphamine.git
cd orphamine

### 2. Set up a virtual environment
python -m venv venv
venv\Scripts\activate     # On Windows
# source venv/bin/activate   # On macOS/Linux


### 3.  Install Dependencies
pip install -r requirements.txt

### 4. Run the app
streamlit run src/interface/search_interface.py


OrphaMine/
├── data_files/               # Stores compound data & embeddings
├── results/                  # Output predictions
├── src/
│   ├── data/                 # Data ingestion + cleaning scripts
│   ├── interface/            # Streamlit UI
│   └── models/               # Embedding + prediction engine
├── README.md
└── requirements.txt

🤝 Who This Is For
Academic researchers in pharmacology and computational biology

Rare disease nonprofits and open-science labs

Bioinformatics students looking for high-impact projects

🛠 Built With
BioBERT — disease embeddings

ChemBERTa — compound embeddings

Streamlit — interactive app

scikit-learn — similarity computation

ChEMBL API — public compound database

