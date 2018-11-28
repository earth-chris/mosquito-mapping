import ccb
import glob

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
plots = base + 'plots/'
ae_pck = base + 'scripts/ae-auc.pck'
aa_pck = base + 'scripts/aa-auc.pck'

# read 'em in to memory
aa = ccb.read.pck(aa_pck)
ae = ccb.read.pck(ae_pck)

# set the colors 
#c_env = ["#56B4E9", "#009E73", "#CC79A7"]
c_ext = ["#009E73", "#56B4E9", "#E69F00", "#CC79A7"]
c_env = c_ext

# set the labels for each 
#l_env = ['climate', 'land cover', 'all']
l_env = ['lai', 'cloud cover', 'temperature', 'all']
l_ext = ['Full extent', 'Central America', 'Caribbean', 'South America']
l_scl = ['1 km', '5 km', '10 km', '50 km', '100 km']
n_scl = [1000, 5000, 10000, 50000, 100000]


# ok, plot out the data across all extents by environmental data used and by scale
plt.figure(figsize=(4.5, 4.5), dpi=200)
nbins = len(l_scl)
width = 0.225
space = 0.0
ind1 = np.arange(nbins)
ind2 = np.arange(nbins) + (width + space)
ind3 = np.arange(nbins) + 2 * (width + space)
ind4 = np.arange(nbins) + 3 * (width + space)
inds = [ind1, ind2, ind3, ind4]

# plot aegypti first
for i in range(len(l_env)):
    plt.bar(inds[i], ae[i, 0, :], width, color=c_env[i], label=l_env[i], edgecolor='#424243')
    
# set the labels and legend
sp = 'Aedes aegypti'
plt.ylim(0.5, 1)
plt.xticks(ind2, l_scl, rotation='vertical')
plt.ylabel('AUC (mean)')
plt.xlabel('Grain size')
plt.title(sp, fontstyle='italic')
plt.legend(ncol=1, loc='upper right')
plt.tight_layout()

# save the figs
plt.savefig(plots + 'Environmental variation - {}.png'.format(sp), dpi=300)
plt.close()

# now for aedes albopictus
plt.figure(figsize=(4.5, 4.5), dpi=200)
for i in range(len(l_env)):
    plt.bar(inds[i], aa[i, 0, :], width, color=c_env[i], label=l_env[i], edgecolor='#424243')
    
# set the labels and legend
sp = 'Aedes albopictus'
plt.ylim(0.5, 1)
plt.xticks(ind2, l_scl, rotation='vertical')
plt.ylabel('AUC (mean)')
plt.xlabel('Grain size')
plt.title(sp, fontstyle='italic')
plt.legend(ncol=1, loc='upper right')
plt.tight_layout()

# save the figs
plt.savefig(plots + 'Environmental variation - {}.png'.format(sp), dpi=300)
plt.close()


# ok, now plot by different holdouts
plt.figure(figsize=(4.5, 4.5), dpi=200)
nbins = len(l_scl)
width = 0.175
space = 0.0
ind1 = np.arange(nbins)
ind2 = np.arange(nbins) + (width + space)
ind3 = np.arange(nbins) + 2 * (width + space)
ind4 = np.arange(nbins) + 3 * (width + space)
inds = [ind1, ind2, ind3, ind4]

# plot aegypti first
for i in range(len(l_ext)):
    plt.bar(inds[i], ae[2, i, :], width, color=c_ext[i], label=l_ext[i], edgecolor='#424243')
    
# set the labels and legend
sp = 'Aedes aegypti'
plt.ylim(0.5, 1)
plt.xticks((ind1 + ind4) / 2, l_scl, rotation='vertical')
plt.ylabel('AUC (mean)')
plt.xlabel('Grain size')
plt.title(sp, fontstyle='italic')
plt.legend(ncol=1, loc='upper right')
plt.tight_layout()

# save 'er up
plt.savefig(plots + 'Extent variation - {}.png'.format(sp), dpi=300)
plt.close()

# albopictus next!
plt.figure(figsize=(4.5, 4.5), dpi=200)
for i in range(len(l_ext)):
    plt.bar(inds[i], aa[2, i, :], width, color=c_ext[i], label=l_ext[i], edgecolor='#424243')
    
# set the labels and legend
sp = 'Aedes albopictus'
plt.ylim(0.5, 1)
plt.xticks((ind1 + ind4) / 2, l_scl, rotation='vertical')
plt.ylabel('AUC (mean)')
plt.xlabel('Grain size')
plt.title(sp, fontstyle='italic')
plt.legend(ncol=1, loc='upper right')
plt.tight_layout()

# save 'er up
plt.savefig(plots + 'Extent variation - {}.png'.format(sp), dpi=300)
plt.close()


