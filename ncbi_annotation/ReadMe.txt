1. NCBI_API-Connector.py

    This API-Connector accesses the NCBI v2 REST API at endpoint <protein/dataset_report> to get gene names if available.
    The output is a tsv file containing the columns <accessions>, <gene_name>.

    Command line usage:
    -ak --apikey
        Enter your NCBI apikey, generated in your NCBI profile.
    -i --input
        Enter the tsv file path to be processed. One single column of accessions (No header).
    -o --output
        Enter a name for your output file.

    Input "Collect only annotated accessions [y/n]? If 'n': accessions without a gene name will be added with an empty entry."

    -Write "y" and press enter to collect only annotated accessions and gene names.
    -Write "n" and press enter to collect all accessions (<gene_name> and <None>).


2. tsv_to_unannotated_fasta.py

    This Script takes a tsv files with columns <accessions>, <gene_name>, as well as a fasta files. If an accession has no gene name
    entry, The respective entry within the fasta file is collected. The output is a filtered fasta file containing only the unannotated
    accessions entries of header and sequence.

    Command line usage:
    -f --fastafile
        Enter the path of the reference fasta file.
    -t --tsvfile
        Enter the path of the tsv file containing the annotation information.


3. crossreference_NCBI_diamond.py

    This Script compares NCBI and diamond results and how they match. The output is a graph showing how many accessions
    match and how many gene names match from both sources.

    Command line usage:
        No argument parser was added here because of too many paths to process. Please adjust the paths within the scriptaccording
        to your defined file names.