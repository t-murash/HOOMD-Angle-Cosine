# HOOMD-Angle-Cosine

## Installation
Get HOOMD's source file.
```
$ wget https://glotzerlab.engin.umich.edu/Downloads/hoomd/hoomd-v2.9.6.tar.gz
$ tar zxvf hoomd-v2.9.6.tar.gz
```

Put source files of HOOMD-Angle-Cosine to HOOMD's `hoomd/md` directory.

```
$ git clone https://github.com/t-murash/HOOMD-Angle-Cosine.git
$ cp HOOMD-Angle-Cosine/src/* hoomd-blue-v2.9.6/hoomd/md/*
```

Then, build HOOMD

```
$ cd hoomd-blue-v2.9.6
$ mkdir build
$ cd build
$ cmake ../ -DCMAKE_INSTALL_PREFIX=`python3 -c "import site; print(site.getsitepackages()[0])"` \
-DCMAKE_CXX_FLAGS="-march=native" -DCMAKE_C_FLAGS="-march=native" -DENABLE_CUDA=ON \
-DCUDA_TOOLKIT_ROOT_DIR=/usr/lib/nvidia-cuda-toolkit -DENABLE_MPI=OFF -DSINGLE_PRECISION=ON
$ make -j64
$ ctest
$ make -j64 install
```

## Note
You need to modify `/usr/include/crt/host.config.h` before building HOOMD.

L138
```
#error -- unsupported GNU version!
```
should be comented out.
```
// #error -- unsupported GNU version!
```



