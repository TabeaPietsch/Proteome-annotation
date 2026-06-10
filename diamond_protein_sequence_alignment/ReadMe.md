# alignment_results_to_excel.py

Merge diamond information from database fasta and results tsvs (combined in one excel file).

This script assumes the defined fasta file is the one used to create the diamond database.
The new sheets in the excel file are the e-value filtered results from diamond protein sequence alignment. It is assumed that the
input excel file contains all results from diamond, with one sheet per diamond input (e.g. 9 bacteria proteomes aligned separately
via diamond = 9 sheets).

### Command line usage:
-e --excelfile  
    The path to your unfiltered diamond results combined in one excel file with multiple sheets.  
    
-f --fastafile  
    The path to your diamond database fasta file.   
    
-o --output  
    The name for the new output excel file.
