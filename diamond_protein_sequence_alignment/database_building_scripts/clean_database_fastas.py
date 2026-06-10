import re
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fastafile', help= "Please enter the path to your fasta file to be filtered for annotated entries.")
parser.add_argument('-o', '--output', help= "Please enter a name for your output fasta file.")

args = parser.parse_args()

fasta_file_path = args.fastafile
output_name = args.output + ".faa"

fasta_entries_annotated = []
fasta_entries_unannotated = []
clean_fasta_chunks = []  # Keep chunks in a list, join once at the very end

# Pre-compile the regex pattern outside the loop for speed
gene_regex = re.compile(r"GN=([^= ]+)")

with open(fasta_file_path, "r") as f:
    header = None
    seq_lines = []

    # Process line-by-line in a single pass
    for line in tqdm(f, desc="Processing and filtering FASTA"):
        if line.startswith(">"):
            # If we already have a gathered sequence, process it before moving to the next
            if header:
                sequence = "".join(seq_lines)
                entry = (header, sequence)

                # Regex search directly on the header
                gene_match = gene_regex.search(header)
                gene_id = gene_match.group(1) if gene_match else None

                if gene_id and "_" not in gene_id:
                    fasta_entries_annotated.append(entry)
                    # Append to list instead of string concatenation (O(1) vs O(N))
                    clean_fasta_chunks.append(f"{header}\n{sequence}\n")
                else:
                    fasta_entries_unannotated.append(entry)

            header = line.rstrip()  # rstrip is faster than strip() for newlines
            seq_lines = []
        else:
            seq_lines.append(line.rstrip())

    # Don't forget to process the very last entry in the file
    if header:
        sequence = "".join(seq_lines)
        entry = (header, sequence)
        gene_match = gene_regex.search(header)
        gene_id = gene_match.group(1) if gene_match else None

        if gene_id and "_" not in gene_id:
            fasta_entries_annotated.append(entry)
            clean_fasta_chunks.append(f"{header}\n{sequence}\n")
        else:
            fasta_entries_unannotated.append(entry)

# Build the final clean_fasta string instantly at the end
clean_fasta = "".join(clean_fasta_chunks)

print("len(fasta_entries_annotated)", len(fasta_entries_annotated))
print("unannotated", len(fasta_entries_unannotated))

# write clean fasta
with open(output_name, "w") as f:
    f.write(clean_fasta)