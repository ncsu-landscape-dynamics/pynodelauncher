# pynodelauncher

The _pynodelauncher_ tool launches pleasantly parallel tasks on multiple nodes
on a HPC cluster.

It is using MPI through the _mpi4py_ package which in turn is using system MPI library.
A task can be any command, typically a call of a script with a series of parameters.

A series of independent, serial tasks can be executed one after each other, but they
don't have to. _pynodelauncher_ starts each individual task on a separate core,
possibly spread over multiple nodes, using MPI depending on job submission on HPC.
Each individual task can be additionally parallelized within itself when the
MPI command or job submission accounts for that.

## Installation

The _pynodelauncher_ tool can be installed using _pip_ from the Git repository.
Alternatively, the `pynodelauncher.py` script can be used directly if needed.

### General Installation

Use _pip_ to install _pynodelauncher_:

```sh
python -m pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
```

This will also install the _mpi4py_ package (again using pip) if it is not already
installed (using pip or in any other way).

### Installation on Ubuntu

Here we assume basic Ubuntu 20.04 with almost no software installed.

```sh
sudo apt update
sudo apt install python3 python3-pip git libopenmpi-dev
python3 -m pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
```

To execute, use `python3` instead of just `python`.
Otherwise, the general usage (below) applies.

### Installation on NC State's Henry2

```sh
conda activate /path/to/env
module load PrgEnv-intel
pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
conda deactivate
```

Replace `/path/to/env` by the path to conda environment you are using or
the whole `conda activate ...` by a module load sets up a conda environment.

Note that the mpi4py and pynodelauncher installations will go to your home directory.
Here, this is desired because 1) you are not using the mpi4py through conda
and 2) you can use any conda environment for your actual work.

See also the official documentation for installing [mpi4py](https://projects.ncsu.edu/hpc/Software/Apps.php?app=Conda-MPI#mpi4py).

If you are using R with `module load R` (and not with conda), you need to load
the R module before loading PrgEnv-intel, because R has a conflict warning for
PrgEnv-intel but not the other way around.

## Usage

Typical usage consists of two steps:

1. Preparing a text file with list of tasks (commands) to execute.
2. Executing the script using MPI.

### General Usage

Prepare file `tasks.txt`:

```text
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
echo "Hello from $HOSTNAME"
```

Each row in the file is a task. A row can contain one or more commands
(separated by `;`). The syntax is syntax of your shell, e.g., Bash.

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

Then call *bsub*:

```sh
bsub < submit_job.csh
```

### More Examples

See [the examples directory](examples).

## Warnings and Limitations

If one of your tasks takes an hour and your other tasks take 5 minutes each,
many cores will be idle while waiting on the long-running task to finish.
You either need to ask for much less cores (e.g. 3)
or submit the long-running task as a separate job. Having many allocated cores idle is
not acceptable use on many HPC systems including NC State's Henry2.
So, you need to plan your allocation well and monitor the job
especially when task run time may vary.

There is no error checking of execution of individual commands as of yet.

This is experimental software, so check existing issues and please
give us feedback, e.g., by opening new issues.

The software does not check your data integrity or compliance with HPC usage policies,
so be mindful of that. In other words, use of this software is at your own risk.

## Authors

- Vaclav Petras, [NC State University, Center for Geospatial Analytics](https://geospatial.ncsu.edu/)
- Lisa L. Lowe, NC State University, Office of Information Technology, Advanced Computing

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
