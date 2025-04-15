import os
import subprocess

## Download some fasta sequence
concat_path = "chr20_21_22.fa"

if not os.path.exists(concat_path):
    # Download the files
    urls = [
        "https://hgdownload.soe.ucsc.edu/goldenpath/hg38/chromosomes/chr20.fa.gz",
        "https://hgdownload.soe.ucsc.edu/goldenpath/hg38/chromosomes/chr21.fa.gz",
        "https://hgdownload.soe.ucsc.edu/goldenpath/hg38/chromosomes/chr22.fa.gz"
    ]
    
    for url in urls:
        subprocess.run(["wget", url], check=True)

    # Decompress the files
    for chr_num in ["20", "21", "22"]:
        subprocess.run(["zcat", f"chr{chr_num}.fa.gz"], stdout=open(f"chr{chr_num}.fa", "w"), check=True)

    # Concatenate the files
    with open(concat_path, "w") as outfile:
        for chr_num in ["20", "21", "22"]:
            with open(f"chr{chr_num}.fa", "r") as infile:
                outfile.write(infile.read())

print("File creation complete:", concat_path)


