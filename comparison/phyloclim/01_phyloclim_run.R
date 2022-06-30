# PhyloClim comparision 
## Folk & Gaynor et al. 

# Load packages
library(phyloclim)

# Set up input files
## Tree
## Read tree file 
### Format needed = Phylo
target2 <- read.tree("data/astral_mcmctree_rep3.tre")
## Tree must be ultrametric
is.ultrametric(target2)
target2 <- phytools::force.ultrametric(target2)
is.ultrametric(target2) 
## Must have tip and node labels in consecutive order 
target2 <- phyloch::fixNodes(target2, quiet = TRUE)


## PNO df
### Its a list of dataframes with even bins
### Create list of files and read.csv
pnolist <- list.files(path = "data/PNO/", pattern = "*", full.names = TRUE, recursive = FALSE)
pnodf <- lapply(pnolist, read.csv, header=FALSE, row.names=NULL)
outkey <- gsub(pattern = "data/PNO//", replacement = "", pnolist)

### Format data frame 
#### Match tips and df
for(i in 1:12){
  pnodf[[i]]<- rbind(pnodf[[i]][1,], pnodf[[i]][match(target2$tip.label, pnodf[[i]]$V1),])
}

#### Fix row and column names
pnodft <- c()
for(i in 1:12){
  pnodft[[i]] <- pnodf[[i]][,2:51]
  rownames(pnodft[[i]]) <- pnodf[[i]][,1]
  colnames(pnodft[[i]]) <- 1:50
}

#### Transpose and convert to data frame
pnodft2 <- c()
for(i in 1:12){
  pnodft2[[i]] <- as.data.frame(t(pnodft[[i]]))
}

## Make sure the tips and PNOs list match! 
tips <- target2$tip.label
pnocol <- colnames(pnodft2[[1]])
tips %in% pnocol
pnocol %in% tips
setdiff(pnocol,tips)

# Finally run the function!
out <- c()
for(i in 1:12){
out[[i]] <- anc.clim(target2, 
         posterior = NULL, 
         pno = pnodft2[[i]],
         n = 100, # number of resamples
         method = "ML")
}


saveRDS(out, "outdf.RDS")
saveRDS(outkey, "outkey.RDS")
#readRDS("outdf.RDS")
#readRDS("outkey.RDS")