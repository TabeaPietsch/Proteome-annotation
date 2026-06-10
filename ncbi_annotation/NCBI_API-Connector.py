import csv
import pandas as pd
import requests
from tqdm import tqdm
import argparse

#----- Configuration --------#

parser = argparse.ArgumentParser()
parser.add_argument('-ak', '--apikey', help= "please enter your ncbi api key (can be generated in your ncbi profile)")
parser.add_argument('-i', '--input', help= "please enter the path of the tsv file to be processed (one column of query accessions)")
parser.add_argument('-o', '--output', help= "please enter a name for your output file")

args = parser.parse_args()

apikey = args.apikey
outfile_name = args.output
accession_tsv = args.input

collect_only_annotated_accessions = input("Collect only annotated accessions [y/n]? If 'n': accessions without a gene name will be added with an empty entry.")


# 1. Read in TSV

df = pd.read_csv(accession_tsv, sep="\t", header=None)
# get rid of version at the end of accession
accessions_list = [str(acc).split(".")[0] for acc in df.iloc[:, 0].tolist()]

# 2. Batch configuration
BATCH_SIZE = 200
NCBI_URL = f"https://api.ncbi.nlm.nih.gov/datasets/v2/protein/dataset_report?api_key={apikey}"


#---- API connection via sessions ---------#

annotated_accessions = []

# Using a Session reuses the underlying TCP connection, making consecutive requests faster
with requests.Session() as session:
    # Process accessions in chunks
    for i in tqdm(
        range(0, len(accessions_list), BATCH_SIZE), desc="Fetching NCBI data"
    ):
        batch = accessions_list[i : i + BATCH_SIZE]

        # POST payload format for NCBI Datasets v2
        payload = {"accessions": batch}

        try:
            response = session.post(NCBI_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                print(data)

                # NCBI returns a list of reports for the valid accessions found
                for report in data.get("reports", []):
                    print(report)
                    # Extract accession from the report
                    acc = report.get("accession")

                    if "conserved_domains" in report:
                        gene_name = report["conserved_domains"][0].get("name")
                        if gene_name and acc:
                            annotated_accessions.append({acc: gene_name})

                    else:
                        print("gene id not found")
                        if collect_only_annotated_accessions == "n":
                            annotated_accessions.append({acc: None})
            else:
                print(
                    f"\nBatch starting at index {i} failed with status: {response.status_code}"
                )

        except Exception as e:
            print(f"\nAn error occurred during batch {i}: {e}")

print(
    f"Annotated: {len(annotated_accessions)} / {len(accessions_list)} accessions."
)


#---- output file creation -----------#

# 3. Write to TSV
with open(outfile_name, "w", encoding="utf-8", newline="") as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter="\t", lineterminator="\n")
    for accession in annotated_accessions:
        for key, value in accession.items():
            tsv_writer.writerow([key, value])