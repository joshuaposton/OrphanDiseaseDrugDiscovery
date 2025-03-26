from Bio import Entrez
import time

Entrez.email = "JoshL.Poston@gmail.com"

def get_pubmed_article_count(drug_name, max_retries=3):
    if drug_name == "N/A":
        return 0

    query = f'"{drug_name}"[Title/Abstract]'
    for attempt in range(max_retries):
        try:
            handle = Entrez.esearch(db="pubmed", term=query)
            record = Entrez.read(handle)
            return int(record["Count"])
        except Exception as e:
            print(f"Retrying ({attempt+1}/{max_retries}) due to error: {e}")
            time.sleep(1)
    return 0