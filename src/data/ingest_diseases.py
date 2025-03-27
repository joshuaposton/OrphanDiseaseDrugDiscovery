import xml.etree.ElementTree as ET
import pandas as pd

# Path to your en_product4.xml file
xml_path = "src/data/en_product4.xml"  # change this if needed
output_csv = "data_files/disease_list.csv"

def parse_orphanet_diseases(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    diseases = []
    for disorder in root.findall(".//Disorder"):
        name_tag = disorder.find(".//Name")
        if name_tag is not None and name_tag.text:
            diseases.append(name_tag.text.strip())

    return sorted(set(diseases))

def main():
    diseases = parse_orphanet_diseases(xml_path)
    df = pd.DataFrame({"name": diseases})
    df.to_csv(output_csv, index=False)
    print(f"✅ Parsed and saved {len(diseases)} orphan diseases to {output_csv}")

if __name__ == "__main__":
    main()
