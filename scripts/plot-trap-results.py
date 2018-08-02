import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib tk


# set the files and directories
base = '/home/cba/src/mosquito-mapping/'
tbls = base + 'scratch/'
plts = base + 'plots/'

sp_target_file = tbls + 'cr-samples-target.csv'
sp_nontarget_file = tbls + 'cr-samples-non-target.csv'

# read 'em and weep
sp_target = pd.read_csv(sp_target_file)
sp_nontarget = pd.read_csv(sp_nontarget_file)

# get the unique trap types
method_target = sp_target['Method'].unique().tolist()
method_nontarget = sp_nontarget['Method'].unique().tolist()
method_target.sort()
method_nontarget.sort()

# first plot out the number of captures by trap type
group_nontarget = sp_nontarget.groupby('Method')
count_nontarget = group_nontarget.size().tolist()

# plot out the results
plt.figure(figsize=(5,4), dpi=150)
nbins = len(method_nontarget)
binsize = 0.85
bins = np.arange(nbins) - binsize
plt.bar(bins, count_nontarget, binsize, align='center', label='non-Aedes spp')
plt.xticks(bins, method_nontarget)
plt.xlabel('Sampling method')
plt.ylabel('Count')
plt.legend()
plt.title('Mosquito trapping evaluation')
plt.tight_layout()
plt.savefig(plts + 'sampling-nontarget-species.png', dpi=300)
plt.close()

# now get the number of captures for Aedes species
sp_unique = sp_target['Species'].unique().tolist()
sp_unique.sort()
n_sp = len(sp_unique)
n_methods = len(method_target)
countarr = np.zeros((n_sp, n_methods))

for i in range(n_methods):
    for j in range(n_sp):
        ind_method = sp_target['Method'] == method_target[i]
        ind_sp = sp_target['Species'] == sp_unique[j]
        countarr[j,i] = (ind_sp & ind_method).sum()
        
# make a stacked bar plot for each species broken down by method
plt.figure(figsize=(5,4), dpi=150)
nbins = len(method_target)
binsize = 0.85
bins = np.arange(nbins) - binsize

plt.bar(bins, countarr[0], binsize, align='center', label=sp_unique[0], bottom=countarr[2] + countarr[1])
plt.bar(bins, countarr[1], binsize, align='center', label=sp_unique[1], bottom=countarr[2])
plt.bar(bins, countarr[2], binsize, align='center', label=sp_unique[2])
plt.xticks(bins, method_target)
plt.xlabel('Sampling method')
plt.ylabel('Count')
plt.legend()
plt.title('Mosquito trapping evaluation')
plt.tight_layout()
plt.savefig(plts + 'sampling-target-species.png', dpi=300)
plt.close()


# now plot out the proportion of aedes captured per method
count_all = (np.array(count_nontarget[1:4])).astype(np.float32)
count_aed = (countarr.sum(axis=0))[1:4]
ratio = 100 * count_aed / count_all
label = method_target[1:4]
nbins = len(labels)
binsize = 0.85
bins = np.arange(nbins) - binsize
plt.figure(figsize=(5,4), dpi=150)
plt.bar(bins, ratio, binsize, align='center', label='proportion of Aedes\nto non-Aedes captures')
plt.xticks(bins, label)
plt.xlabel('Sampling method')
plt.ylabel('%')
plt.title('Sampling specificity')
plt.legend()
plt.tight_layout()
plt.savefig(plts + 'sampling-precision.png', dpi=300)
plt.close()
