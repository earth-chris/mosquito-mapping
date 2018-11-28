import os
import ccb
import glob
from shapely.geometry import Point
import geopandas as gpd

# set the base files to use
base = '/home/salo/src/mosquito-mapping/maxent-inputs/'
indir = base + 'epsg4326/'
outdir = base

# get the list of files to convert
infs = glob.glob(indir + '*.csv')

# set the projections
iprj = {'init': 'epsg:4326'}
oprj = {'init': 'epsg:54009'}
oprj = 54009

# function to get the x and y values
def getXY(pt):
    return (pt.x, pt.y)

# now loop through each file, read the csv, reproject, and save as a new csv
for inf in infs:

    # read the dataframe
    df = pd.read_csv(inf)
    
    # convert the xy columns into a geopandas dataframe
    geometry = [Point(xy) for xy in zip(df.X, df.Y)]
    gdf = gpd.GeoDataFrame(df['species'], geometry=geometry, crs=iprj)
    
    # save this as an output file
    basename = os.path.basename(inf)[:-4]
    out_4326 = outdir + basename + '-4326.shp'
    out_oprj = outdir + basename + '-{}.shp'.format(oprj)
    gdf.to_file(out_4326)
    
    # conver it to the new projection
    cmd = 'ogr2ogr -t_srs EPSG:{prj} {outf} {inf}'.format(
        prj=oprj, outf=out_oprj, inf=out_4326)
    print(cmd)
    ccb.run(cmd)
    
    # read this new file into geopandas
    gdf = gpd.read_file(out_oprj)
    
    # get the x and y coordinates as separate lists
    centroidseries = gdf['geometry'].centroid
    x, y = [list(t) for t in zip(*map(getXY, centroidseries))]
    
    # then replace the X and Y columns from the original dataframe
    df.X = x
    df.Y = y
    
    # and save this final csv
    out_csv = outdir + basename + '.csv'
    df.to_csv(out_csv, index=False)
    
    # ta da.
    
# then, remove the temp files
tf1 = glob.glob(base + '*4326.*')
tf2 = glob.glob(base + '*{}.*'.format(oprj))
for f in (tf1 + tf2):
    os.remove(f)