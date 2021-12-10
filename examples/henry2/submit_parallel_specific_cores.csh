#!/bin/csh
#BSUB -n 11,15                       # Number of MPI tasks: min,max
#BSUB -R "span[ptile=1] select[oc]"  # MPI tasks per node; Request 8 core nodes - that is 2x8=16 cores
#BSUB -x                             # Exclusive use of nodes
#BSUB -J parallel_specific_cores     # Name of job
#BSUB -W 5:00                        # Wall clock time
#BSUB -oo parallel_tasks_out         # Standard out
#BSUB -eo parallel_tasks_err         # Standard error

# Script name: submit_parallel_specific_cores.csh
# This script is useful if each task is parallel and you want to select nodes with a specific number of cores for each task
# HPC resources by processer type: https://projects.ncsu.edu/hpc/Documents/LSFResources.php#numcores

module load PrgEnv-intel

mpiexec python -m mpi4py -m pynodelauncher parallel_tasks.txt
