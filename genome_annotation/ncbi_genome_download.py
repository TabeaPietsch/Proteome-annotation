import requests
import argparse
import io
import zipfile

#----- Configuration --------#

parser = argparse.ArgumentParser()
parser.add_argument('-ak', '--apikey', help= "Please enter your ncbi api key (can be generated in your ncbi profile).")
parser.add_argument('-acc', '--accession', help= "Please enter the genome assembly accession to be downloaded.")

args = parser.parse_args()

apikey = args.apikey
accession = args.accession


# process accession
NCBI_url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/{accession}/download?api_key={apikey}"

# depending on what you want to download, add or delete params from the list
# possible annotation types are:  DEFAULT ┃ GENOME_GFF ┃ GENOME_GBFF ┃ RNA_FASTA ┃ PROT_FASTA ┃ GENOME_GTF ┃
# CDS_FASTA ┃ GENOME_FASTA ┃ SEQUENCE_REPORT
params = {"include_annotation_type":
          ["GENOME_FASTA", "GENOME_GTF"]
    }

response = requests.get(NCBI_url, params=params)

if response.status_code == 200:
   
    zip_bytes = response.content

    print("Download complete. Extracting package...")
    
    # extract zip file with io.BytesIO
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
        z.extractall(path=f"./genome_{accession}")
        
        print("\nExtracted files:")
        for file_info in z.infolist():
            print(f" - {file_info.filename}")
            
    print(f"\nDone! Files saved in: ./genome_{accession}")


elif response.status_code == 404:
    print("The requested accession was not found.")
else:
    print(f"Failed with status code: {response.status_code}")