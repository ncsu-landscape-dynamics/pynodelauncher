#!/bin/tcsh
#BSUB -n 5,20                                     # Number of MPI tasks to simultaneously assign (min, max)
#BSUB -W 1440                                      # request 24 hours for running (max for general HPC = 4 days [5760])
#BSUB -R "span[ptile=1] rusage[mem=22000]"          # MPI tasks per node, with minimum memory specified
#BSUB -x                                            # exclusive use of nodes that each MPI task is assigned to
#BSUB -J gpareto_kfolds100                          # specify job NAME
#BSUB -o stdout_%J                                  # output file (%J will be replaced by job name [number]) #-oo means overwrite
#BSUB -e stderr_%J                                  # error file (%J will be replaced by job name [number]) # -eo means overwrite

##BSUB - R select[oc]                                # Specify number of cores to use. oc=octa, and there are 2 nodes, so 2*8=16 cores
                                                    ## if this is commented out, then the MPI tasks are assigned to any node meeting the 
                                                    ## rusage memory specification above

## Objective: I have a function that takes a random 90% of my data and runs a function over it (parallelizing in the process). 
### I want to do a kfold validation using 100 folds.

## How this script works: Here, my .txt file is a list of 100 calls to my script that runs the function. MPI is used to assign the
### each task to its own node, and then the memory specifies the minimum for each node. By not defining the number of cores, I am asking
### pynodelauncher to put my job wherever (whatever number of cores) so long as at minimum 5 tasks are running simultaneously and the memory 
### specification is met.

module load PrgEnv-intel
conda activate /path/To/Folder
mpiexec python -m mpi4py -m pynodelauncher ./kfold.txt
conda deactivate
