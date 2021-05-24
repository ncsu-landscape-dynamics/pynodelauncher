# pynodelauncher

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4779076.svg)](https://doi.org/10.5281/zenodo.4779076)
[![FAIR Software](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8B%20%20%E2%97%8B-orange)](https://fair-software.eu)

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

To execute, use `python3` instead of just `python` unless you also set
the default Python to be Python 3.
Otherwise, the general usage (below) applies.

### Installation on NC State's Henry2

```sh
module load conda
conda activate /path/to/env
module load PrgEnv-intel
pip install git+https://github.com/ncsu-landscape-dynamics/pynodelauncher.git
conda deactivate
```

Replace `/path/to/env` by the path to conda environment you are using or
the whole `module load conda` and `conda activate ...` by a module load
which sets up a conda environment.

Note that the mpi4py and pynodelauncher installations will go to your home directory.
Here, this is desired because 1) you are not using the mpi4py through conda
and 2) you can use any conda environment for your actual work.
However, you need to have enough space for the installation in your home directory.
That should not be an issue unless you are using the home directory for things
which need to be outside of it such as data or conda environments or cache.

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
mpiexec -n 4 python -m mpi4py -m pynodelauncher tasks.txt
```

Notice the `python -m mpi4py -m` part which is needed for avoiding
deadlocks (and thus stalled processes) in certain cases.
See the [mpi4py.run documentation](https://mpi4py.readthedocs.io/en/stable/mpi4py.run.html) for details.

### Usage on NC State's Henry2

The submission script needs to include the LSF parameters
(esp. `-n 5` for number of MPI processes), the MPI library setup,
the conda setup, and mpiexec call. For example:

```sh
#!/bin/tcsh
#BSUB -n 5  # number of MPI processes
#BSUB -W 00:10  # maximum time
#BSUB -oo tasks_out
#BSUB -eo tasks_err
#BSUB -J tasks  # job name

module load PrgEnv-intel
module load conda
conda activate /path/to/env

mpiexec python -m mpi4py -m pynodelauncher tasks.txt
```

The `module load...conda activate...` part should be modified as needed
in the same way as for the installation (see above).

Assuming the file above is called `submit_job.csh`, call _bsub_:

```sh
bsub < submit_job.csh
```

### More Examples

See [the examples directory](examples).

## Troubleshooting

This section discusses common issues with installation and usage.

### Script not on PATH

After a successful installation, you may get the following warning about the directory
in which the (executable) script is not being in the system environment PATH variable:

```text
WARNING: The script pynodelauncher is installed in '.../.local/bin' which is not on PATH.
```

This means that you want be able to execute _pynodelauncher_ directly as a command
(without specifying path including filename extension). However, the MPI execution
is done using module execution (with `-m`) not through an executable on PATH.
If you want to do thing like calling _pynodelauncher_ as a command to get usage
and help, then follow the further instructions in this section.

The PATH variable is an environmental variable which the operating system uses to find
executable files (scripts or binaries). It contains paths (directories) where the
executable files are separated by a platform-depended separator (usually `:` or `;`).

Hence, the message either means you should install the package in some other way on
your system, or, more likely, that you should add the path `.../.local/bin` to your
PATH variable. Replace the `...` part (or whole `.../.local/bin`) by what appears in
the warning message (`...` will be likely your home directory).

Here is how the modification of the PATH variable is done in Bash (either in command line
or in `.bashrc` file):

```sh
export PATH="$HOME/.local/bin:$PATH"
```

### Running without Installation

The `python -m mpi4py` piece assumes you installed _pynodelauncher_ with pip
and accesses _pynodelauncher_ as a module (with `-m`).
If you just have the `pynodelauncher.py` script somewhere, you need to pass it
as a file to mpi4py, so:

```sh
... python -m mpi4py /path/to/pynodelauncher.py
```

Executing with `python -m mpi4py` never uses executable files (commands) on PATH,
but you can can use combination of _which_ command and command substitution
to achieve similar behavior if you want to test your shell skills.

### ImportError with Shared Object File

If you get a Python traceback with ImportError saying it can't find
a shared object file like the one below and you are on HPC, you likely
forgot to load the appropriate MPI module or loaded a wrong one.

```text
Traceback (most recent call last):
  File ".../.local/bin/pynodelauncher", line 5, in <module>
    from pynodelauncher import main
  File ".../.local/lib/python3.7/site-packages/pynodelauncher.py", line 4, in <module>
    from mpi4py import MPI
ImportError: libimf.so: cannot open shared object file: No such file or directory
```

If you get traceback like this on your local machine, you need to investigate
how to install and test mpi4py properly on your system.

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
