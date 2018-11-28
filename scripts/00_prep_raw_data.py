import os
import ccb

# set the base files to use
base = '/home/salo/src/mosquito-mapping/raster/'
raw = base + 'raw/'
scratch = base + 'scratch/'
outd = base

# set the vector mask file
burn_vector = '/home/salo/src/mosquito-mapping/vector/borders-usa-buffered.shp'

# set the raster files to process
raster_cld = [
    'LACR-CLD-kurtosis.tif',
    'LACR-CLD-mean.tif',
    'LACR-CLD-skewness.tif',
    'LACR-CLD-variance.tif'
]

raster_lai = [
    'LACR-LAI-kurtosis.tif',
    'LACR-LAI-mean.tif',
    'LACR-LAI-skewness.tif',
    'LACR-LAI-variance.tif'
]

raster_lst = [
    'LACR-LST-kurtosis.tif',
    'LACR-LST-mean.tif',
    'LACR-LST-skewness.tif',
    'LACR-LST-variance.tif'
]

raster_pop = 'LACR-pop-density-2015.tif' # data average resampled 

# output projection
proj = 'EPSG:54009' # molleweide
#proj = 'EPSG:54017' # behrman

# output scales
scales = [1000, 5000, 10000, 50000, 100000]

# output data format
of = 'AAIGrid'


#####
# first, convert all the nans to 0s in the LAI data
raster_lai_nd = []
for f in raster_lai:
    outf = '{}{}-nonan.tif'.format(scratch, f[:-4])
    raster_lai_nd.append(outf)
    cmd = 'gdal_calc.py -A {} --outfile={} --co=COMPRESS=LZW --calc="nan_to_num(A)"'.format(
        raws+f, outf)
    print(cmd)
    ccb.run(cmd)
    
    
#####
# then, get the nodata values from the LST / Cloud data
msk_cld = scratch+'mask-cld.tif'
msk_lst = scratch+'mask-lst.tif'
msk_final = scratch+'mask-final.tif'

cmd = 'otbcli_ManageNoData -usenan true -in {} -out "{}?&gdal:co:COMPRESS=LZW" uint8'.format(raw+raster_cld[0], msk_cld)
print(cmd)
ccb.run(cmd)

cmd = 'otbcli_ManageNoData -usenan true -in {} -out "{}?&gdal:co:COMPRESS=LZW" uint8'.format(raw+raster_lst[0], msk_lst)
print(cmd)
ccb.run(cmd)

# merge these masks
cmd = 'otbcli_BandMath -il {} {} -out "{}?&gdal:co:COMPRESS=LZW" uint8 -exp "im1b1 * im2b1"'.format(
    msk_cld, msk_lst, msk_final)
print(cmd)
ccb.run(cmd)


#####
# apply the final mask to each data file
masked_files = []

# first, update the paths for the lst/cld data
raster_cld_path = []
raster_lst_path = []
for i in range(len(raster_cld)):
    raster_cld_path.append(raw + raster_cld[i])
    raster_lst_path.append(raw + raster_lst[i])
    
to_mask = raster_lai_nd + raster_cld_path + raster_lst_path
to_mask.append(raw + raster_pop)

for f in to_mask:
    # set the output file name
    outf = '{}-masked.tif'.format(scratch + os.path.basename(f)[:-4])
    masked_files.append(outf)
    
    # set the input file nodata to be consistent
    cmd = 'gdal_edit.py -a_nodata -9999 {}'.format(f)
    print(cmd)
    ccb.run(cmd)
    
    # apply the mask
    cmd = 'otbcli_ManageNoData -in {} -out "{}?&gdal:co:COMPRESS=LZW" -mode apply -mode.apply.mask {}'.format(
        f, outf, msk_final)
    print(cmd)
    ccb.run(cmd)
    
    
#####
# also, mask the  US out of these data
for f in masked_files:
    cmd = 'gdal_rasterize -burn -9999 {} {}'.format(burn_vector, f)
    print(cmd)
    ccb.run(cmd)
    
    
#####
# stack these data into a single mosaic
stack = scratch + 'masked-stack.tif'
cmd = 'otbcli_ConcatenateImages -il {} -out "{}?&gdal:co:COMPRESS=LZW"'.format(
    ' '.join(masked_files), stack)
print(cmd)
ccb.run(cmd)

# make sure everything is set cleanly in gdal
ccb.run('gdal_edit.py -a_nodata -9999 {}'.format(stack))
ccb.run('gdal_edit.py -unsetstats {}'.format(stack))
ccb.run('gdal_edit.py -stats {}'.format(stack))
ccb.run('gdaladdo -ro -r average {} 2 4 8 16 32 64 128 256'.format(stack))


#####
# reproject and rescale the data to the different output scales
output_stacks = []
for res in scales:
    outf = '{}{:06d}-m/stacked-layers.tif'.format(base, res)
    output_stacks.append(outf)
    cmd = 'gdalwarp -multi -co COMPRESS-LZW -r bilinear -t_srs {srs} -tr {res} {res} {inf} {outf}'.format(
        srs=proj, res=res, inf=stack, outf=outf)
    print(cmd)
    ccb.run(cmd)
    

#####
# now convert each layer to ascii grid for maxent
bnames = [
    'LAI-kurtosis',
    'LAI-mean',
    'LAI-skew',
    'LAI-variance',
    'CLD-kurtosis',
    'CLD-mean',
    'CLD-skew',
    'CLD-variance',
    'LST-kurtosis',
    'LST-mean',
    'LST-skew',
    'LST-variance',
    'Population'
]

for i in range(len(scales)):
    for j in range(len(bnames)):
        outf = '{}{:06d}-m/{}.asc'.format(base, scales[i], bnames[j])
        cmd = 'gdal_translate -of {of} -b {b} {inf} {outf}'.format(
            of=of, b=j+1, inf=output_stacks[i], outf=outf)
        print(cmd)
        ccb.run(cmd)
        

#####
# then, dumbly, do the log transform on the population data separately
for i in range(len(scales)):
    outf = '{}{:06d}-m/Population-ln.tif'.format(base, scales[i])
    cmd = 'otbcli_BandMath -il {inf} -out "{outf}?&gdal:co:COMPRESS=LZW" -exp "exp(im1b13)"'.format(
        inf=output_stacks[i], outf=outf)
    print(cmd)
    ccb.run(cmd)
    
    outf_ln = '{}{:06d}-m/Population-ln.asc'.format(base, scales[i])
    cmd = 'gdal_translate -overwrite -of {of} {inf} {outf}'.format(
        of=of, inf=outf, outf=outf_ln)
    print(cmd)
    ccb.run(cmd)