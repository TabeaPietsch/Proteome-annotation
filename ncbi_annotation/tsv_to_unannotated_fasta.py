from tqdm import tqdm
import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--fastafile', help= "Please enter the path to your input fasta file.")
parser.add_argument('-t', '--tsvfile', help= "Please enter the path to the tsv file containing annotation information.")

args = parser.parse_args()

fasta_file_path = args.fastafile
tsv_file_path = args.tsvfile


# filter out accession without annotation

df_NCBI_results = pd.read_csv(tsv_file_path, sep= '\t', header = None)
list_NCBI_results = list(df_NCBI_results.iloc[:,1])
list_NCBI_accessions = list(df_NCBI_results.iloc[:,0])

list_unannotated = []
for index, entry in enumerate(list_NCBI_results):
    if type(entry) != str:
        list_unannotated.append(list_NCBI_accessions[index])

print(list_unannotated)


# process fasta file

fasta_entries_unannotated_chunks = []

with open(fasta_file_path, "r") as f:
    header = None
    seq_lines = []

    # Process line-by-line in a single pass
    for line in tqdm(f, desc="Processing and filtering FASTA"):
        if line.startswith(">"):
            # process already gathered sequences
            if header:
                sequence = "".join(seq_lines)
                entry = (header, sequence)

                for unannotated_id in list_unannotated:
                    if unannotated_id in str(header):
                        fasta_entries_unannotated_chunks.append(f"{header}{sequence}")

            header = line
            seq_lines = []
        else:
            seq_lines.append(line)

    # process last entry in fasta file
    if header:
        sequence = "".join(seq_lines)
        entry = (header, sequence)

        for unannotated_id in list_unannotated:
            if unannotated_id in str(header):
                fasta_entries_unannotated_chunks.append(f"{header}{sequence}")


# Build final fasta
unannotated_fasta = "".join(fasta_entries_unannotated_chunks)

print("unannotated", len(fasta_entries_unannotated_chunks))

# write fasta
with open("9_GCF_unannotated.faa", "w") as f:
    f.write(unannotated_fasta)