"""
Create an excel file with 9 sheets (one for every bacterium).
Write all relevant information into it (columns):
    1. query accession
    2. sequence
    3. gene id (ncbi)
    4. gene id (diamond)
    5. organism providing gene id (diamond)
    6. target found (foldseek)
    7. database of target (foldseek)
"""
#--------------------------------------------#
#------ imports -----------------------------#
#--------------------------------------------#

import pandas as pd
from tqdm import tqdm


#--------------------------------------------#
#------ configuration -----------------------#
#--------------------------------------------#

# complete input accessions
input_accessions = [
    "ncbi_annotation/complete_input_fasta_accessions/1_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/2_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/3_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/4_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/5_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/6_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/7_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/8_GCF-original_accessions.tsv",
    "ncbi_annotation/complete_input_fasta_accessions/9_GCF-original_accessions.tsv"
    ]

# original input fasta files
input_fastas = [
    "protein_sequence_alignment/InputFasta/1_GCF_900105145.1.faa",
    "protein_sequence_alignment/InputFasta/2_GCF_000766795.1.faa",
    "protein_sequence_alignment/InputFasta/3_GCF_000688335.1.faa",
    "protein_sequence_alignment/InputFasta/4_GCF_007827445.1.faa",
    "protein_sequence_alignment/InputFasta/5_GCF_002846555.1.faa",
    "protein_sequence_alignment/InputFasta/6_GCF_000060345.1.faa",
    "protein_sequence_alignment/InputFasta/7_GCF_900105035.1.faa",
    "protein_sequence_alignment/InputFasta/8_GCF_007827275.1.faa",
    "protein_sequence_alignment/InputFasta/9_GCF_000723205.1.faa"
]

# diamond output (performed for complete bacteria proteomes)
diamond_out_excel = r"protein_sequence_alignment/merged_output_bacteroidota_unique.xlsx"
diamond_sheet_names = [
    "1out_bacteroidota_LowE",
    "2out_bacteroidota_LowE",
    "3out_bacteroidota_LowE",
    "4out_bacteroidota_LowE",
    "5out_bacteroidota_LowE",
    "6out_bacteroidota_LowE",
    "7out_bacteroidota_LowE",
    "8out_bacteroidota_LowE",
    "9out_bacteroidota_LowE"
]

# new names for the merged excel file
output_sheet_names = [
    "bacterium1", "bacterium2", "bacterium3", "bacterium4", "bacterium5", "bacterium6", "bacterium7", "bacterium8", "bacterium9"
]

# ncbi output (performed for complete bacteria proteomes)
ncbi_annotated_tsvs = [
    "ncbi_annotation/original_input_accessions_ncbi_annotated/1_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/2_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/3_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/4_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/5_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/6_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/7_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/8_GCF-original_annotated.tsv",
    "ncbi_annotation/original_input_accessions_ncbi_annotated/9_GCF-original_annotated.tsv"
]

# foldseek output (performed for remaining unannotated proteins after diamond and ncbi annotation)
# one output for all 9 species
foldseek_annotated_tsv = "foldseek_annotation/foldseek_results_best_matches.tsv"


#--------------------------------------------#
#------ functions ---------------------------#
#--------------------------------------------#

def collect_fasta_entries(filepath):
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


#--------------------------------------------#
#------ process files -----------------------#
#--------------------------------------------#

# loop through all 9 species
all_sheets_dict = {}

for index, sheet_name in enumerate(diamond_sheet_names):
    # read in sequence alignment sheets (query accession with version)
    diamond_df = pd.read_excel(diamond_out_excel, sheet_name= sheet_name)
    diamond_df = diamond_df.rename(columns={
        "Query Accession ": "query accession",
        "gene_id": "gene id (diamond)",
        "organism": "organism providing gene id (diamond)"
        })
    print(diamond_df.columns)
    diamond_df_select = diamond_df[["query accession", "gene id (diamond)", "organism providing gene id (diamond)"]]

    # read in ncbi information (query accession without version)
    ncbi_df = pd.read_csv(ncbi_annotated_tsvs[index], sep= "\t", header= None)
    ncbi_df.columns = ["query accession", "gene id (ncbi)"]
    # Append '.1' to every row in the column
    ncbi_df["query accession"] = ncbi_df["query accession"].astype(str) + ".1"
    print(ncbi_df)

    # read in foldseek information (query accession with version)
    foldseek_df = pd.read_csv(foldseek_annotated_tsv, sep= "\t")
    foldseek_df = foldseek_df.rename(columns={
        "query": "query accession",
        "target": "target found (foldseek)",
        "database": "database of target (foldseek)"
        })
    foldseek_select = foldseek_df[["query accession", "target found (foldseek)", "database of target (foldseek)"]]

    # read in all accessions (query accession with version)
    merged_accessions = pd.read_csv(input_accessions[index], sep= "\t", header=None)
    merged_accessions.columns = ["query accession"]

    # read in sequences
    fasta_entries = collect_fasta_entries(input_fastas[index])
    sequences = []
    for entry in fasta_entries:
        sequences.append(entry[1])

    # add fasta sequences to merged dict
    merged_accessions["sequence"] = sequences
    print(merged_accessions)

    # merge ncbi information
    ncbi_merge = pd.merge(
        merged_accessions, ncbi_df, on="query accession", how="left"
    )

    # merge diamond information
    ncbi_diamond_merge = pd.merge(
        ncbi_merge, diamond_df_select, on="query accession", how="left"
    )

    # merge foldseek information
    final_merged_df = pd.merge(
        ncbi_diamond_merge, foldseek_select, on="query accession", how="left"
    )
    print(final_merged_df)
    
    all_sheets_dict[output_sheet_names[index]] = final_merged_df


#--------------------------------------------#
#------ write output excel file -------------#
#--------------------------------------------#

with pd.ExcelWriter("annotation_info_all.xlsx", engine="openpyxl") as writer:
    for name, df in tqdm(all_sheets_dict.items(), desc= "writing excel file..."):
        df.to_excel(writer, sheet_name=name, index=False)