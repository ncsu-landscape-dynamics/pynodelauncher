# Sample script

args <- commandArgs(trailingOnly=TRUE)

doGParetoFold <- function(foldN=1){
  print(paste0("Finished running Fold ", foldN, ". Yay!"))
}

doGParetoFold(foldN=args[1])
