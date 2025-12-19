# HOOMD-Angle-Cosine
This is an extension package for HOOMD-blue, providing an angle potential<br>
$U(\theta)=K[1-\cos(\theta-\theta_0)]$
<br>
which is commonly used in polymer's community <sup>[1](https://pubs.rsc.org/en/content/articlelanding/1999/CP/a809796h),[2](https://pubs.acs.org/doi/10.1021/ma000058y),[3](https://chemistry-europe.onlinelibrary.wiley.com/doi/10.1002/1439-7641(20010316)2:3%3C180::AID-CPHC180%3E3.0.CO;2-Z),[4](https://pubs.acs.org/doi/10.1021/acs.macromol.9b02428)</sup>.<br>
(This potential is implemented in LAMMPS as [angle_style cosine/delta](https://docs.lammps.org/angle_cosine_delta.html).)


<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/fig/movie.gif width=400px alt="Demo">

Red: (k=10, &theta;<sub>0</sub>=0), Green: (k=0, &theta;<sub>0</sub>=0), Blue: (k=-10, &theta;<sub>0</sub>=0)

<img src=https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/fig/hoomd-angle-cosine.png width=400px alt="Def.">

Authored by:
[Takahiro Murashima](https://github.com/t-murash)<br>
Tohoku University, Japan<br>
Initial commit: Mar 23, 2021<br>
Last updated: Dec 19, 2025<br>
Support provided via [issues](https://github.com/t-murash/HOOMD-Angle-Cosine/issues) and/or [email](mailto:murasima@cmpt.phys.tohoku.ac.jp).


## Installation for HOOMD-blue v6.0.0

This section provides instructions for building and installing HOOMD-blue v6.0.0 from source with this extension.

### 0. Install Micromamba
Micromamba is used for managing dependencies. The installation will begin with the next command.
```bash
"${SHELL}" <(curl -L micro.mamba.pm/install.sh)
```
When prompted as below, agree with everything.
```bash
Micromamba binary folder? [~/.local/bin] [Enter]
Init shell (bash)? [Y/n] Y
Configure conda-forge? [Y/n] Y
Prefix location? [~/micromamba] [Enter]
```


Ensure `~/.local/bin` is in your `PATH`.
```bash
export PATH=$HOME/.local/bin:$PATH
```

Create a new micromamba environment for HOOMD-blue v6.0.0.

```bash
micromamba create -n hoomd-v6.0.0 python=3.14
```

### 1. Environment Preparation
Set up your CUDA environment if you have a compatible GPU.
```bash
export CUDA_HOME=/usr/local/cuda-12.6;
export PATH=$CUDA_HOME/bin:$PATH;
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```


### 2. Install Build Dependencies
Install necessary packages using micromamba.
```bash
micromamba activate hoomd-v6.0.0 &&
micromamba install -y -c conda-forge cmake eigen git ninja numpy pybind11 python
```

### 3. Get HOOMD-blue Source Code
Download the HOOMD-blue source code and extract it using tar.
```bash
wget https://github.com/glotzerlab/hoomd-blue/releases/download/v6.0.0/hoomd-6.0.0.tar.gz;
tar zxvf hoomd-6.0.0.tar.gz;
mv hoomd-6.0.0 hoomd-blue
```

### 4. Add HOOMD-Angle-Cosine Source Files
Put the source files of this extension into the `hoomd/md` directory of the HOOMD-blue source tree.
```bash
git clone https://github.com/t-murash/HOOMD-Angle-Cosine.git;
cp HOOMD-Angle-Cosine/src/* hoomd-blue/hoomd/md/.
```

### 5. Configure the Build with CMake
```bash
cd hoomd-blue
``` 
Configure the build using CMake.
```bash
micromamba activate hoomd-v6.0.0
```

```bash
cmake -B build -S . -GNinja \
  -DENABLE_GPU=on \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=$(python -c "import site; print(site.getsitepackages()[0])")
```

### 6. Build and Install
Compile and install HOOMD-blue.
```bash
ninja -C build && ninja -C build install
```

### 7. Verify Installation
Check if the installation was successful.
```python
import hoomd
print(f'HOOMD-blue version: {hoomd.version.version}')
print(f'GPU support: {hoomd.version.gpu_enabled}')
```
Or
```bash
python3 -c "import hoomd; print(f'HOOMD Version: {hoomd.version.version}'); print(f'GPU support: {hoomd.version.gpu_enabled}')"
```
Expected output:
```
HOOMD-blue version: 6.0.0
GPU support: True
```

## Usage

Activate the HOOMD-blue environment
```bash
micromamba activate hoomd-v6.0.0
```

To run the CPU example:
```bash
python angle-cosine-test-v6.py
```

To run the GPU example:
```bash
python angle-cosine-test-v6-gpu.py
```

Please see `example/angle-cosine-test-v6.py` and `example/angle-cosine-test-v6-gpu.py` for details.


## Troubleshoot


### RTX 5090 specific issues

This section describes the patch for running HOOMD-blue v6.0.0 on NVIDIA GeForce RTX 5090.

#### Background
NVIDIA GeForce RTX 5090 (Compute Capability 12.0) has some incompatibilities with HOOMD-blue v6.0.0:
1. RTX 5090 does not support `cudaDevAttrConcurrentManagedAccess` attribute.
2. `cudaSetValidDevices()` may cause unexpected errors.

##### Error message
```bash
Traceback (most recent call last):
  File "/path/to/angle-cosine-test-v6-gpu.py", line 14, in <module>
    device = hoomd.device.GPU()
  File "/path/to/device.py", line 359, in __init__
    self._cpp_exec_conf = _hoomd.ExecutionConfiguration(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        _hoomd.ExecutionConfiguration.executionMode.GPU,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<2 lines>...
        self._cpp_msg,
        ^^^^^^^^^^^^^^
    )
    ^
RuntimeError: No supported GPUs are present on this system.
The device NVIDIA GeForce RTX 5090 does not support managed memory.
```

#### Patch files
The patch files are located in `patch-hoomd-v6.0.0` directory.
This patch includes modifications for `ExecutionConfiguration.cc`, `ExecutionConfiguration.h`, and `Autotuner.h`.

#### How to apply
Replace the files directly.

```bash
# Backup original files
cp hoomd-blue/hoomd/ExecutionConfiguration.cc hoomd-blue/hoomd/ExecutionConfiguration.cc.orig;
cp hoomd-blue/hoomd/ExecutionConfiguration.h hoomd-blue/hoomd/ExecutionConfiguration.h.orig;
cp hoomd-blue/hoomd/Autotuner.h hoomd-blue/hoomd/Autotuner.h.orig;

# Copy modified files
cp HOOMD-Angle-Cosine/patch-hoomd-v6.0.0/hoomd/ExecutionConfiguration.cc hoomd-blue/hoomd/;
cp HOOMD-Angle-Cosine/patch-hoomd-v6.0.0/hoomd/ExecutionConfiguration.h hoomd-blue/hoomd/;
cp HOOMD-Angle-Cosine/patch-hoomd-v6.0.0/hoomd/Autotuner.h hoomd-blue/hoomd/;

# Rebuild
cd hoomd-blue/build; ninja && ninja install;
```

## Note
- [Derivation of angle force field](https://github.com/t-murash/HOOMD-Angle-Cosine/blob/master/doc/Angle-Cosine.pdf)



## Citing the HOOMD-Angle-Cosine package

Users of this package are encouraged to cite the following article in scientific publications:

* J. A. Anderson, J. Glaser, S. C. Glotzer, "HOOMD-blue: A Python package for high-performance molecular dynamics and hard particle Monte Carlo simulations", *Computational Materials Science*, (2020) **173** 109363, https://doi.org/10.1016/j.commatsci.2019.109363.

* K. Hagita, T. Murashima, "Molecular Dynamics Simulations of Ring Shapes on a Ring Fraction in Ring-Linear Polymer Blends", *Macromolecules*, (2021) **54** (17) 8043-8051, https://doi.org/10.1021/acs.macromol.1c00656.



