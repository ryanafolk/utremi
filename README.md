# Heuchera ancestral niche analyses

## Scripts in main directory
`projections_binned_ancestralreconstruction.py` performs the range predictions on a per-node basis. 

`date_histograms_from_mcmctree.r` generates dating histograms from MCMCtree output. 

`weight_projection_by_date_probability.py` takes the output of the projection and date histogram scripts to weight projections by posterior probability.

`trim_sum_and_normalize_projections.py` trims the projections to the study area, normalizes histogram area, and combines across species.

`annotate_maximum_density.py` annotates trees by the single value with maximum probability density. In the case of ties one is arbitrarily taken.

All scripts contain usage examples in header comments. 

## Subfolders
`ancestral_reconstruction` folders contain trees with the ancestral reconstruction result (in BEAST-style format) and plots of both extant and ancestral reconstruction histograms. There is a folder for each of the ASTRAL and concatenation topologies. Plots of histograms are blue for the ML result, and red and green representing +- standard error.

`ancestral_projection` folders contain an animated GIF showing trends in habitat suitability from the Pleistocene to present based on mean annual temperature. There is a folder for each of the ASTRAL and concatenation topologies.
