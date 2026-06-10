import pandas as pd


# read in tsv files

number_results = int(input('How many result files do you have? E.g. "3":'))

files_and_dbs = {}

for amount in range(number_results):
    result = input("Please enter the path to a foldseek results file (tsv): ").strip('"')
    result_name = input("Please enter the name of the result database: ")
    files_and_dbs[result_name] = result


# label columns
column_headers = [
    "query", "target", "fident", "alnlen", "mismatch", "gapopen",
    "qstart", "qend", "tstart", "tend", "evalue", "bits"
]

# process and merge all files
all_dfs = []

for db_name, file_path in files_and_dbs.items():
    # Read in tsv file
    df = pd.read_csv(file_path, sep="\t", header=None)

    # Label columns
    df.columns = column_headers

    # Add respective database name
    df["database"] = db_name

    all_dfs.append(df)

# merge dataframes
foldseek_all_df = pd.concat(all_dfs, ignore_index=True)

# filter out e-values greater than 10^-5
foldseek_all_df_lowE = foldseek_all_df.loc[foldseek_all_df["evalue"] <= 10**-5, :]


# select best match for every accession
# 1. highest bit score 2. highest alignment length
foldseek_df_best_hits = (foldseek_all_df_lowE.sort_values(["bits", "alnlen"], ascending=[False, False])
                        .groupby("query").head(1))

print(foldseek_df_best_hits[["query", "alnlen", "evalue", "bits", "database"]], len(foldseek_all_df))
print(max(foldseek_df_best_hits["evalue"]))

# save filtered foldseek results
output_path = "foldseek_results_best_matches.tsv"
foldseek_df_best_hits.reset_index(drop=True).to_csv(path_or_buf= output_path, sep= "\t", index= False)