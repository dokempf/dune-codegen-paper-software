#!/bin/bash

# IMPORTANT
# Remember to set the working directory of this script to
# the top level build directory of dune-perftool-paperplots
# through:
# sbatch -D <workdir>

# Set a name for the job
#SBATCH -J haswell_poisson

# Number of processes
#SBATCH -n 32

# Choose the SLURM partition (sinfo for overview)
#SBATCH -p haswell16c

# Each process needs two PUs: circumvent hyperthreading
#SBATCH -c 2

set -e

# Load modules
ml gcc/6.4.0
ml python/3.6.3
ml openmpi
ml cmake
ml openblas
ml metis
ml suite-sparse
ml superlu

# Pin processes to cores
# (Possible values: socket, core)
SRUNOPT="--cpu_bind=verbose,core"

# Delete old measurement results
rm -f *.csv

# Search for runnable executables and execute all of them
FILES=$(ls ./haswell-poisson/*.ini)
for inifile in $FILES
do
  line=$(grep ^"opcounter = " $inifile)
  extract=${line##opcounter = }
  UPPER=10
  if [ $extract -eq 1 ]
  then
    UPPER=1
  fi
  COUNT=0
  while [ $COUNT -lt $UPPER ]; do
    exec=${inifile%.ini}
    srun $SRUNOPT ./$exec $inifile
    COUNT=$((COUNT + 1))
  done
done
