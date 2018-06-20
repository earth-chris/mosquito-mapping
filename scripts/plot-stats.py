import aei
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib tk

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
tbls = base + 'tables/'
plts = base + 'plots/'
ae_all_f = tbls + 'aedes-aegypti-all.csv'
ae_car_f = tbls + 'aedes-aegypti-caribbean.csv'
ae_cam_f = tbls + 'aedes-aegypti-central-america.csv'
ae_sam_f = tbls + 'aedes-aegypti-south-america.csv'
aa_all_f = tbls + 'aedes-albopictus-all.csv'
aa_car_f = tbls + 'aedes-albopictus-caribbean.csv'
aa_cam_f = tbls + 'aedes-albopictus-central-america.csv'
aa_sam_f = tbls + 'aedes-albopictus-south-america.csv'
bg_all_f = tbls + 'background-all.csv'
bg_car_f = tbls + 'background-caribbean.csv'
bg_cam_f = tbls + 'background-central-america.csv'
bg_sam_f = tbls + 'background-south-america.csv'

# read the data into memory
ae_all = pd.read_csv(ae_all_f)
ae_car = pd.read_csv(ae_car_f)
ae_cam = pd.read_csv(ae_cam_f)
ae_sam = pd.read_csv(ae_sam_f)
aa_all = pd.read_csv(aa_all_f)
aa_car = pd.read_csv(aa_car_f)
aa_cam = pd.read_csv(aa_cam_f)
aa_sam = pd.read_csv(aa_sam_f)
bg_all = pd.read_csv(bg_all_f)
bg_car = pd.read_csv(bg_car_f)
bg_cam = pd.read_csv(bg_cam_f)
bg_sam = pd.read_csv(bg_sam_f)

# remove no-data values
ae_all = ae_all[ae_all['SoilCover'] != 255]
ae_car = ae_car[ae_car['SoilCover'] != 255]
ae_cam = ae_cam[ae_cam['SoilCover'] != 255]
ae_sam = ae_sam[ae_sam['SoilCover'] != 255]
aa_all = aa_all[aa_all['SoilCover'] != 255]
aa_car = aa_car[aa_car['SoilCover'] != 255]
aa_cam = aa_cam[aa_cam['SoilCover'] != 255]
aa_sam = aa_sam[aa_sam['SoilCover'] != 255]

# set the fields
fields = ae_all.columns[1:]
labels = ['Soil cover', 'Vegetation cover', 'Impervious cover', 'Minimum temperature', 'Median temperature',
    'Maximum temperature', 'Tree cover', 'Population density']
units = ['%', '%', '%', 'C', 'C', 'C', '%', 'people per ha']
group_labels = ['Background', 'Aedes aegypti', 'Aedes albopictus']

# set group labels to show the number of points
group_labels_all = []
group_labels_car = []
group_labels_cam = []
group_labels_sam = []
for i in range(len(group_labels)): 
    group_lables_all.append
    group_labels_car = []
    group_labels_cam = []
    group_labels_sam = []

#cb = aei.color.color_blind()
#cols = [cb[1], cb[3], cb[6]]

# ok, let's first plot out the full extent's distributions by variable
for i in range(len(fields)):
    # set up general data per plot
    xlabel = "{} ({})".format(labels[i], units[i])
    title = "{} distributions\nExtent - Latin America and the Caribbean\nGrain size - 1 km".format(labels[i])
    group_labels_all = []
    group_labels_all.append("{} (n={})".format(group_labels[0], len(bg_all)))
    group_labels_all.append("{} (n={})".format(group_labels[1], len(ae_all)))
    group_labels_all.append("{} (n={})".format(group_labels[2], len(aa_all)))
    
    # set up the full plots
    plt.figure(figsize=(5, 5), dpi=150)
    plt = aei.plot.density_dist([bg_all[fields[i]], ae_all[fields[i]], aa_all[fields[i]]],
        plot=plt, fill=True, label=group_labels_all, xlabel=xlabel, title=title, cutoff=2)
        
    # save the figure
    plt.savefig("{}global-1km-{}.png".format(plts, fields[i]), dpi=200)
    plt.close()
    

# ok, let's do that again for the caribbean
for i in range(len(fields)):
    # set up general data per plot
    xlabel = "{} ({})".format(labels[i], units[i])
    title = "{} distributions\nExtent - the Caribbean\nGrain size - 1 km".format(labels[i])
    group_labels_car = []
    group_labels_car.append("{} (n={})".format(group_labels[0], len(bg_car)))
    group_labels_car.append("{} (n={})".format(group_labels[1], len(ae_car)))
    group_labels_car.append("{} (n={})".format(group_labels[2], len(aa_car)))
    
    # set up the full plots
    plt.figure(figsize=(5, 5), dpi=150)
    plt = aei.plot.density_dist([bg_car[fields[i]], ae_car[fields[i]], aa_car[fields[i]]],
        plot=plt, fill=True, label=group_labels_car, xlabel=xlabel, title=title, cutoff=2)
        
    # save the figure
    plt.savefig("{}caribbean-1km-{}.png".format(plts, fields[i]), dpi=200)
    plt.close()
    
    
    
# ok, let's do that again for central america
for i in range(len(fields)):
    # set up general data per plot
    xlabel = "{} ({})".format(labels[i], units[i])
    title = "{} distributions\nExtent - Central America\nGrain size - 1 km".format(labels[i])
    group_labels_cam = []
    group_labels_cam.append("{} (n={})".format(group_labels[0], len(bg_cam)))
    group_labels_cam.append("{} (n={})".format(group_labels[1], len(ae_cam)))
    group_labels_cam.append("{} (n={})".format(group_labels[2], len(aa_cam)))
    
    # set up the full plots
    plt.figure(figsize=(5, 5), dpi=150)
    plt = aei.plot.density_dist([bg_cam[fields[i]], ae_cam[fields[i]], aa_cam[fields[i]]],
        plot=plt, fill=True, label=group_labels_cam, xlabel=xlabel, title=title, cutoff=2)
        
    # save the figure
    plt.savefig("{}central-america-1km-{}.png".format(plts, fields[i]), dpi=200)
    plt.close()
    
    
# and finall for south america    
for i in range(len(fields)):
    # set up general data per plot
    xlabel = "{} ({})".format(labels[i], units[i])
    title = "{} distributions\nExtent - South America\nGrain size - 1 km".format(labels[i])
    group_labels_sam = []
    group_labels_sam.append("{} (n={})".format(group_labels[0], len(bg_sam)))
    group_labels_sam.append("{} (n={})".format(group_labels[1], len(ae_sam)))
    group_labels_sam.append("{} (n={})".format(group_labels[2], len(aa_sam)))
    
    # set up the full plots
    plt.figure(figsize=(5, 5), dpi=150)
    plt = aei.plot.density_dist([bg_sam[fields[i]], ae_sam[fields[i]], aa_sam[fields[i]]],
        plot=plt, fill=True, label=group_labels_sam, xlabel=xlabel, title=title, cutoff=2)
        
    # save the figure
    plt.savefig("{}south-america-1km-{}.png".format(plts, fields[i]), dpi=200)
    plt.close()
    

# ok, now we're going to plot out 
    
    
    
    