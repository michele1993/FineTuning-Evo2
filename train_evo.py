import os
import subprocess

root_dir = os.path.dirname(os.path.abspath(__file__)) 
config_file_dir = os.path.join(root_dir,"training_data_config.yaml")

assert os.path.exists(config_file_dir), f"Error need to create training_config.yaml file first" 

# Set FAST_CI_MODE before running the script, or default to False
FAST_CI_MODE = os.getenv("FAST_CI_MODE", "False").lower() in ("true", "1", "yes")

# Define training parameters
MAX_STEPS: int = 10 if FAST_CI_MODE else 100
val_check_interval = min(int(MAX_STEPS // 2), 50)
warmup_steps = min(MAX_STEPS, 100)

# Set model subset options based on FAST_CI_MODE
if FAST_CI_MODE:
    model_subset_option = "--num-layers 4 --hybrid-override-pattern SDH* --activation-checkpoint-recompute-num-layers 2"
else:
    model_subset_option = "--activation-checkpoint-recompute-num-layers 5"

# Construct the training command
train_cmd = f"""train_evo2 \
    -d training_data_config.yaml \
    --dataset-dir ./preprocessed_data \
    --experiment-dir pretraining_demo \
    --model-size 1b \
    --devices 1 \
    --num-nodes 1 \
    --seq-length 8192 \
    --micro-batch-size 2 \
    --lr 0.000015 \
    --min-lr 0.0000149 \
    --warmup-steps {warmup_steps} \
    --grad-acc-batches 4 \
    --max-steps {MAX_STEPS} \
    --ckpt-dir nemo2_evo2_1b_8k \
    --clip-grad 250 \
    --wd 0.001 \
    --attention-dropout 0.01 \
    --hidden-dropout 0.01 \
    --val-check-interval {val_check_interval} \
    {model_subset_option} \
    --ckpt-async-save \
    --no-wandb"""

# Execute the command
subprocess.run(train_cmd, shell=True, check=True)

