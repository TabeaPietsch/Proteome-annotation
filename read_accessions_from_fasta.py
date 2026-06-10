import csv
from tqdm import tqdm
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help= "Please enter the path of the input fasta file")
parser.add_argument('-o', '--output', help= "Please enter the wanted name of the output file")

args = parser.parse_args()

input_fasta_file_path = args.input
outfile_name = args.output

WP_regex = re.compile(r"^>WP_[\w.]+")

fasta_entries = []

with open(input_fasta_file_path, "r") as f:
    for line in f:
        if line.startswith(">"):
            WP_match = WP_regex.search(line)
            # unpack regex match
            WP_id = WP_match.group() if WP_match else None
            # get rid of ">" at the start
            WP_id = WP_id[1:]

            fasta_entries.append(WP_id)

print(len(fasta_entries))

with open(outfile_name, "w", encoding= "utf-8", newline= '') as tsv_file:
    tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
    for accession in tqdm(fasta_entries, desc= "writing list accessions"):
        tsv_writer.writerow([accession])