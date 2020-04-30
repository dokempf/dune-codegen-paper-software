MAKE_FLAGS=-j40 ./dune-common/bin/dunecontrol --opts=skylake.opts --builddir=$(pwd)/build --module=dune-codegen-paper all

# Spin up the autotune build server that runs exclusively on socket 0 and have code generation happen exclusively
# on socket 1. Communication between the two is realized through the file system, see the server implementation
hwloc-bind socket:0 ./dune-codegen-paper/autotune-scripts/autotune_build_server.py mpirun --bind-to core -np 20 &
sleep 0.2

AUTOTUNE_MAKE="hwloc-bind socket:1 make -j20"

pushd build/dune-codegen-paper
$AUTOTUNE_MAKE skylake_poisson
$AUTOTUNE_MAKE skylake_stokes
popd

echo "exit" >> tasks.txt
