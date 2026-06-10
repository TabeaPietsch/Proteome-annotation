import pandas as pd
import re
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

#------- Configuration

excel_file = r"\diamond_protein_sequence_alignment\merged_output_bacteroidota_unique.xlsx"

sheet_names = [
    "1out_bacteroidota_LowE",
    "2out_bacteroidota_LowE",
    "3out_bacteroidota_LowE",
    "4out_bacteroidota_LowE",
    "5out_bacteroidota_LowE",
    "6out_bacteroidota_LowE",
    "7out_bacteroidota_LowE",
    "8out_bacteroidota_LowE",
    "9out_bacteroidota_LowE"
]

NCBI_annotation_paths = [
    "1_GCF-original_annotated.tsv",
    "2_GCF-original_annotated.tsv",
    "3_GCF-original_annotated.tsv",
    "4_GCF-original_annotated.tsv",
    "5_GCF-original_annotated.tsv",
    "6_GCF-original_annotated.tsv",
    "7_GCF-original_annotated.tsv",
    "8_GCF-original_annotated.tsv",
    "9_GCF-original_annotated.tsv"
    ]


#-------- functions

def smart_match(query_gene, ncbi_gene):
    """
    Checks if query_gene matches the ncbi_gene exactly OR matches any individual
    component segment (separated by spaces, underscores, or hyphens).
    Prevents 'era' -> 'transferase', but allows 'rpm' -> 'rpm_er_2'.
    """
    if pd.isna(query_gene) or pd.isna(ncbi_gene):
        return False

    # Standardize to lowercase and strip whitespace
    q = str(query_gene).strip().lower()
    n = str(ncbi_gene).strip().lower()

    # 1. Check for a perfect direct match
    if q == n:
        return True

    # 2. Split the NCBI name into segments using a regular expression.
    # This splits by spaces, underscores (_), and hyphens (-)
    # e.g., "rpm_er_2" becomes ['rpm', 'er', '2']
    ncbi_segments = re.split(r"[\s_\-]+", n)

    # 3. Check if our exact query name is one of those segments
    if q in ncbi_segments:
        return True

    return False


#------------ process all samples

plot_sheets = []
plot_gene_percentages = []
plot_accession_percentages = []

for sample in tqdm(range(9)):
    print(f"--- Processing Sample {sample+1} ---")
    gene_match_count = 0
    accession_match_count = 0

    # 1. Read Excel alignment file
    alignment_df = pd.read_excel(excel_file, sheet_name=sheet_names[sample])

    # 2. Read NCBI annotation file
    ncbi_df = pd.read_csv(
        NCBI_annotation_paths[sample], sep="\t", header=None
    )
    ncbi_df.columns = ["Accession", "GeneName"]
    # NCBI Accessions are already version free and do not need to be cleaned

    # 3. Create a lookup dictionary: { Accession: GeneName }
    ncbi_lookup = dict(zip(ncbi_df["Accession"], ncbi_df["GeneName"]))

    # 4. Iterate through alignment rows securely
    for idx, row in alignment_df.iterrows():
        # Get accession and clean it to match NCBI format
        raw_accession = str(row["Query Accession "]).strip()
        align_accession = raw_accession.split(".")[0]

        align_gene = row["gene_id"]

        # Look up the corresponding gene name from NCBI using the Accession ID
        if align_accession in ncbi_lookup:
            accession_match_count += 1
            ncbi_gene = ncbi_lookup[align_accession]

            # Use whole-word matching function for the match search
            if smart_match(align_gene, ncbi_gene):
                print(
                    f"Match found for {align_accession}: '{align_gene}' (align) matches '{ncbi_gene}' (NCBI)"
                )
                gene_match_count += 1
        else:
            # Optional: handle accessions that exist in alignment but missing in NCBI report
            pass

    align_gene_length = len(alignment_df.iloc[:,0].tolist())
    NCBI_gene_length = len(ncbi_df["GeneName"].tolist())
    print(f"gene matches: {gene_match_count}/{min(align_gene_length, NCBI_gene_length)} \n"
          f"accession matches: {accession_match_count}/{min(align_gene_length, NCBI_gene_length)}"
          f"total lengths: {align_gene_length} (align) {NCBI_gene_length} (NCBI)")

    # append sheet info
    plot_sheets.append(f"sample{sample+1}")
    plot_gene_percentages.append(gene_match_count/min(align_gene_length, NCBI_gene_length)*100)
    plot_accession_percentages.append(accession_match_count/min(align_gene_length, NCBI_gene_length)*100)


#-------------- bar graph with match info for all 9 files/ sheets -------#

# Define positions for the bars
x = np.arange(len(plot_sheets))
width = 0.35  # Width of each individual bar

# Create subplots to establish the figure structure neatly
fig, ax = plt.subplots(figsize=(12, 6))

# Plot both sets of bars side-by-side by offsetting their x positions
rects1 = ax.bar(
    x - width / 2,
    plot_gene_percentages,
    width,
    label="Gene Name Matches",
    #color="#4c72b0",
)
rects2 = ax.bar(
    x + width / 2,
    plot_accession_percentages,
    width,
    label="Accession Matches",
    #color="#c44e52",
)

# Customize chart details
ax.set_ylabel("Matches [%]", fontsize=12)
ax.set_title("Gene and accession matches across samples", fontsize=14)
ax.set_xticks(x)

# Rotate labels slightly so long sheet names don't overlap or get truncated
ax.set_xticklabels(plot_sheets, rotation=30, ha="right", fontsize=10)
ax.legend(
    loc= "center left",
    bbox_to_anchor= (1.05, 1),
    fontsize=11)
ax.grid(axis="y", linestyle="--", alpha=0.7)  # Add a subtle grid for readability

# Save your plot directly to a file
plt.savefig("match_counts_plot2.png", dpi=300, bbox_inches="tight")
print("\nPlot successfully generated and saved as 'match_counts_plot.png'!")