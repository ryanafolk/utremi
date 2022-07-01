# Note on node labeling. Binned ancestral reconstruction code will be off by one because the root does not get a numeric label. Otherwise the node labels will match between R numbering, MCMCtree, and the binned reconstruction script as long as the tree file is the same.
table = read.table("./../data/mcmc.txt", sep = "\t", header = TRUE)

# Remove irrelevant tailing columns
x = ncol(table) - 3 
table_reduced = table[2:x]

# Dating analysis was scaled to my/100 so this reverses that.
table_reduced = data.frame(apply(table_reduced, 2, FUN <- function(x)(return (x * 100)))) 

## Reduce table to time period of interest (not needed)
#table_reduced = table_reduced[table_reduced <= 3.3]

# List of scenario dates.
break_list = c(0,0.07,0.13,0.2,0.26,0.33,0.4,0.46,0.53,0.59,0.66,0.73,0.79,0.86,0.92,0.99,1.06,1.12,1.19,1.25,1.32,1.39,1.45,1.52,1.58,1.65,1.72,1.78,1.85,1.91,1.98,2.05,2.11,2.18,2.24,2.31,2.38,2.44,2.51,2.57,2.64,2.71,2.77,2.84,2.9,2.97,3.04,3.1,3.17,3.23,3.3)

# MUST have more than one column in table_reduced or this won't work on the right axis
# Note the histogram is only calculated on the period of interest.
histograms = sapply(table_reduced, FUN = function(x) hist(x[x <= 3.3], breaks = break_list, plot = FALSE)$density)

# Remove columns with no data (these are taxa outside the period of interest).
histograms_cleaned <- histograms[,colSums(is.na(histograms))<nrow(histograms)]

histograms_normalized = apply(histograms_cleaned, 2, FUN <- function(x)(return (x/sum(x))))

# Generate bin labels
histogram_labels = sapply(table_reduced, FUN = function(x) hist(x[x <= 3.3], breaks = break_list, plot = FALSE)$breaks)

# Add bin label
histograms_normalized = data.frame(cbind(histogram_labels[1:50], histograms_normalized))

# Get rid of rows with only zeros (these are timeslices with only extant taxa).
histograms_normalized_cleaned = histograms_normalized[rowSums(histograms_normalized[, -1])>0, ]

write.csv(histograms_normalized_cleaned, "./dating_histograms.csv", row.names = FALSE)
