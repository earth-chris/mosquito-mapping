import os
import ccb


# set the paths to the input files
base = '/home/cba/src/mosquito-mapping/raster/'
popdn_inf = base + 'scratch/popdn-raw-mosaic-masked.tif'
popdn_tmp = base + 'scratch/popdn-raw-mosaic-masked-ln-tmp.tif'
popdn_out = base + 'scratch/popdn-raw-mosaic-masked-ln.tif'

# set the min/max ln-transformed population density data to rescale to 0-254 range
popln_min = -12.4
popln_max = 5.54
rescl_min = 0
rescl_max = 254
nodata = 255

# first, calculate the ln transformation on the population data
cmd = 'otbcli_BandMath -il {inf} -out {outf}?&gdal:co:COMPRESS=LZW -exp "ln(im1b1)"'.format(inf=popdn_inf, outf=popdn_tmp)
ccb.prnt.status('calculating population ln transformation')
ccb.prnt.status(cmd)
ccb.run(cmd)

# then, rescale this output to byte range to save space
cmd = 'gdal_translate -scale {srcmin} {srcmax} {dstmin} {dstmax} -a_nodata {nodata} -co COMPRESS=LZW {inf} {outf}'.format(
    srcmin=popln_min, srcmax=popln_max, dstmin=rescl_min, dstmax=rescl_max, nodata=nodata,
    inf=popdn_tmp, outf=popdn_out)
ccb.prnt.status('rescaling ln data')
ccb.prnt.status(cmd)
ccb.run(cmd)

# delete the temp file
os.remove(popdn_tmp)

# celebrate
ccb.prnt.status('finished rescaling population density raster!')