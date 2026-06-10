# 1. collect_unannotated_accession_queries.py

This script filters out unannotated accessions from input fasta files by checking if the respective accession can be found
in the defined excel file. It is assumed that the number of fasta files is equal to the number of sheets in the excel file, and that the
excel file only contains annotated accessions. The first fasta file entered in the command line will be compared with hte first
sheet in the excel file.
The results will be saved as one tsv file per fasta file, containing the unannotated accessions.

### Command line usage:
-f --fastafile  
    Enter one or more paths of your input fasta files, separated by spaces.  
    
-e --excelfile  
    Enter the path to your excel file.  
    
-n --name  
    Enter the name of the column containing the query accessions to be compared with the accessions from the fasta file
    (">WP..." at the start of the header within the fasta files, "WP..." in your excel file.)
    Please use parantheses for the column name if it contains spaces.


# 2. read_accessions_from_fasta.py

This script returns a tsv file containing all accessions ("WP..") found in the input fasta file.

### Command line usage:
-i --input  
    Enter the path of the wanted fasta file.  
    
-o --output  
    Enter a name for your output tsv file.


# 3. merge_annotation_outputs.py

This script merges information from NCBI, sequence alignment (diamond), and structural alignment (foldseek).

### Command line usage:
No argument parser was added here because of too many paths to process. Please change the paths within the script
according to your defined file names of the output files.
