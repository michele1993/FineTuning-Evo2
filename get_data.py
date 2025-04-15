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

## Create necessary `.yaml` config file
full_fasta_path = os.path.abspath(concat_path)
output_dir = os.path.abspath("preprocessed_data")
output_yaml = f"""
- datapaths: ["{full_fasta_path}"]
  output_dir: "{output_dir}"
  output_prefix: chr20_21_22_uint8_distinct
  train_split: 0.9
  valid_split: 0.05
  test_split: 0.05
  overwrite: True
  embed_reverse_complement: true
  random_reverse_complement: 0.0
  random_lineage_dropout: 0.0
  include_sequence_id: false
  transcribe: "back_transcribe"
  force_uppercase: false
  indexed_dataset_dtype: "uint8"
  tokenizer_type: "Byte-Level"
  vocab_file: null
  vocab_size: null
  merges_file: null
  pretrained_tokenizer_model: null
  special_tokens: null
  fast_hf_tokenizer: true
  append_eod: true
  enforce_sample_length: null
  ftfy: false
  workers: 1
  preproc_concurrency: 100000
  chunksize: 25
  drop_empty_sequences: true
  nnn_filter: false  # If you split your fasta on NNN (in human these are contigs), then you should set this to true.
  seed: 12342  # Not relevant because we are not using random reverse complement or lineage dropout.
"""
with open("preprocess_config.yaml", "w") as f:
    print(output_yaml, file=f)
