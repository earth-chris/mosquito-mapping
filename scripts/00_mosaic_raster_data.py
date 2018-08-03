import os
import ccb
import glob

# set the base files to use
base = '/home/cba/src/mosquito-mapping/'
rstr = base + 'raster/'
raws = rstr + 'raw/'
outd = rstr + 'scratch/'

# set the files and names for each raster
s_ccblc = raws + 'CCB-LC-*-unmixed-*.tif'
s_temps = raws + 'CCB-LC-*-temp-*.tif'
s_popdn = raws + 'LACR-pop-*.tif'
s_trees = raws + 'LACR-trees-*.tif'

o_ccblc = outd + 'ccblc-raw-mosaic.tif'
o_temps = outd + 'temps-raw-mosaic.tif'
o_popdn = outd + 'popdn-raw-mosaic.tif'
o_trees = outd + 'trees-raw-mosaic.tif'

# the file with the extent to use
#extentf = raws + 'LACR-pop-density-2015-100m.tif'
#ext = ccb.read.raster(extentf)

# jk, use this set bounding box (pulled from other rasters)
xmin = -117.787
ymin = -56.279
xmax = -32.599
ymax = 32.995
xps = 0.000898
yps = xps

# set up basic gdalwarp parameters for each file
te = '{xmin:0.3f} {ymin:0.3f} {xmax:0.3f} {ymax:0.3f}'.format(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)
tr = '{xps} {yps}'.format(xps=xps, yps=yps)
co = 'COMPRESS=LZW'
r = 'near'

# for each set of files, build the string to gdalwarp/mosaic each set of files
i_ccblc = glob.glob(s_ccblc)
inf = ' '.join(i_ccblc)
cmd = 'gdalwarp -r {r} -co {co} -te {te} -tr {tr} {inf} {outf} -ot Byte -multi -overwrite'.format(r=r, co=co, te=te, tr=tr, inf=inf, outf=o_ccblc)
ccb.prnt.status('building ccblc mosaic')
ccb.prnt.status(cmd)
#ccb.run(cmd)

# now temps
i_temps = glob.glob(s_temps)
inf = ' '.join(i_temps)
cmd = 'gdalwarp -r {r} -co {co} -te {te} -tr {tr} {inf} {outf} -ot Byte -multi -overwrite'.format(r=r, co=co, te=te, tr=tr, inf=inf, outf=o_temps)
ccb.prnt.status('building temps mosaic')
ccb.prnt.status(cmd)
ccb.run(cmd)

# now population density
i_popdn = glob.glob(s_popdn)
inf = ' '.join(i_popdn)
cmd = 'gdalwarp -r {r} -co {co} -te {te} -tr {tr} {inf} {outf} -multi -overwrite'.format(r=r, co=co, te=te, tr=tr, inf=inf, outf=o_popdn)
ccb.prnt.status('building popdn mosaic')
ccb.prnt.status(cmd)
ccb.run(cmd)

# and finally tree cover
i_trees = glob.glob(s_trees)
inf = ' '.join(i_trees)
cmd = 'gdalwarp -r {r} -co {co} -te {te} -tr {tr} {inf} {outf} -ot Byte -multi -overwrite'.format(r=r, co=co, te=te, tr=tr, inf=inf, outf=o_trees)
ccb.prnt.status('building trees mosaic')
ccb.prnt.status(cmd)
ccb.run(cmd)

# hooray!
ccb.prnt.status('done with raster mosaics!')