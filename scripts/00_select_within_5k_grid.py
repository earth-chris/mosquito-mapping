import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# set the base files to use
base = '/home/salo/src/mosquito-mapping/maxent-inputs/'
indir = base + 'pre-split/'
outdir = base

# get the list of files to resample
inf_ae = indir + 'aedes-aegypti-intersection.shp'
inf_aa = indir + 'aedes-albopictus-intersection.shp'
infs = [inf_ae, inf_aa]

# set the output files
outf_ae = outdir + 'aedes-aegypti-resampled.csv'
outf_aa = outdir + 'aedes-albopictus-resampled.csv'
outfs = [outf_ae, outf_aa]

# set the seed
np.random.seed(1985)

# function to get the x and y values
def getXY(pt):
    return (pt.x, pt.y)

# steps:
#  loop through each file
#  find the unique grid IDs
#  if only one point in that ID, keep it.
#  if more than one point, randomly pick one to keep
#  save all kept points as a new csv

for inf, outf in zip(infs, outfs):

    # read the dataframe
    df = gpd.read_file(inf)
    
    # create the output data frame
    odf = pd.DataFrame(columns=['species', 'geometry'])
    
    # get the unique ids
    ids = df['id'].unique().tolist()
    
    for id in ids:
        # subset the dataframe to just this id
        dfid = df[df['id'] == id]
        
        # if its just one point, push it to the output data frame
        n_pts = len(dfid)
        if n_pts == 1:
            odf = odf.append(dfid, ignore_index=True)
        
        # otherwise, randomly sample which point to use    
        else:
            random_index = np.random.randint(0, n_pts, size=None)
            odf = odf.append(dfid.iloc[random_index], ignore_index=True)
            
    # reset the index of the output data frame
    odf.reset_index(inplace=True)
    
    # convert the data to geopandas to maxent format
    gdf = gpd.GeoDataFrame(odf['species'], geometry=odf['geometry'], crs={'init': 'epsg:54009'})
    centroidseries = gdf['geometry'].centroid
    x, y = [list(t) for t in zip(*map(getXY, centroidseries))]
    
    # save the geodataframe to a shapefile
    gdf.to_file(outf[:-4] + '.shp')
    
    # create X and Y columns from the original dataframe
    gdf['X'] = x
    gdf['Y'] = y
    
    # remove the geometry column
    cols = ['species', 'X', 'Y']
    gdf = gdf[cols]
    
    # and save as an output csv
    gdf.to_csv(outf, index=False)