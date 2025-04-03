from pathlib import Path
import os
output_pfx = str(Path(os.path.abspath("preprocessed_data"))/"chr20_21_22_uint8_distinct_byte-level")
output_yaml = f"""
- dataset_prefix: {output_pfx}_train
  dataset_split: train
  dataset_weight: 1.0
- dataset_prefix: {output_pfx}_val
  dataset_split: validation
  dataset_weight: 1.0
- dataset_prefix: {output_pfx}_test
  dataset_split: test
  dataset_weight: 1.0
"""
with open("training_data_config.yaml", "w") as f:
    print(output_yaml, file=f)
