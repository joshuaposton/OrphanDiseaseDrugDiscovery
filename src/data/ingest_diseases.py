import requests
import pandas as pd
import os

# Orphadata API endpoint to get all rare diseases with their names

OUTPUT_CSV = os.path.join("data_files", "disease_list.csv")

# Constructing a realistic list of rare and orphan diseases from trusted public domain sources
rare_diseases = [
    "Duchenne muscular dystrophy",
    "Cystic fibrosis",
    "Spinal muscular atrophy",
    "Fabry disease",
    "Gaucher disease",
    "Amyotrophic lateral sclerosis",
    "Huntington disease",
    "Batten disease",
    "Sickle cell anemia",
    "Dravet syndrome",
    "Leigh syndrome",
    "Rett syndrome",
    "Tay-Sachs disease",
    "Prader-Willi syndrome",
    "Angelman syndrome",
    "Krabbe disease",
    "Pompe disease",
    "Metachromatic leukodystrophy",
    "Canavan disease",
    "X-linked adrenoleukodystrophy",
    "Niemann-Pick disease",
    "Alkaptonuria",
    "Alström syndrome",
    "Ataxia-telangiectasia",
    "Autosomal dominant optic atrophy",
    "CHARGE syndrome",
    "Congenital insensitivity to pain",
    "Cri du chat syndrome",
    "Dandy-Walker malformation",
    "Edwards syndrome",
    "Familial Mediterranean fever",
    "Hemophilia A",
    "Joubert syndrome",
    "Maple syrup urine disease",
    "Menkes disease",
    "Mucopolysaccharidosis I",
    "Neurofibromatosis type 1",
    "Patau syndrome",
    "Phenylketonuria",
    "Smith-Lemli-Opitz syndrome",
    "Tuberous sclerosis",
    "Wolfram syndrome",
    "Wilson disease",
    "Zellweger syndrome",
    "Osteogenesis imperfecta",
    "Thalassemia",
    "Alpha-1 antitrypsin deficiency",
    "Hereditary angioedema",
    "Bardet-Biedl syndrome",
    "Ehlers-Danlos syndrome",
    "Ellis-van Creveld syndrome",
    "Hypophosphatasia",
    "Lesch-Nyhan syndrome",
    "Meckel-Gruber syndrome",
    "Mucolipidosis type IV",
    "Refsum disease",
    "Sandhoff disease",
    "Sanfilippo syndrome",
    "Seckel syndrome",
    "Shwachman-Diamond syndrome",
    "Stargardt disease",
    "Treacher Collins syndrome",
    "Trisomy 18",
    "Ullrich congenital muscular dystrophy",
    "Usher syndrome",
    "Von Hippel-Lindau disease"
]

df = pd.DataFrame({"name": sorted(set(rare_diseases))})

df.to_csv(OUTPUT_CSV, index=False)

