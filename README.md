# HOOMD-Angle-Cosine
This is an extension package for HOOMD-blue, providing an angle potential<br>
<img src="https://latex.codecogs.com/gif.latex?&space;U(\theta)=K[1-\cos(\theta-\theta_0)]" /> <br>
which is commonly used in polymer's community <sup>[1](https://pubs.rsc.org/en/content/articlelanding/1999/CP/a809796h),[2](https://pubs.acs.org/doi/10.1021/ma000058y),[3](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/1439-7641(20010316)2:3%3C180::AID-CPHC180%3E3.0.CO;2-Z),[4](https://pubs.acs.org/doi/10.1021/acs.macromol.9b02428)</sup>.<br>
(This potential is implemented in LAMMPS as [angle_style cosine/delta](https://docs.lammps.org/angle_cosine_delta.html).)


<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/fig/movie.gif width=400px alt="Demo">

Red: (k=10, &theta;<sub>0</sub>=0), Green: (k=0, &theta;<sub>0</sub>=0), Blue: (k=-10, &theta;<sub>0</sub>=0)

<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/fig/hoomd-angle-cosine.png width=400px alt="Def.">

Authored by:
[Takahiro Murashima](https://github.com/t-murash)<br>
Tohoku University, Japan<br>
Initial commit: Mar 23, 2021<br>
Last updated: Apr 20, 2023<br>
Support provided via [issues](https://github.com/t-murash/HOOMD-Angle-Cosine/issues) and/or [email](mailto:murasima@cmpt.phys.tohoku.ac.jp).


## Preparation

```
$ wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
$ bash Miniconda3-latest-Linux-x86_64.sh
$ conda update --all
$ conda create -n hoomd-v3.11 python=3.10
$ conda activate hoomd-v3.11
$ conda install pybind11
$ conda install -c omnia eigen3
$ conda install -c conda-forge cereal
$ conda install numpy
$ conda install -c conda-forge gsd
```


## Installation
Get HOOMD-blue's source file.
```
$ wget https://github.com/glotzerlab/hoomd-blue/releases/download/v3.11.0/hoomd-v3.11.0.tar.gz
$ tar zxvf hoomd-v3.11.0.tar.gz
```

Put source files of HOOMD-Angle-Cosine to HOOMD's `hoomd/md` directory.

```
$ git clone https://github.com/t-murash/HOOMD-Angle-Cosine.git
$ cp HOOMD-Angle-Cosine/src/* hoomd-v3.11.0/hoomd/md/.
```

Then, build HOOMD-blue

```
$ cd hoomd-v3.11.0
$ mkdir build
$ cd build
$ cmake ../ -DCMAKE_INSTALL_PREFIX=`python -c "import site; print(site.getsitepackages()[0])"` -DCMAKE_CXX_FLAGS="-march=native" -DCMAKE_C_FLAGS="-march=native" -DENABLE_GPU=ON -DENABLE_MPI=OFF -DSINGLE_PRECISION=ON
$ make -j64
$ ctest
$ make install
```

## Usage
```
$ python example/angle-cosine-test.py
```
Please see `example/angle-cosine-test.py`.


## Technical note
- [Derivation of angle force field](https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/doc/Angle-Cosine.pdf)

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



