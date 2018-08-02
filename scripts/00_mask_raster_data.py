import os
import ccb
import glob

# set the base files to use
base = '/home/salo/src/mosquito-mapping/raster/'
raws = base + 'scratch/'
outd = base + 'scratch/'

# the file with the extent to use
maskf = raws + 'temps-raw-mosaic.tif'
masko = outd + 'maskfile.tif'

# set the input and output files
i_ccblc = outd + 'ccblc-raw-mosaic.tif'
i_temps = outd + 'temps-raw-msoaic.tif'
i_popdn = outd + 'popdn-raw-mosaic.tif'
i_trees = outd + 'trees-raw-mosaic.tif'

o_ccblc = outd + 'ccblc-raw-mosaic-masked.tif'
o_temps = outd + 'temps-raw-msoaic-masked.tif'
o_popdn = outd + 'popdn-raw-mosaic-masked.tif'
o_trees = outd + 'trees-raw-mosaic-masked.tif'

# set the nodata value in the raster to enable mask building
nodata = 0
cmd = 'gdal_edit.py -a_nodata {nodata:d} {file}'.format(nodata=nodata, file=maskf)
ccb.prnt.status('setting mask nodata value')
ccb.prnt.status(cmd)
ccb.run(cmd)

# then build the maskfile
cmd = 'otbcli_ManageNoData -in {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -mode buildmask'.format(
    inf=maskf, outf=masko)
ccb.prnt.status('building nodata mask')
ccb.prnt.status(cmd)
ccb.run(cmd)

# set nodata values for the rasters to use
nodata = 255
ccb.prnt.status('assigning nodata to input rasters')
cmd = 'gdal_edit.py -a_nodata {nodata:d} {file}'.format(nodata=nodata, file=i_ccblc)
ccb.run(cmd)
cmd = 'gdal_edit.py -a_nodata {nodata:d} {file}'.format(nodata=nodata, file=i_temps)
ccb.run(cmd)
cmd = 'gdal_edit.py -a_nodata {nodata:d} {file}'.format(nodata=nodata, file=i_popdn)
ccb.run(cmd)
cmd = 'gdal_edit.py -a_nodata {nodata:d} {file}'.format(nodata=nodata, file=i_trees)
ccb.run(cmd)

# then run through each file and apply the mask
ccb.prnt.status('masking raster data')
cmd = 'otbcli_ManageNoData -in {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -mode apply -mode.apply.mask {maskf}'.format(
    inf=i_ccblc, out=o_ccblc, maskf=masko)
ccb.prnt.status(cmd)
ccb.run(cmd)

cmd = 'otbcli_ManageNoData -in {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -mode apply -mode.apply.mask {maskf}'.format(
    inf=i_temps, out=o_temps, maskf=masko)
ccb.prnt.status(cmd)
ccb.run(cmd)

cmd = 'otbcli_ManageNoData -in {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -mode apply -mode.apply.mask {maskf}'.format(
    inf=i_popdn, out=o_popdn, maskf=masko)
ccb.prnt.status(cmd)
ccb.run(cmd)

cmd = 'otbcli_ManageNoData -in {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -mode apply -mode.apply.mask {maskf}'.format(
    inf=i_trees, out=o_trees, maskf=masko)
ccb.prnt.status(cmd)
ccb.run(cmd)

# celebrate
ccb.prnt.status('done masking raster data!')