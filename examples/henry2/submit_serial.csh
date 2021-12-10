#!/bin/tcsh
#BSUB -n 5  # number of MPI processes
#BSUB -W 00:05  # maximum time
#BSUB -oo tasks_out
#BSUB -eo tasks_err
#BSUB -J tasks  # job name

module load PrgEnv-intel
# Modify the following line to use your conda environment.
conda activate /the/environment/you/are/using

mpiexec python -m mpi4py -m pynodelauncher tasks.txt
