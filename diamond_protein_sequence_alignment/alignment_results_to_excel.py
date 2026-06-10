import pandas as pd
import re
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e', '--excelfile', help="Please enter the path to your diamond results excel file.")
parser.add_argument('-f', '--fastafile', help="Please enter the path to your diamond database fasta file.")
parser.add_argument('-o', '--output', help="Please enter a name for your output excel file.")

args = parser.parse_args()

excel_file = args.excelfile
fasta_file = args.fastafile
outputname = args.output

protein_column = "Target Accession"
distance_column = "E-Value"


# ---------------------------------------------------------
# 1. Parse FASTA file (pure Python, no BioPython required)
# ---------------------------------------------------------

def parse_fasta(filepath):
    fasta_entries = []
    with open(filepath, "r") as f:
        header = None
        seq_lines = []

        for line in tqdm(f, desc= "parsing fasta file..."):
            line = line.strip()
            if line.startswith(">"):
                if header:
                    fasta_entries.append((header, "".join(seq_lines)))
                header = line[1:]  # remove ">"
                seq_lines = []
            else:
                seq_lines.append(line)

        # last entry
        if header:
            fasta_entries.append((header, "".join(seq_lines)))

    return fasta_entries


raw_fasta = parse_fasta(fasta_file)

# Convert to DataFrame with extracted fields
records = []
locus_tag_counter = 0
for header, seq in tqdm(raw_fasta, desc= "converting to dataframe..."):

    # clean_id = second field between pipes
    parts = header.split("|")
    clean_id = parts[1] if len(parts) >= 2 else None

    # gene_id extraction
    gene_match = re.search(r"GN=([^= ]+)", header)
    # extract gene id from regex result
    gene_id = gene_match.group(1) if gene_match else None

    # organism extraction
    org_match = re.search(r"OS=([^=]+?)(?= OX=| GN=| PE=| SV=|$)", header)
    organism = org_match.group(1).strip() if org_match else None

    records.append({
        "clean_id": clean_id,
        "sequence": seq,
        "gene_id": gene_id,
        "organism": organism
    })

fasta_df = pd.DataFrame(records)

# ---------------------------------------------------------
# 2. Function to process one sheet
# ---------------------------------------------------------

def process_sheet(sheet_name):
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # extract clean_id from protein_column
    df["clean_id"] = df[protein_column].str.split("|", expand=True)[1]

    # merge with FASTA info
    df = df.merge(fasta_df, on="clean_id", how="left")
    return df


# ---------------------------------------------------------
# 3. Process all sheets
# ---------------------------------------------------------

sheet_names = pd.ExcelFile(excel_file).sheet_names

merged_dict = {sheet: process_sheet(sheet) for sheet in tqdm(sheet_names, desc= "processing sheets...")}


# ---------------------------------------------------------
# 4. Create LowE versions
# ---------------------------------------------------------

for sheet in tqdm(sheet_names, desc= "creating lowE versions..."):
    df = merged_dict[sheet].copy()

    # convert E-value to numeric
    df["EValue_numeric"] = pd.to_numeric(df[distance_column], errors="coerce")

    # remove E-values greater than 10^(-5)
    df = df[(df["EValue_numeric"].notna()) & (df["EValue_numeric"] <= 10**-5)]

    # remove gene_ids containing "_"
    df = df[df["gene_id"].notna() & ~df["gene_id"].str.contains("_")]

    # lowest E-value per gene_id, highest Bitscore if E-values are equal
    df_lowE = df.sort_values(["EValue_numeric", "Bit Score"], ascending= [True, False]).groupby("gene_id").head(1)

    # lowest E-value per accession query, highest Bitscore if E-values are equal
    df_lowE_unique = df_lowE.sort_values(["EValue_numeric", "Bit Score"], ascending=[True, False]).groupby("Query Accession ").head(1)

    merged_dict[f"{sheet}_LowE"] = df_lowE_unique

print(merged_dict)


# ---------------------------------------------------------
# 6. Write final Excel with all sheets
# ---------------------------------------------------------
outputname = outputname + ".xlsx"

with pd.ExcelWriter(outputname, engine="openpyxl") as writer:
    for name, df in tqdm(merged_dict.items(), desc= "writing excel file..."):
        df.to_excel(writer, sheet_name=name[:31], index=False)
