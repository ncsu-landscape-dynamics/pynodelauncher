#!/bin/csh
#BSUB -n 11,17                                  # Number of MPI tasks: min,max
#BSUB -R "span[ptile=1] rusage[mem=30000]"      # MPI tasks per node; memory
#BSUB -x                                        # Exclusive use of nodes
#BSUB -J parallel_dynamic_cores                 # Name of job
#BSUB -W 12:00                                  # Wall clock time
#BSUB -oo dy_parallel_tasks_out                 # Standard out
#BSUB -eo dy_parallel_tasks_err                 # Standard error

# Script name: submit_parallel_dynamic_cores.csh
# This script is useful if each task is parallel and if you don’t care how many cores you get for each task (reduces wait time)
# This script leads to dynamic core selection

module load PrgEnv-intel

mpiexec python -m mpi4py -m pynodelauncher parallel_tasks.txt
