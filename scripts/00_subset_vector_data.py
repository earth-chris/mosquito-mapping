import ccb
import geopandas as gpd


# set paths
base = '/home/cba/src/mosquito-mapping/vector/'
outdir = '/home/cba/src/mosquito-mapping/maxent-inputs/'
aef = base + 'aedes-aegypti-KRGBIF.shp'
aaf = base + 'aedes-albopictus-KRGBIF.shp'
carf = base + 'borders-carribean.shp'
camf = base + 'borders-central-america.shp'
samf = base + 'borders-south-america.shp'

# set some strings for later
aegypti = 'aedes-aegypti'
albopictus = 'aedes-albopictus'
field='Name'

# convert the full data sets to maxent files
# aegypti
outf = '{dir}{sp}-all.csv'.format(dir=outdir, sp=aegypti)
cmd = 'vector-to-maxent -i {i} -o {o} -f {f}'.format(i=aef, o=outf, f=field)
#ccb.run(cmd)
# and albo
outf = '{dir}{sp}-all.csv'.format(dir=outdir, sp=albopictus)
cmd = 'vector-to-maxent -i {i} -o {o} -f {f}'.format(i=aaf, o=outf, f=field)
#ccb.run(cmd)

# read the data to begin subset
ae = gpd.read_file(aef)
aa = gpd.read_file(aaf)
car = gpd.read_file(carf)
cam = gpd.read_file(camf)
sam = gpd.read_file(samf)

# buffer things out to get a few extra points
car['geometry'] = car.buffer(0.1)
cam['geometry'] = cam.buffer(0.1)
sam['geometry'] = sam.buffer(0.1)

# set the background datasets
car_bg = cam.append(sam)
cam_bg = car.append(sam)
sam_bg = cam.append(car)
car_bg.reset_index(inplace=True)
cam_bg.reset_index(inplace=True)
sam_bg.reset_index(inplace=True)

# intersect each
ae_car = gpd.sjoin(ae, car, op='within')
ae_cam = gpd.sjoin(ae, cam, op='within')
ae_sam = gpd.sjoin(ae, sam, op='within')
ae_car_bg = gpd.sjoin(ae, car_bg, op='within')
ae_cam_bg = gpd.sjoin(ae, cam_bg, op='within')
ae_sam_bg = gpd.sjoin(ae, sam_bg, op='within')
ae_in = [ae_car, ae_cam, ae_sam]
ae_out = [ae_car_bg, ae_cam_bg, ae_sam_bg]

aa_car = gpd.sjoin(aa, car, op='within')
aa_cam = gpd.sjoin(aa, cam, op='within')
aa_sam = gpd.sjoin(aa, sam, op='within')
aa_car_bg = gpd.sjoin(aa, car_bg, op='within')
aa_cam_bg = gpd.sjoin(aa, cam_bg, op='within')
aa_sam_bg = gpd.sjoin(aa, sam_bg, op='within')
aa_in = [aa_car, aa_cam, aa_sam]
aa_out = [aa_car_bg, aa_cam_bg, aa_sam_bg]

zones=['car', 'cam', 'sam']
ins = [ae_in, aa_in]
outs = [ae_out, aa_out]
sp = [aegypti, albopictus]
vecs = [ins, outs]
labels = ['training', 'testing']

# write out the vectors and convert them to maxent formats
for i in range(len(sp)):
    for j in range(len(zones)):
        for k in range(len(labels)):
            # write the vector file
            outv = '{dir}{sp}-{zone}-{label}.shp'.format(dir=base, sp=sp[i], zone=zones[j], label=labels[k])
            vecs[k][i][j][['Name', 'geometry']].to_file(outv)
            
            # then convert the vector to maxent csv
            outm = '{dir}{sp}-{zone}-{label}.csv'.format(dir=outdir, sp=sp[i], zone=zones[j], label=labels[k])
            cmd = '/home/cba/src/ccb/bin/vector-to-maxent -i {i} -o {o} -f {f}'.format(i=outv, o=outm, f='Name')
            ccb.run(cmd)