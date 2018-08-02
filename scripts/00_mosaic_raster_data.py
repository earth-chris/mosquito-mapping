import os
import ccb
import glob

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
rstr = base + 'raster/'
raws = rstr + 'raw/'
outd = rstr + 'scratch/'

# the file with the extent to use
extentf = raws + 'LACR-pop-density-2015-100m.tif'
ext = ccb.read.raster(extentf)

# set the files and names for each raster
s_ccblc = raws + 'CCB-LC-*-unmixed-*.tif'
s_temps = raws + 'CCB-LC-*-temp-*.tif'
s_popdn = raws + 'LACR-pop-*.tif'
s_trees = raws + 'LACR-trees-*.tif'

o_ccblc = outd + 'ccblc-raw-mosaic.tif'
o_temps = outd + 'temps-raw-msoaic.tif'
o_popdn = outd + 'popdn-raw-mosaic.tif'
o_trees = outd + 'trees-raw-mosaic.tif'

# set up basic gdalwarp parameters for each file
te = '{xmin:0.3f} {ymin:0.3f} {xmax:0.3f} {ymax:0.3f}'.format(xmin=ext.xmin, ymin=ext.ymin, xmax=ext.xmax, ymax=ext.ymax)
tr = '{xps} {yps}'.format(xps=ext.xps, yps=ext.yps)
co = 'COMPRESS=LZW'

# for each set of files, build the string to gdalwarp/mosaic each set of files
i_ccblc = glob.glob(s_ccblc)
inf = ' '.join(i_ccblc)
cmd = 'gdalwarp -co {co} -te {te} -tr {tr} {inf} {outf} -overwrite'.format(co=co, te=te, tr=tr, inf=inf, outf=o_ccblc)
ccb.prnt.status('building ccblc mosaic')
ccb.prnt.status(cmd)
ccb.run(cmd)

# now temps
i_temps = glob.glob(s_temps)
inf = ' '.join(i_temps)
cmd = 'gdalwarp -co {co} -te {te} -tr {tr} {inf} {outf} -overwrite'.format(co=co, te=te, tr=tr, inf=inf, outf=o_temps)
ccb.prnt.status('building temps mosaic')
ccb.prnt.status(cmd)
#ccb.run(cmd)

# now population density
i_popdn = glob.glob(s_popdn)
inf = ' '.join(i_popdn)
cmd = 'gdalwarp -co {co} -te {te} -tr {tr} {inf} {outf} -overwrite'.format(co=co, te=te, tr=tr, inf=inf, outf=o_popdn)
ccb.prnt.status('building popdn mosaic')
ccb.prnt.status(cmd)
#ccb.run(cmd)

# and finally tree cover
i_trees = glob.glob(s_trees)
inf = ' '.join(i_trees)
cmd = 'gdalwarp -co {co} -te {te} -tr {tr} {inf} {outf} -overwrite'.format(co=co, te=te, tr=tr, inf=inf, outf=o_trees)
ccb.prnt.status('building ccblc mosaic')
ccb.prnt.status(cmd)
#ccb.run(cmd)

# hooray!
ccb.prnt.status('done with raster mosaics!')