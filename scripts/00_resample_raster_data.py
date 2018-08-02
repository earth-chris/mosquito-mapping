import os
import ccb
import glob

# set the base files to use
base = '/home/salo/src/mosquito-mapping/raster/'
raws = base + 'scratch/'
outd = base

# set the input files
i_ccblc = raws + 'ccblc-raw-mosaic-masked.tif'
i_temps = raws + 'temps-raw-msoaic-masked.tif'
i_popdn = raws + 'popdn-raw-mosaic-masked.tif'
i_trees = raws + 'trees-raw-mosaic-masked.tif'
i_files = [i_ccblc, i_temps, i_popdn, i_trees]

# set the target resolutions
res = [500, 1000, 5000, 10000, 50000, 100000]

# make directories for each res
for r in res:
    rpath = '{dir}{r:6d}-m/'
    if not os.path.exists(rpath):
        os.makedirs(rpath)

# loop through each of the target files and resample them
ccb.prnt.status('resampling raster data')
for file in i_files:
    obase = os.path.splitext(file)[0]
    for r in res:
        opath = '{dir}{r:6d}-m/{obase}.tif'
        cmd = 'gdalwarp -tr {res} {res} -co COMPRESS=LZW {inf} {outf]'.format(res=r, inf=file, outf=opath)
        ccb.prnt.status(cmd)
        ccb.run(cmd)
        
# convene a shindig
ccb.prnt.status('done resampling raster data!')