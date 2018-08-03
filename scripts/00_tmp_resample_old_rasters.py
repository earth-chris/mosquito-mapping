import ccb
import numpy as np


# set paths
base = '/home/cba/src/mosquito-mapping/raster/'

# set the base image to resample
inf = base + '001000-m/stacked-layers-masked.tif'

# set the base names of the layers
layers = ['soil', 'vegetation', 'impervious', 'temp-min', 'temp-med', 'temp-max', 'trees', 'population']

# set the resolutions to resample to
res = np.array([5000, 10000, 50000, 100000])
res_scalar = 1. / 111000
res_scaled = res * res_scalar

# set the resampling scheme
resample = 'average'

# first, do a band-by-band extraction of the original res data
for j in range(len(layers)):
    lpath = '{dir}{r:06d}-m/{layer}.asc'.format(dir=base, r=1000, layer=layers[j])
    cmd = 'gdal_translate -of AAIGrid -b {band} {inf} {outf}'.format(
        band=j+1, inf=inf, outf=lpath)
    ccb.prnt.status(cmd)
    #ccb.run(cmd)

# loop through each of the target files and resample them
ccb.prnt.status('resampling raster data')
for i in range(len(res)):
    #obase = os.path.splitext(inf)[0]
    obase = 'stacked-layers'
    opath = '{dir}{r:06d}-m/{obase}.tif'.format(dir=base, r=res[i], obase=obase)
    cmd = 'gdalwarp -multi -tr {res} {res} -r {resample} -co COMPRESS=LZW {inf} {outf}'.format(
        res=res_scaled[i], resample=resample, inf=inf, outf=opath)
    ccb.prnt.status(cmd)
    #ccb.run(cmd)
    
    # then run the band-by-band extraction
    for j in range(len(layers)):
        lpath = '{dir}{r:06d}-m/{layer}.asc'.format(dir=base, r=res[i], layer=layers[j])
        cmd = 'gdal_translate -of AAIGrid -b {band} {inf} {outf}'.format(
            band=j+1, inf=opath, outf=lpath)
        ccb.prnt.status(cmd)
        if j == 2:
            ccb.run(cmd)
        
# convene a shindig
ccb.prnt.status('done resampling raster data!')