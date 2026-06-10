Foldseek annotation was performed with a fasta file of remaining unannotated accessions. To get foldseek results files, go to the
foldseek website, input your fasta file, click "predict" and select your prefered databases for structural alignment. Alternatively,
you can input pdb files, or check out the foldseek documentation on github.

It is assumed that foldseek results are one or more tsv files with the following columns:

1. Query: input protein
2. Target: AlphaFold protein
3. fident: identity in %
4. alnlen: number of aligned residues
5. mismatch: number of mismatched positions
6. gapopen: No gap openings
7+8. Query range: Match covers residues x to y of the protein (7. qstart, 8. qend)
9+10. Target range: Match covers residues x to y of target structure (9. tstart, 10. tend)
11. evalue
12. bits: alignment score

# filter_foldseek_results.py

To filter the multiple results per accession, e-values higher than 10^-5 are eliminated. The best match per accession
is then selected by sorting all remaining results per accession for their bit score and align length and saving the
best score.

### Command line usage:
Please follow the input prompts and use integers for the first question of how many files to process.
        
