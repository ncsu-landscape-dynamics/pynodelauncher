#!/bin/tcsh
#BSUB -n 5  # number of MPI processes
#BSUB -W 00:05  # maximum time
#BSUB -oo tasks_out
#BSUB -eo tasks_err
#BSUB -J tasks  # job name

module load PrgEnv-intel
conda activate /path/to/env

mpiexec python -m mpi4py pynodelauncher tasks.txt
