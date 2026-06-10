# ncbi_genome_download.py

This script downloads genome information of a specified genome assembly accession from NCBI via the NCBI Rest API.
The downloaded contents will be saved under ./genome_<accession>.

You can choose from the accessible annotation types by adding or deleting entries from the params dictionary values.
Possible annotation types are:
    DEFAULT ┃ GENOME_GFF ┃ GENOME_GBFF ┃ RNA_FASTA ┃ PROT_FASTA ┃ GENOME_GTF ┃ CDS_FASTA ┃ GENOME_FASTA ┃ SEQUENCE_REPORT

### Command line usage:
-ak --apikey  
    The NCBI apikey generated in your NCBI profile.  

-acc --accession  
    The genome assembly accession of your target genome.
