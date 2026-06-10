import re
from tqdm import tqdm
import pandas as pd
import csv
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--fastafile', nargs= "+", help= "Please enter one or more paths of fasta files (space separated).")
parser.add_argument('-e', '--excelfile', help= "Please enter the path to your excel file to be filtered.")
parser.add_argument('-n', '--name', help= "Please enter the column name of the query accessions within your excel file (use paranthesis).")

args = parser.parse_args()

annotated_sequences_excel = args.excelfile
input_fastas = args.fastafile
accessions_column_name = args.name


# read in annotated sequences from xlsx and save accession queries

sheet_names = pd.ExcelFile(annotated_sequences_excel).sheet_names
print("sheet names", sheet_names)


def process_sheet(
        sheet_name,
        annotated_sequences_excel,
        fasta_file_path):

    df = pd.read_excel(annotated_sequences_excel, sheet_name=sheet_name)

    # extract query accession ("WP_"...)
    annotated_WP = list(df[accessions_column_name])

    ### process input fasta file and only save entries that were not annotated via sequence similarity yet

    # Pre-compile the regex pattern for the query accession outside the loop for speed
    WP_regex = re.compile(r"^>WP_[\w.]+")

    fasta_entries_unannotated = []
    # input_fastas_unannotated = []
    # for sheet_index, sheet_name in tqdm(enumerate(sheet_names)):

    #     single_sheet_fasta_entries_unannotated = []
    with open(fasta_file_path, "r") as f:
        for line in f:
            if line.startswith(">"):
                WP_match = WP_regex.search(line)
                # unpack regex match
                WP_id = WP_match.group() if WP_match else None
                # get rid of ">" at the start
                WP_id = WP_id[1:]

                # check if WP is already annotated
                if WP_id not in annotated_WP:
                    fasta_entries_unannotated.append(WP_id)

    return fasta_entries_unannotated


# unannotated sequences to fasta
def write_tsv(outfile_name, fasta_entries_unannotated):
    with open(outfile_name, "w", encoding= "utf-8", newline= '') as tsv_file:
        tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
        for WP in tqdm(fasta_entries_unannotated, desc= "writing list of unannotated query accessions"):
            tsv_writer.writerow([WP])
    tsv_file.close()


# call functions for all sheets
for sheet_index, sheet_name in enumerate(tqdm(sheet_names, desc= "processing sheets")):
    fasta_file_path =input_fastas[sheet_index]

    fasta_entries_unannotated = process_sheet(
        sheet_name= sheet_name,
        annotated_sequences_excel= annotated_sequences_excel,
        fasta_file_path= fasta_file_path,
    )
    outfile_name = f"{sheet_index + 1}unannotated_GCF.tsv"
    write_tsv(outfile_name= outfile_name,
              fasta_entries_unannotated= fasta_entries_unannotated)