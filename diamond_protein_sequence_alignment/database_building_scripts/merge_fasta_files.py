import glob
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help= "Please enter the path to your directory, containing the fasta files to be merged.")
parser.add_argument('-o', '--output', help="Please enter a name for your output fasta file.")

args = parser.parse_args()
files_path = args.directory + "/*"
output_path = args.output + ".faa"

output_file = open(output_path, "w")

files = [file for file in glob.glob(files_path)]

for file_name in tqdm(files):
    with open(file_name, 'r') as fasta_file:
        content = fasta_file.read()
        output_file.write(content)

output_file.close()
