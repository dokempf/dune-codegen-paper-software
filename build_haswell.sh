ml gcc/6.4.0
ml benchmark/1.4.0
ml python/3.6.3
ml openmpi
ml cmake
ml openblas
ml metis
ml suite-sparse
ml superlu
ml parmetis

SuiteSparse_ROOT=$SUITESPARSE_DIR
MAKE_FLAGS=-j40 ./dune-common/bin/dunecontrol --module=dune-codegen-paper --builddir=$(pwd)/build --opts=./opts/haswell.opts all

pushd build/dune-codegen-paper
make -j40 haswell_poisson
make -j40 haswell_stokes
make -j40 costmodel_verification_poisson
make -j40 costmodel_verification_poisson_skeleton
popd
