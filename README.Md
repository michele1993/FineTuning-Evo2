# Evo2 NVIDIA fine-tuning tutorial

To my knowledge, the only available script to fine-tune evo2 is provided via the **NVIDIA BioNeMo Framework** (i.e,  [here](https://docs.nvidia.com/bionemo-framework/latest/user-guide/examples/bionemo-evo2/fine-tuning-tutorial/)). Here, I describe how to install this framework on the CRG cluster, so that we can then run the evo2 fine-tune script on the cluster (and hopefully adapt it to our needs). 
I also include a step to step guidance on how to run the actual script (see Evo2 fine-tuning tutorial section below).

## Installation

We first need to set-up the **NVIDIA BioNeMo Framework** , which includes all the API (e.g, scripts) to fine-tune evo2.

### BioNeMo Framework

- a free-to-use collection of programming tools and packages offering access to optimized, pre-trained biomolecular models and workflows.

**Set-up**

Fortunately, the Bionemo framework is provided as a Docker container, including all the necessary dependencies. Although the CRG cluster does not have Docker, we can use this container via Apptainer (Singularity), which is installed in the cluster (see [here](https://developer.nvidia.com/blog/docker-compatibility-singularity-hpc/) for more info on how to run docker Bionemo containers in Apptainer/Singularity).

In order to access this (Bionemo framework) container, we need to perform the following steps: 

1. Create a **free** account on [NGC](https://ngc.nvidia.com/signin) (just insert your email address to create a new account if don't have one)

2. Log in & generate API KEY by going to **User** (top right corner where you email address is displayed) **> Setup > Generate API Key, then click + Generate API Key and Confirm**. Store the API Key in a secure location (we gonna need it)

3. Log in CRG cluster and then add the docker username (don't worry about this, it is autogenerated) and the API key that you generated in step 2. as environment variables. The easiest way to do this is to 
	add these variables to your `.bash_profile` file in the home directory, `$HOME` (i.e., where you login). 
	To do so, open your `~/.bash_profile` with your preferred editor (e.g., vim) and paste the following, (if you don't have a `.bash_profile` file in home dir, create one),
```
export NGC_API_KEY= GENERATED_API_KEY
export SINGULARITY_DOCKER_USERNAME='$oauthtoken'
export SINGULARITY_DOCKER_PASSWORD="$NGC_API_KEY"
```
where you **need to insert** the generated API Key of step 2 instead of `GENERATED_API_KEY` in the first line.

**IMPORTANT** To prevent Apptainer from running out of memory in your home directory, you should also set the following variables in your `.bash_profile`, ensuring Apptainer `cache` and  `tmp` are stored in the much bigger `no_backup` directory,
```
export APPTAINER_CACHEDIR="/no_backup/YOUR_GROUP_NAME/YOUR_USER_NAME"
export APPTAINER_TMPDIR="/no_backup/YOUR_GROUP_NAME/YOUR_USER_NAME"
```
where you should fill `/YOUR_GROUP_NAME/YOUR_USER_NAME` appropriately (**Note** if you don't have a `/no_backup` folder for your username send a ticket to IT to create one).

Next run,
```
source ~/.bash_profile
```

to load the changes (After this, if you run `echo $SINGULARITY_DOCKER_PASSWORD` your generated API KEY should appear).

**Note** if you don't want to have these variables in your `.bash_profile`, I recommend using [direnv](https://direnv.net/docs/installation.html) which you can easily install in the CRG cluster from binary without sudo privileges.

4. Now that we have set the correct variables, we can finally download the BioNemoFramework container by pulling this container with Apptainer (installed in the cluster). To do so, run the following,
```
apptainer pull docker://nvcr.io/nvidia/clara/bionemo-framework:2.5
```
This is going to take a while (i.e, 16GB), in my case it took roughly 40 min to complete. If this process completes correctly, you should have a `bionemo-framework_2.5.sif` file in your current directory.

5. In `bionemo-framework_2.5.sif`, we have the entire BioNeMo Framework inside a container that we can run in the CRG cluster with Apptainer, including  all the dependencies needed to run the NVIDIA fine-tune evo2 tutorial (and extend it to any custom dataset).

From here you can use this container as it suits you (no only for evo2 but for any BioNeMo model/functionality).Below I include the steps on how I reproduced the actual NVIDIA evo2 fine-tune [tutorial](https://docs.nvidia.com/bionemo-framework/latest/user-guide/examples/bionemo-evo2/fine-tuning-tutorial/) using this container.

## Evo2 fine-tuning tutorial

Now that we have access to the **NVIDIA BioNeMo Framework**, we can use it to run the evo2 fine-tuning [tutorial](https://docs.nvidia.com/bionemo-framework/latest/user-guide/examples/bionemo-evo2/fine-tuning-tutorial/).

We can do this by asking for an interactive job on the CRG cluster, asking for at least a GPU with 40GB GPU.

Once, you are granted the interactive node, execute the following to run the container interactively (should be run from the directory where you stored the `bionemo-framework_2.5.sif` file),
```
apptainer shell --nv bionemo-framework_2.5.sif
```
This will open a shell from inside the container with access to all the Bionemo functionalities. Since we asked for an interactive node, we can run stuff directly from this "Apptainer" shell, which will be executed by the interactive node.
From inside here, you have access to all the scripts/functions used in the NVIDIA tutorial. Since I don't want to run a JupiterNotebook, I created corresponding python scripts to perform all the required operations (you can find these scripts in this repo). Using these scripts, you should run the following,
```
python get_data.py
```
**NOTE** the `get_data.py` download some `.fasta` dataset, you can edit this to use your custom dataset. The important thing is that you create an appropriate `preprocess_config.yaml` for the next (preprocessing) step,
```
preprocess_evo2 --config preprocess_config.yaml
```

**Select evo2 checkpoint**
Next, you need to specify the evo2 checkpoint, you want to download. 
In this case, they use the `1b` model (**only need to run this once**),
```
evo2_convert_to_nemo2 --model-path hf://arcinstitute/savanna_evo2_1b_base  --model-size 1b --output-dir nemo2_evo2_1b_8k
```
**Important** here you can specify any evo2 checkpoint from hugging face (e.g, 7b, 40b).

**Configure the training and validation set**
```
python create_training_config.py
```

and finally you can start the fine-tuning process by running,
```
train_evo.py
```

At the end of training, you can find the tensorboard log file by running,
```
find pretraining_demo -name "events.out.tfevents*"
```
Next, you can download this on your local machine and visualise it with tensorboard.

**IMPORTANT** In this tutorial, they show the `1b` evo2 checkpoint is sensitive to `--fp8`, unlike the `7b` checkpoint (and `40b` ?). So you should only use the 1-billion checkpoint if you used FP8 enables (i.e., how it was trained)` or maybe find the newer corrected `1b` checkpoint if available. Alternatively, you need to use the 7-billion checkpoint, which does not suffer from this limitation and seems robust to FP8 being activated or not.

Finally, here I used an interactive session for simplicity, but everything can be adapted to a job submission, using the appropriate Apptainer commands.
