# Proteome-annotation
This repository is the result of a four week internship at the Rappsilber Laboratory [1].

Proteome annotation was done in python via NCBI download [2], Diamond protein sequence alignment [3], and Foldseek structural alignment [4]. Genome annotation was started but not finished and contains only a genome download script.

## Required packages
- argparse
- concurrent.futures
- csv
- glob
- io
- matplotlib
- numpy
- os
- pandas
- re 
- requests
- tqdm
- zipfile

## Project Documentation READMEs
1. General and evaluation scripts [here](ReadMe.md)
2. NCBI annotation [here](ncbi_annotation/ReadMe.md)
3. Diamond database building [here](diamond_protein_sequence_alignment/database_building_scripts/ReadMe.md)
4. Diamond results evaluation [here](diamond_protein_sequence_alignment/ReadMe.md)
5. Foldseek [here](foldseek_annotation/ReadMe.md)
6. Genome download from NCBI [here](genome_annotation/ReadMe.md)

## References
1. Rappsilber Laboratory https://www.rappsilberlab.org/,  https://github.com/Rappsilber-Laboratory
2. NCBI Datasets v2 REST API https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/rest-api/
3. Diamond https://github.com/bbuchfink/diamond
5. Foldseek https://github.com/steineggerlab/foldseek
