echo "============= START BUILD ============="
echo "Compiler: ${CXX}"

which gcc
which g++
which qmake
mkdir -p $PREFIX/bin
qmake
make
cp src/exdir-browser $PREFIX/bin/exdir-browser
