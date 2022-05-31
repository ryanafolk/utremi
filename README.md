# Heuchera ancestral niche analyses
Scripts written in python3 should be run in bash per below. The ancestral reconstruction should be run, with results in the paths specified below. E.g., tables output should be at `./ancestral_reconstruction_tables`.

## Ancestral niche analyses
### Install BiotaphyPy
```
#git clone https://github.com/biotaphy/BiotaPhyPy
#cd BiotaPhyPy/
#python setup.py install
#cd ..
```

### Run ancestral niche reconstruction in a loop, one iteration per variable
```
for f in ./pnos/*.dropped; do
g=$( echo ${f} | sed 's/.*\///g' | sed 's/\..*//g' )
echo ${g}
mkdir plots_${g}
./BiotaPhyPy/biotaphy/tools/ancestral_distribution.py astral_mcmctree_rep3.tre newick ${f} csv out_${g}.tre nexus -c out_table_${g}.txt -p plots_${g}
done
```

## Downstream analyses
1. `date_histograms_from_mcmctree.r` generates dating histograms from MCMCtree output. Run with the MCMC as mcmc.txt in the working directory. 

2. `projections_binned_ancestralreconstruction.py` performs the range projections on a per-node basis.  
    Example: 
    ```
    ./projections_binned_ancestralreconstruction.py ./ancestral_reconstruction_tables/out_table_BIOCLIM_1.txt ./BIOCLIM_1 -l ./PALEOCLIMATE_LAYERS/bio1_final/*.tif
    ````

3. `weight_projection_by_date_probability.py` takes the output of the projection and date histogram scripts to weight projections by posterior probability. Projections should be in a folder called "projected". Filepaths should reflect output of #2 above.
   
    Example: 
    ```
    ./weight_projection_by_date_probability.py dating_histograms.csv 
    ```
   
4. `trim_sum_and_normalize_projections.py` trims the projections to the study area, normalizes histogram area, and combines across species.
    
    Example:
    ```
    mkdir combined_normalized
    for i in `ls projected_weighted/*.tif | sed 's/.*_//g' | sed 's/\.tif//g' | sort | uniq`; do
     ./trim_sum_and_normalize_projections.py ./combined_normalized/${i}.combined.tif -178.2 6.6 -49.0 83.3 --rasters `ls projected_weighted/*_${i}.*tif`
    done
    ```

5. `annotate_maximum_density.py` annotates trees by the single value with maximum probability density. This is used for color plotting. In the case of ties one is arbitrarily taken. 

    Example: 
    ```
    for f in out_*.tre; do
    g=`echo ${f} | sed 's/\.tre//g'`
    ./annotate_maximum_density.py ${f} ${g}.maxdensity.tre
    done
    ```

All scripts contain usage examples in header comments. 

## Setup  
```     
Directory/   
├── projection   
|	├── {taxon}.Bio1_{date}.tifout_table_BIOCLIM_1.tif   
|	└──...   
├── ancestral_reconstruction_tables   
|	├── out_table_BIOCLIM_1.txt   
|	└── ...   
├── projected_weighted (from weight_projection_by_date_probability.py)   
|	├── {taxon}.bio1_{date}.tif   
|	└── ...   
├── BIOCLIM_1   
|	├──   
|	└── ...   
├── PALEOCLIMATE_LAYERS/bio1_final  
|	└── \*\.tif (layers generated with paleogenerate)   
├──  combined_normalized (from trim_sum_and_normalize_projections.py)   
|	└── ${i}.combined.tif    
├── mcmc.txt   
├── dating_histograms.csv (from date_histograms_from_mcmctree.r)   
├── annotate_maximum_density.py   
├── trim_sum_and_normalize_projections.py   
├── projections_binned_ancestralreconstruction.py   
├── weight_projection_by_date_probability.py   
└── date_histograms_from_mcmctree.r   
```

## Subfolders
`ancestral_reconstruction` folders contain trees with the ancestral reconstruction result (in BEAST-style format) and plots of both extant and ancestral reconstruction histograms. There is a folder for each of the ASTRAL and concatenation topologies. Plots of histograms are blue for the ML result, and red and green representing +- standard error.

`ancestral_projection` folders contain an animated GIF showing trends in habitat suitability from the Pleistocene to present based on mean annual temperature. There is a folder for each of the ASTRAL and concatenation topologies.
