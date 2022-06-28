# Heuchera ancestral niche analyses
The quoted code should be run in bash. Ensure that paths of output from each step are not being messed with. Some paths are hard-coded in scripts and should be changed as noted. PNO files should be in a directory called "pnos", and the path to mcmc output should be updated in `date_histograms_from_mcmctree.r`.

## Setup  
If you want to run this pipeline yourself, clone the repository such that your directory setup is as follows:

```     
Directory/   
├── data # Replace with your own data
|	├── astral_mcmctree_rep3.tre (tree file - dated)
|	├── mcmc.txt    
|	└──...   
├── pnos # Replace with your own data
|	├──
|	└── ...   
├── results # These are previously calculated results
|	└── 
├── scripts # From repository
|	├──  dating_histograms.csv (from date_histograms_from_mcmctree.r)   
|	├──   annotate_maximum_density.py   
|	├──   trim_sum_and_normalize_projections.py   
|	├──   projections_binned_ancestralreconstruction.py   
|	├──   weight_projection_by_date_probability.py   
└─ 	└──   date_histograms_from_mcmctree.r   
├── comparision
|	├──  phyloclim
|	     ├──  01_phyloclim_run.R
|	     ├── data
|	         ├── PNO
|               └─── ... 
└─           └── astral_mcmctree_rep3.tre
```

To duplicate paper results, run as follows without changes. The only thing missing in the path is paleoclimatic data (see that repository).

## Subfolders
### `data`
Tree and MCMCtree output.

### `pnos`
PNO files in the expected format.

### `scripts`
Python and R scripts.

### `results`
`ancestral_reconstruction` folders contain paper results comprising trees with the ancestral reconstruction (in BEAST-style format) and plots of both extant and ancestral reconstruction histograms. There is a folder for each of the ASTRAL and concatenation topologies. Plots of histograms are blue for the ML result, and red and green representing +- standard error.

`ancestral_projection` folders contain results comprising an animated GIF showing trends in habitat suitability from the Pleistocene to present based on mean annual temperature. There is a folder for each of the ASTRAL and concatenation topologies.

### `comparision`  
Comparsion with previous published methods including phyloclim and ambitus. 

## Dependencies
The python scripts have various dependencies that can be queried by attempting to run the scripts; full installation instructions are only given for BiotaphyPy below. Most important is a full working install of GDAL (both the Python library and the executables) that is in the path. A further incomplete list is:
```
pip3 install rasterio
pip3 install dendropy
```

## Set up directory structure
```
mkdir ancestral_reconstruction_astral

mkdir ancestral_projection_astral
```

## Ancestral niche analyses
### 1. Install BiotaphyPy
```
cd ancestral_reconstruction_astral
git clone https://github.com/biotaphy/BiotaPhyPy
cd BiotaPhyPy/
python setup.py install
cd ..
```
Ensure the cloned repository remains in the working directory for the next step.

### 2. Run ancestral niche reconstruction in a loop, one iteration per variable
```
for f in ./pnos/*.dropped; do
    g=$( echo ${f} | sed 's/.*\///g' | sed 's/\..*//g' )
    echo ${g}
    mkdir plots_${g}
    python3 BiotaPhyPy/biotaphy/tools/ancestral_distribution.py ./../data/astral_mcmctree_rep3.tre newick ${f} csv out_${g}.tre nexus -c out_table_${g}.txt -p plots_${g}
    done
```

### 3. Annotate trees by the single bin value with maximum probability density
This is used for color plotting. In the case of ties one is arbitrarily taken.
```
for f in out_*.tre; do
    g=`echo ${f} | sed 's/\.tre//g'`
    python3 ./../scripts/annotate_maximum_density.py ${f} ${g}.maxdensity.tre
    done
```


## Downstream analyses
### 1. Generate histograms representing dating uncertainty
Generates dating histograms from MCMCtree output. Note the path to the mcmc.txt file output by this package is hard-coded on line 2 and should be updated as appropriate.
```
cd ..
cd ancestral_projection_astral
R CMD BATCH ./../scripts/date_histograms_from_mcmctree.r 
# A file called dating_histograms.csv should appear in the working directory
```

### 2. Perform geographic range projections on paleoclimate data
```
python3 ./../scripts/projections_binned_ancestralreconstruction.py ./../ancestral_reconstruction_astral_testrun/out_table_BIOCLIM_1.txt ./BIOCLIM_1 -l ./../../Heuchera_complete_project/ancestral_projection_astral/ShellyFinal_NovemberLayers_2019/bio1_final/*.tif
mkdir projected
mv *tifout*.tif ./projected/
# There should now be lots of TIFs in a folder called projected
```

### 3. Weight projections by posterior probability of occurrence date
File paths should reflect output of #1 and #2 above and should not be messed with just yet.  
```
python3 ./../scripts/weight_projection_by_date_probability.py dating_histograms.csv 
# There should now be yet more TIFs in a folder called projected_weighted
```
   
### 4. Trim the projections to the study area, normalize histogram area, and combine across species.  
```
mkdir combined_normalized
for i in `ls projected_weighted/*.tif | sed 's/.*_//g' | sed 's/\.tif//g' | sort | uniq`; do
    python3 ./../scripts/trim_sum_and_normalize_projections.py ./combined_normalized/${i}.combined.tif -178.2 6.6 -49.0 83.3 --rasters `ls projected_weighted/*_${i}.*tif`
    done
```
We end up with one TIF per time period, representing joint probabilities of occurrence for all species.

All scripts contain usage examples in header comments. 
