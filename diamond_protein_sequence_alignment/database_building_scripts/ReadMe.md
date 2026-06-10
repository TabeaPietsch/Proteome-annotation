Read Me for the database building scripts

To build a new database go to uniprot.org, select proteomes, and search for the wanted proteomes.
Select "reference proteomes" on the left hand side, if you are looking for gene annotated sequences. Download
the results list with the UP ID.

# 1. uniprot_fasta_download.py

This script reads a list of IDs from the previously downloaded search results tsv file and downloads
the respective proteome fasta files from uniprot. The file name for every downloaded fasta file is:
"uniprot_proteome_<organism name from results file>_<upID from results file>"

Make sure there are no backslashes in the organism names, as these might cause problems in file handling.

### Command line usage:
-i --input  
    A tsv file containing a list of Proteome IDs to be downloaded.  

-o --output  
    The name of your output directory. A new directory will be created if it does not exist yet.

# 2. merge_fasta_files.py

This script merges all fasta files from a defined directory into one single fasta file.

### Command line usage:
-d --directory  
    The path to your directory.  
    
-o --output  
    The name for your output fasta file.

# 3. clean_database_fasta.py

This script reads a fasta file and filters out sequences without a proper gene ID (Every gene ID with an
underscore in the name is kicked out). This works for Diamond annotated files to differentiate between locus
tags and gene names, because diamond gene names do not have underscores in the name. Please check if there are
gene names with underscores in the name before using the cleanup script on files that were not created with diamond.

Edit: The locus tag filter might need to be improved to handle locus tags without an underscore.

### Command line usage:
-f --fastafile  
    The path to your fasta file to be filtered.   
    
-o --output  
    The name for your output fasta file.
