#!/bin/bash 
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
#SBATCH --time 00:10:00
#SBATCH --mem 10G
#SBATCH --array=0-24
#SBATCH -o origxyz_%a.out
#SBATCH -e origxyz_%a.err
#SBATCH --job-name=ausfrogs
#SBATCH --mail-type=ALL
#SBATCH --mail-user=thejasvi.beleyur@ab.mpg.de

module load anaconda/3/2020.02
export LIBIOMP5_PATH=$ANACONDA_HOME/lib/libiomp5.so

# activate the environment 
conda init bash

source ~/.bashrc
conda activate /u/tbeleyur/conda-envs/fresh/

# and now run the file 
cd /u/tbeleyur/ausfrogs_pydatemm/
# setup the parameter files 
python preparing_parametersets_esfpond.py
# run one of the parameter files
python -m pydatemm -paramfile ausfrogs_param_n_output/ausfrogs_$SLURM_ARRAY_TASK_ID.yaml


