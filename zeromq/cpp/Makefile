CXX=g++
INC=-I/home/jenkovaa/csc-spack/install-tree/gcc-9.1.0/cppzmq-4.3.0-suvgls/include/ 
INC+=-I/home/jenkovaa/csc-spack/install-tree/gcc-9.1.0/libzmq-4.2.5-p7ek76/include
LIBDIR=-L/home/jenkovaa/csc-spack/install-tree/gcc-9.1.0/libzmq-4.2.5-p7ek76/lib/
LIB=-lzmq

EXE=cmodule

all: $(EXE)

$(EXE): module.cpp
	$(CXX) -o $@ module.cpp $(INC) $(LIBDIR) $(LIB)
