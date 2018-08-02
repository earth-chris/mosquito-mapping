import ccb
import geopandas as gpd


# set the input and output files
base = '/home/cba/src/mosquito-mapping/'
infile = base + 'vector/culicidae-all.shp'
out_vec = base + 'vector/culicidae-nontarget.shp'
out_csv = base + 'vector/culicidae-nontarget.csv'
out_epsg = 3410
out_field = 'family'

# set the vectors to exclude from the output bias file
to_remove = ['Aedes aegypti', 'Aedes albopictus']

# read the full shapefile data into memory
input_vector = gpd.read_file(infile)

# get the list of unique species
sp_list = input_vector['species'].unique().tolist()
sp_list.sort()

# loop through the unique species and remove the target vectors
for sp in to_remove:
    sp_list.remove(sp)
    
# then subset the original vector to just the non-target records
ind = input_vector['species'].isin(sp_list)
output_vector = input_vector[ind]
output_vector.to_file(out_vec)

# and convert the vector file to maxent format
cmd_str = 'vector-to-maxent -i {i} -o {o} -e {e} -f {f}'.format(i=out_vec, o=out_csv, e=out_epsg, f=out_field)
ccb.run(cmd_str)