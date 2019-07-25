import ccb
import glob
from matplotlib import lines
%matplotlib tk

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
plots = base + 'plots/'
ae_pck = base + 'scripts/ae-auc.pck'
aa_pck = base + 'scripts/aa-auc.pck'

# read 'em in to memory
aa = ccb.read.pck(aa_pck)
ae = ccb.read.pck(ae_pck)

# subset to mean and stdev for the cross validation
aa_mn = aa.mean(axis=0)
ae_mn = ae.mean(axis=0)
aa_sd = aa.std(axis=0)
ae_sd = ae.std(axis=0)

# set the colors 
#c_env = ["#56B4E9", "#009E73", "#CC79A7"]
c_ext = ["#56B4E9", "#009E73", "#E69F00", "#CC79A7", '#F0E442', '#424243', '#ffffff']
c_env = c_ext
c_bar = ['#424243']

# set vector-specific colors
c_ae = '#CC79A7'
c_aa = '#E69F00'

# set the labels for each 
#l_env = ['climate', 'land cover', 'all']
#env = ['cld', 'lst', 'luc', 'pop', 'envs']
env = ['pcp', 'luc', 'lst', 'pop', 'all']
#l_env = ['Cloud\ncover', 'Temperature', 'Land\ncover', 'Population\ndensity', 'all']
l_env = ['Precipitation', 'Land cover', 'Temperature', 'Population\ndensity', 'all']
l_ext = ['Full extent', 'Central America', 'Caribbean', 'South America']
l_scl = ['1 km', '5 km', '10 km', '50 km', '100 km']
n_scl = [1000, 5000, 10000, 50000, 100000]

# function to create legend proxies
def create_proxy(color, marker, linestyle='none'):
    line = lines.Line2D([0], [0], linestyle=linestyle, mfc=color,
        mec='black', marker=marker)
    return line

################################################
# JOINT PLOTTING
plt.figure(figsize=(4, 4), dpi=150)

# do some stuff to index the boxplots backwards from how they're saved
order = [3, 2, 1, 0]
order = [2, 0, 1, 3]
env_arr = np.array(l_env[:4])

# set the plot
inds = np.arange(4)
inds_ae = inds-0.15
inds_aa = inds+0.15

# do the boxplot
aa_bx = aa[:4, :, 0, 0]
ae_bx = ae[:4, :, 0, 0]
width=0.25

# ae first
bp = plt.boxplot(ae_bx[:, order], patch_artist=True, 
    positions=inds_ae, widths=width)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color=c_bar[0], alpha=0.8)
    
for element in ['boxes']:
    plt.setp(bp[element], color=c_ae)

for i, patch in enumerate(bp['boxes']):
    patch.set(facecolor=c_ae)
    
# aa next
bp = plt.boxplot(aa_bx[:, order], patch_artist=True, positions=inds_aa, 
    widths=width)
for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color=c_bar[0], alpha=0.8)

for element in ['boxes']:
    plt.setp(bp[element], color=c_aa)

for i, patch in enumerate(bp['boxes']):
    patch.set(facecolor=c_aa)


# set the labels
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(inds, env_arr[order], fontsize=8.5)
plt.xlim(-0.75, 3.75)
plt.ylabel('AUC (mean)')
plt.title('Drivers of habitat suitability')

# set ticks and labels
ylim = [0.5, 1.0]
#ylim = [0.725, 0.875]
#step = 0.025
#yticks = np.round((np.arange(ylim[0], ylim[1], step)), 3)
#ytick_s = ['{:0.3f}'.format(ytick) for ytick in yticks]
#plt.yticks(yticks, ytick_s)
plt.ylim(ylim)

xlabels = ax.set_xticklabels(env_arr[order])
for i, xlabel in enumerate(xlabels):
    xlabel.set_y(xlabel.get_position()[1] - (i % 2) * 0.045)

# set the legend
legend_labels = ['$\it{Aedes\ aegypti}$', '$\it{Aedes\ albopictus}$']
legend_colors = [c_ae, c_aa]
legend_markers = ['s', 's']
proxies = []
for i in range(len(legend_labels)):
    proxies.append(create_proxy(legend_colors[i], legend_markers[i]))
plt.legend(proxies, legend_labels, loc='upper right', fontsize=8.5)
plt.tight_layout()

# save and close up
plt.savefig(plots + 'figure-2.png', dpi=600)
plt.savefig(plots + 'figure-2.svg')
plt.close()


################################################
# ERROR BARS

# create the figure
plt.figure(figsize=(4, 4), dpi=150)

# do some stuff to index the boxplots backwards from how they're saved
order = [3, 2, 1, 0]
env_arr = np.array(l_env[:4])

# set the plot
inds = np.arange(4)
plt.errorbar(inds, ae_mn[:, 0, 0][order], yerr=ae_sd[:, 0, 0][order], color=c_ae, 
    ecolor=c_bar[0], fmt='o', markersize=10, label='$\it{Aedes\ aegypti}$', 
    markeredgecolor='black', markeredgewidth=0.5)

# loop through and annotate each point
for i, item in enumerate(order):
    plt.annotate(r'$\sigma={:0.3f}$'.format(ae_sd[:, 0, 0][item]), 
        [inds[i]-0.4, ae_mn[:, 0, 0][item]-0.04])
    
#plt.errorbar(inds, aa_mn[:, 0, 0][order], yerr=aa_sd[:, 0, 0][order], color=c_aa, 
#    ecolor=c_bar[0], fmt='o', markersize=10, label='$\it{Aedes\ albopictus}$')

# set the labels
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(inds, env_arr[order], fontsize=8.5)
plt.ylim(0.5, 1.0)
plt.xlim(-0.5, 3.5)
plt.ylabel('AUC (mean)')
plt.title('A)  $\it{Aedes\ aegypti}$')
#plt.title('Drivers of habitat suitability')
#plt.legend()
plt.tight_layout()

# save and close up
plt.savefig(plots + 'aedes-aegypti-drivers.png', dpi=150)
plt.savefig(plots + 'aedes-aegypti-drivers.svg')
plt.close()

#####
# do it again for the albo

# create the figure
plt.figure(figsize=(4, 4), dpi=150)

# do some stuff to index the boxplots backwards from how they're saved
order = [3, 2, 1, 0]
env_arr = np.array(l_env[:4])

# set the plot
inds = np.arange(4)
plt.errorbar(inds, aa_mn[:, 0, 0][order], yerr=aa_sd[:, 0, 0][order], color=c_aa, 
    ecolor=c_bar[0], fmt='o', markersize=10, label='$\it{Aedes\ albopictus}$',
    markeredgecolor='black', markeredgewidth=0.5)
    
# loop through and annotate each point
for i, item in enumerate(order):
    plt.annotate(r'$\sigma={:0.3f}$'.format(aa_sd[:, 0, 0][item]), 
        [inds[i]-0.4, aa_mn[:, 0, 0][item]-0.04])

# set the labels
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(inds, env_arr[order], fontsize=8.5)
plt.ylim(0.5, 1.0)
plt.xlim(-0.5, 3.5)
plt.ylabel('Mean AUC')
plt.title('B)  $\it{Aedes\ albopictus}$')
plt.tight_layout()

# save and close up
plt.savefig(plots + 'aedes-albopictus-drivers.png', dpi=150)
plt.savefig(plots + 'aedes-albopictus-drivers.svg')
plt.close()


################################################
# BOXPLOTS

# do boxplots for each vector using the bootstraps
# should be in rows: n_folds, cols: covariates
aa_bx = aa[:4, :, 0, 0]
ae_bx = ae[:4, :, 0, 0]

# do some stuff to index the boxplots
order = [3, 2, 1, 0]
env_arr = np.array(l_env[:4])

# create the figure
plt.figure(figsize=(4, 4), dpi=150)

# set some weird boxplots stuff
bp = plt.boxplot(ae_bx[:, order], patch_artist=True)
for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color=c_bar[0])

for i, patch in enumerate(bp['boxes']):
    patch.set(facecolor=c_env[i])
    
# set the labels
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
xticks = plt.xticks()
plt.xticks(xticks[0], env_arr[order])
plt.ylim(0.5, 1.0)
plt.ylabel('AUC')
plt.title('Environmental drivers of suitability\n$\it{Aedes\ aegypti}$')

# clean up and save
plt.tight_layout()
plt.savefig(plots + 'aedes-aegypti-drivers.png', dpi=150)
plt.close()

# create the figure for albopictus
plt.figure(figsize=(4, 4), dpi=150)

# set some weird boxplots stuff
bp = plt.boxplot(aa_bx[:, order], patch_artist=True)
for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp[element], color=c_bar[0])

for i, patch in enumerate(bp['boxes']):
    patch.set(facecolor=c_env[i])
    
# set the labels
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
xticks = plt.xticks()
plt.xticks(xticks[0], env_arr[order])
plt.ylim(0.5, 1.0)
plt.ylabel('AUC')
plt.title('Environmental drivers of suitability\n$\it{Aedes\ albopictus}$')

# clean up and save
plt.tight_layout()
plt.savefig(plots + 'aedes-albopictus-drivers.png', dpi=150)
plt.close()

# ok, plot out the data across all extents by environmental data used and by scale
plt.figure(figsize=(4.5, 4.5), dpi=200)
nbins = len(l_scl)
width = 0.175
space = 0.0
ind1 = np.arange(nbins)
ind2 = np.arange(nbins) + (width + space)
ind3 = np.arange(nbins) + 2 * (width + space)
ind4 = np.arange(nbins) + 3 * (width + space)
ind5 = np.arange(nbins) + 4 * (width + space)
ind6 = np.arange(nbins) + 5 * (width + space)
inds = [ind1, ind2, ind3, ind4, ind5, ind6]

# plot aegypti first
for i in range(len(l_env)):
    plt.bar(inds[i], ae_mn[i, 0, :], width, color=c_env[i], label=l_env[i], edgecolor='#424243',
        yerr=ae_sd[i, 0, :])
    #plt.errorbar(inds[i], ae_mn[i, 0, :], yerr=ae_sd[i, 0, :], color=c_env[i], ecolor=c_bar, fmt='o')

# set the labels and legend
sp = 'Aedes aegypti'
plt.ylim(0.5, 1)
plt.xticks(ind2+(width/2), l_scl)
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
    plt.bar(inds[i], aa_mn[i, 0, :], width, color=c_env[i], label=l_env[i], edgecolor='#424243',
        yerr=aa_sd[i, 0, :])
    
# set the labels and legend
sp = 'Aedes albopictus'
plt.ylim(0.5, 1)
plt.xticks(ind2+(width/2), l_scl)
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
    plt.bar(inds[i], ae_mn[4, i, :], width, color=c_ext[i], label=l_ext[i], edgecolor='#424243',
        yerr=ae_sd[4, i, :])
    
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
plt.savefig(plots + 'Extent variation - {} - all.png'.format(sp), dpi=300)
plt.close()

# albopictus next!
plt.figure(figsize=(4.5, 4.5), dpi=200)
for i in range(len(l_ext)):
    plt.bar(inds[i], aa_mn[4, i, :], width, color=c_ext[i], label=l_ext[i], edgecolor='#424243',
        yerr=aa_sd[4, i, :])
    
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
plt.savefig(plots + 'Extent variation - {} - all.png'.format(sp), dpi=300)
plt.close()


