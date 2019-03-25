import glob


# set the base directory
base = '/home/salo/src/mosquito-mapping/raster/'

# set the nodata values to search/replace
oval = '-3.4028234663852885981e+38'
nval = '-9999'

# find all the ln transformed population rasters
rasters = glob.glob(base + '*/Population-ln.asc')
rasters.sort()
rasters.reverse()

# loop through and create new files with updated no data
for raster in rasters:
    outfile = raster[:-4] + '-nd.asc'
    
    # open the new file
    with open(outfile, 'w+') as outf:
        
        # read data line by line from the input file
        with open(raster, 'r+') as inf:
            
            # read the first 6 lines and put 'em in the output files
            for i in range(6):
                line = inf.readline()
                outf.write(line)

            for line in inf:
                split = line.split()
                newvals = [val.replace(oval, nval) for val in split]
                joined = ' '.join(newvals)
                outf.write(joined)
                outf.write('\n')