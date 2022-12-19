# HOOMD-Angle-Cosine
This package is a patch for HOOMD-blue, providing an angle potential<br>
<img src="https://latex.codecogs.com/gif.latex?&space;U(\theta)=K[1-\cos(\theta-\theta_0)]" />, <br>
which is commonly used in polymer's community.


<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/movie.gif width=400px alt="Demo">

red: (k=10, &theta;<sub>0</sub>=0), green: (k=0, &theta;<sub>0</sub>=0), blue: (k=-10, &theta;<sub>0</sub>=0)

<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/hoomd-angle-cosine.png width=400px alt="Def.">

Authored by:
[Takahiro Murashima](https://github.com/t-murash)<br>
Tohoku University, Japan<br>
Initial commit: Mar 23, 2021<br>
Last updated: Dec 19, 2022<br>
Support provided via [issues](https://github.com/t-murash/HOOMD-Angle-Cosine/issues) and/or [email](mailto:murasima@cmpt.phys.tohoku.ac.jp).


## Installation
Get HOOMD-blue's source file.
```
$ wget https://glotzerlab.engin.umich.edu/Downloads/hoomd/hoomd-v3.7.0.tar.gz
$ tar zxvf hoomd-v3.7.0.tar.gz
```

Put source files of HOOMD-Angle-Cosine to HOOMD's `hoomd/md` directory.

```
$ git clone https://github.com/t-murash/HOOMD-Angle-Cosine.git
$ cp HOOMD-Angle-Cosine/src/* hoomd-blue-v3.7.0/hoomd/md/*
```

Then, build HOOMD

```
$ cd hoomd-blue-v3.7.0
$ mkdir build
$ cd build
$ cmake ../ -DCMAKE_INSTALL_PREFIX=`python3 -c "import site; print(site.getsitepackages()[0])"` -DCMAKE_CXX_FLAGS="-march=native" -DCMAKE_C_FLAGS="-march=native" -DENABLE_GPU=ON -DENABLE_MPI=OFF -DSINGLE_PRECISION=ON
$ make -j64
$ ctest
$ make -j64 install
```

## Usage
```
$ python example/angle-cosine-test.py
```
Please see `example/angle-cosine-test.py`.

## Technical note
- [Derivation of angle force field](https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/Angle-Cosine.pdf)

## Troubleshoot
If you meet "unsupported GNU version" error, you need to modify `/usr/include/crt/host.config.h` before building HOOMD-blue.

L138
```
#error -- unsupported GNU version!
```
should be comented out.
```
// #error -- unsupported GNU version!
```


## Citing the HOOMD-Angle-Cosine package

Users of this package are encouraged to cite the following article in scientific publications:

* K. Hagita, T. Murashima, "Molecular Dynamics Simulations of Ring Shapes on a Ring Fraction in Ring-Linear Polymer Blends", *Macromolecules*, (2021) **54** (17) 8043-8051, https://doi.org/10.1021/acs.macromol.1c00656.



