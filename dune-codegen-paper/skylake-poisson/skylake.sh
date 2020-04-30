#!/bin/bash

# Pass the top level build directory of dune-perftool-paperplots
# to this script as the first and only argument!
cd $1

# Load MPI
#module load mpi/openmpi-x86_64

# Remove any csv data
rm -f *.csv

# Search for runnable executables
FILES=$(ls ./skylake-poisson/*.ini)
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
    MAXCORES=40
    mpirun --bind-to core -np $MAXCORES ./$exec $inifile
    COUNT=$((COUNT + 1))
  done
done

# Process the measurement results
./run-in-dune-env process_measurements.py

# Move it to the correct subfolder
cp floprates.csv doftimes.csv ./skylake-poisson

# And delete all intermediate data
rm *.csv
