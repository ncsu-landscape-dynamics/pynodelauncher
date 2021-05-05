# pynodelauncher

The *pynodelauncher* tool launches pleasantly parallel tasks on multiple nodes
on a HPC cluster.

It is using MPI through the *mpi4py* package which in turn is using system MPI library.
A task can be any command, typically a call of a script with a series of parameters.

## Installation

### General Installation

Use *pip* to install *pynodelauncher*:

```sh
python -m pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
```

This will also install the *mpi4py* package (again using pip) if it is not already
installed (using pip or in any other way).

### Installation on NC State's Henry2

```sh
conda activate /path/to/env
module load PrgEnv-intel
pip install mpi4pygit+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
conda deactivate
```

Replace `/path/to/env` by the path to conda environment you are using or
the whole `conda activate ...` by a module load sets up a conda environment. 

Note that the mpi4py and pynodelauncher installations will go to your home directory.
Here, this is desired because 1) you are not using the mpi4py through conda
and 2) you can use any conda environment for your actual work.

See also the official documentation for installing [mpi4py](https://projects.ncsu.edu/hpc/Software/Apps.php?app=Conda-MPI#mpi4py).

## Usage

### General Usage

Prepare file `tasks.txt`:

```text
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
```

Run from command line:

```sh
mpiexec -n 4 python -m mpi4py pynodelauncher tasks.txt
```

### Usage on NC State's Henry2

```sh
#!/bin/tcsh
#BSUB -n 5  # number of MPI processes
#BSUB -W 00:10  # maximum time
#BSUB -oo tasks_out
#BSUB -eo tasks_err
#BSUB -J tasks  # job name

module load PrgEnv-intel
conda activate /path/to/env

mpiexec python -m mpi4py pynodelauncher tasks.txt
```

The `conda activate ...` part should be modified as needed
in the same way as for the installation (see above).

## Authors

* Vaclav Petras, [NC State University, Center for Geospatial Analytics](https://geospatial.ncsu.edu/)
* Lisa L. Lowe, NC State University, Office of Information Technology, Advanced Computing

## Copyright, License, and Disclaimer

Copyright (C) 2021 The Authors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
