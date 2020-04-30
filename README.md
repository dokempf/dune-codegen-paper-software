This repository documents the software stack and the experimental setup
of the manuscript: Automatic Code Generation for High-Performance
Discontinuous Galerkin Methods on Modern Architectures.

It provides the technical details of how the results of the manuscript were
achieved, but reproduction might require adapting its scripts and configuration
files to your computing environment.

In general the procedure is:
* Clone this repository recursively
* Run ./patch.sh
* Run ./build_{haswell,skylake}.sh
* Go into the individual subfolders of build/dune-codegen-paper and apply this procedure to produce a plot:
  * Run the execution script (like `donkey.sbatch` or `skylake.sh`) 
    (watch out for requirements on the working directory...)
  * If there, run `process.sh` to distill the data
  * Copy the resulting `csv` files into the source and commit them through `git-lfs`
  * Run `plot.py` in a suitable env (say through `run-in-dune-env`) to generate pdfs.

