#!/bin/bash

set -e

# Process the measurement results
./run-in-dune-env process_measurements.py

# Move it to the correct subfolder
cp floprates.csv doftimes.csv ./haswell-poisson

# And delete all intermediate data
rm *.csv
