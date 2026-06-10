import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import argparse

#---------- functions -------------------------

def download_single_proteome(p_id, organism_name, output_dir, base_url):
    """Worker function to handle a single download."""

    # 1. CLEAN ORGANISM NAME: Split at '(' and take everything before it, then strip extra spaces
    clean_org_name = organism_name.split("(")[0].strip()

    # Replace any spaces with underscores so the file path is clean
    clean_org_name = clean_org_name.replace(" ", "_")

    # Define the final target file path
    file_path = os.path.join(output_dir, f"uniprot_proteome_{clean_org_name}_{p_id}.fasta")

    # 2. SKIP IF ALREADY DOWNLOADED
    if os.path.exists(file_path):
        # Return True but specify it was skipped so the main loop knows
        return True, f"Skipped (Already exists): {p_id}"

    params = {
        'format': 'fasta',
        'query': f'proteome:{p_id}'
    }

    try:
        # Use stream=True to stay RAM-safe
        response = requests.get(base_url, params=params, stream=True, timeout=30)

        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True, p_id
        else:
            return False, f"Failed for {p_id}. Status code: {response.status_code}"

    except Exception as e:
        return False, f"Error downloading {p_id}: {e}"


def download_uniprot_proteomes(proteome_ids, organism_names, output_dir):
    """
    Downloads proteome FASTA files from UniProt concurrently using threads.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_url = "https://rest.uniprot.org/uniprotkb/stream"

    # max_workers=4 is safe and polite for UniProt's servers while giving a ~4x speedup
    max_workers = 4

    print(f"Starting concurrent download with {max_workers} parallel workers...")

    # We use ThreadPoolExecutor to manage parallel downloads
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks to the executor pool
        futures = {
            executor.submit(download_single_proteome, p_id, organism_names[i], output_dir, base_url): p_id
            for i, p_id in enumerate(proteome_ids)
        }

        # Wrap as_completed in tqdm to track overall progress dynamically
        for future in tqdm(as_completed(futures), total=len(futures), desc="downloading proteomes"):
            success, message = future.result()
            if not success:
                print(f"\n[WARNING] {message}")


#--------------- main ------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', help= "Please enter the path to your tsv file containing the list of Proteome IDs to be downloaded")
parser.add_argument('-o', '--output', help= "Please enter the name for your output directory. If it does not exist yet, a new directory will be created.")
args = parser.parse_args()
proteomes_list_path = args.input
output_dir = args.output

proteomes_list_df = pd.read_csv(proteomes_list_path, sep="\t")
# list of strings (uniprot IDs)
proteome_ids_list = list(proteomes_list_df["Proteome Id"])
# list of string (organism names)
organism_names_list = list(proteomes_list_df["Organism"])


download_uniprot_proteomes(proteome_ids_list, organism_names_list, output_dir)