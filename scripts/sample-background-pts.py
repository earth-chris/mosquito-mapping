import aei
import ccb
import glob
import pickle
import numpy as np
from scipy import stats
import geopandas as gpd
import matplotlib as mpl
from matplotlib import ticker
from matplotlib import pyplot as plt

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
plots = base + 'plots/'
rpath = base + 'raster/001000-m/'
bias_file = base + '/maxent-outputs/bias-file-001000-m/Culicidae.asc'
#ae_file = base + 'vector/aegypti-54009-3.shp'
#aa_file = base + 'vector/albopictus-54009-3.shp'
ae_file = base + 'vector/aedes-aegypti-resampled-extract-precip.shp'
aa_file = base + 'vector/aedes-albopictus-resampled-extract-precip.shp'
bck_file = base + 'scripts/background_data.pck'

# set the font size
mpl.rcParams.update({'font.size': 20})
fs_xlabel = 22

# set the colors
c_cld = "#56B4E9" 
c_pcp = "#56B4E9" 
c_lst = "#E69F00"
c_lc = "#009E73" 
c_pop = "#CC79A7"
c_bck = "#424243"

# set vector-specific colors
c_ae = '#CC79A7'
c_aa = '#E69F00'

# set the number of points
n_pts = 10000

# create a list to store the background data
bck_data = list()

# set the seed for consistent random sampling
np.random.seed(1985)

# read the bias file into memory
no_data = -9999
#bias_ref = ccb.read.raster(bias_file)
#bias_ref.read_all()
#gd = bias_ref.data != no_data
#bias = bias_ref.data[gd]

# clear memory
bias_ref.data = None
bias_ref = None

# calculate the length of the array to sample
n_vals = gd.sum()
inds = np.arange(n_vals)

# randomly sample the good data values
p = bias / bias.sum()
samples = np.random.choice(inds, size=n_pts, replace=False, p=p)


# ok! we have our random samples now.
# time to plot these data

# read the extracted vector data into memory
ae = gpd.read_file(ae_file)
aa = gpd.read_file(aa_file)

# read the background data from the pickle file
with open(bck_file, 'rb') as f:
    bck_data = pickle.load(f)

# set the corresponding vector fields with the raster data to read
fields = ['LAI_k', 'LAI_m', 'LAI_s', 'LAI_v', 'LC-bare', 'LC-trees',
          'CLD_k', 'CLD_m', 'CLD_s', 'CLD_v', 'LST_k',
          'LST_m', 'LST_s', 'LST_v', 'POP', 'PCP_m', 'PCP_v', 'PCP_s']

rasters = ['LAI-kurtosis.asc',
           'LAI-mean.asc',
           'LAI-skew.asc',
           'LAI-variance.asc',
           'LC-Bare.asc',
           'LC-Trees.asc',
           'CLD-kurtosis.asc',
           'CLD-mean.asc',
           'CLD-skew.asc',
           'CLD-variance.asc',
           'LST-kurtosis.asc',
           'LST-mean.asc',
           'LST-skew.asc',
           'LST-variance.asc',
           'Population-ln-nd.asc',
           'PCP-mean.asc',
           'PCP-variance.asc',
           'PCP-skew.asc']
           
xlabels = ['leaf area index\nkurtosis',
           'leaf area index\nmean',
           'leaf area index\nskew',
           'leaf area index\nvariance',
           'bare ground\n ',
           'tree cover\n ',
           'cloud cover\nkurtosis',
           'cloud cover\nmean',
           'cloud cover\nskew',
           'cloud cover\nvariance',
           'temperature\nkurtosis',
           'temperature\nmean',
           'temperature\nskew',
           'temperature\nvariance',
           'population\ndensity',
           'precipitation\nmean',
           'precipitation\nvariance',
           'precipitation\nskew']
"""           
fields = ['PCP_m', 'PCP_v', 'PCP_s']

rasters = ['PCP-mean.asc',
           'PCP-variance.asc',
           'PCP-skew.asc']
           
xlabels = ['precipitation\nmean',
           'precipitation\nvariance',
           'precipitation\nskew']
"""

units = {
    'lai': "\n($m^2\ m^{-2}$)",
    'lc': "\n($\%$)",
    'lst': "\n($C$)",
    'pcp': "\n($mm\ mo^{-1}$)",
    'pop': "\n($people\ ha^{-1}$)"
}
           
# create a list to store the min/max x/y values for plotting later
xlims = list()
ylims = list()

# jk, use these ylim values that i calculated (using the above variables!)
xlims = [[-4.008774429202085, 53.320801704764484],
        [-2.3001940460205077, 48.30407496643066],
        [-1.3720380291938783, 4.496097963809966],
        [-25.762138305664067, 541.0049044189453],
        [-4.194991661071779, 88.09482488250735],
        [-4.95, 103.95],
        [-1.5685747449398038, 2.5903610579967498], # cloud kurtosis
        [0.2081664787530899, 0.9602533329725266],  # cloud mean
        [-1.4806402913331986, 0.7627759615182876], # cloud skew
        [-0.0003270627567544702, 0.0956758858831602], # cloud variance
        [-1.1809223284721373, 2.8794445624351486],
        [7.442875038146975, 39.64330431365967],
        [-0.8497736017704011, 0.7679966728687285],
        [-2.1421645126342774, 142.2108084640503],
        [-8.051052951335908, 4.618369416713715],
        [3.2515556125640863, 220.4330385417938],
        [-1183.7761563110348, 33739.38537872314],
        [0.17007034665346174, 4.41339653724432]]

ylims = [[-0.009340051832334826, 0.19614108847903133],
        [-0.0038746795934066058, 0.08136827146153872],
        [-0.03255476872622524, 0.6836501432507299],
        [-0.0004251588892512255, 0.008928336674275734],
        [-0.008711697558134472, 0.18294564872082392],
        [-0.0016500071404219792, 0.034650149948861564],
        [-0.04467084619818229, 0.9380877701618281],
        [-0.1800003748600323, 3.7800078720606782],
        [-0.07172997253419282, 1.506329423218049],
        [-1.5266269606069613, 32.05916617274619],
        [-0.047942915892479024, 1.0068012337420595],
        [-0.005625322885153317, 0.11813178058821966],
        [-0.06412266028178852, 1.346575865917559],
        [-0.0028453945973609396, 0.059753286544579724],
        [-0.01329228074871254, 0.2791378957229633],
        [-0.0006940201285573098, 0.014574422699703507],
        [-7.787104757443538e-06, 0.00016352919990631428],
        [-0.04355847010902551, 0.9147278722895357]]
"""
xlims = [[3.2515556125640863, 220.4330385417938],
        [-1183.7761563110348, 33739.38537872314],
        [0.17007034665346174, 4.41339653724432]]
        
ylims = [[-0.0006940201285573098, 0.014574422699703507],
        [-7.787104757443538e-06, 0.00016352919990631428],
        [-0.04355847010902551, 0.9147278722895357]]
"""

# loop through each one and plot
for field, raster, xlabel, xlim, ylim, background in \
    zip(fields, rasters, xlabels, xlims, ylims, bck_data):
#for field, raster, xlabel in zip(fields, rasters, xlabels):
    
    # read the raster data
    #ref = ccb.read.raster(rpath+raster)
    #ref.read_all()
    
    # subset the background points
    #background = ref.data[gd][samples]
    
    # clear mem
    #ref.data = None
    #ref = None
    
    # set a dummy variable to handle pop density transforms
    cov_ae = np.array(ae[field])
    cov_aa = np.array(aa[field])
    
    # subset to just good data values
    cov_ae = cov_ae[cov_ae != no_data]
    cov_aa = cov_aa[cov_aa != no_data]
    background = background[background != no_data]
    
    # get general metadata on colors
    if 'LAI' in field or 'LC' in field:
        col = c_lc
        unit = units['lai']
        if 'LC' in field:
            unit = units['lc']
    elif 'CLD' in field:
        col = c_cld
    elif 'PCP' in field:
        col = c_pcp
        unit = units['pcp']
    elif 'LST' in field:
        col = c_lst
        unit = units['lst']
    elif 'POP' in field:
        col = c_pop
        unit = units['pop']
        # and log transform the extracted data
        #cov_ae = np.log(cov_ae)
        #cov_aa = np.log(cov_aa)
        
    # infinity check
    if np.isinf(cov_ae).any():
        infs = np.isinf(cov_ae)
        finite = np.invert(infs)
        cov_ae = cov_ae[finite]
        
    if np.isinf(cov_aa).any():
        infs = np.isinf(cov_aa)
        finite = np.invert(infs)
        cov_aa = cov_aa[finite]
        
    # ok! ready to begin plotting
    # set the figure size 
    plt.figure(figsize=(4,4), dpi=160)
    
    # do the deed
    aei.plot.density_dist([cov_ae, background], plot=plt, color=[c_ae, c_bck])#,
        #xlabel=xlabel)
        
    # set legend and other plot parameters
    plt.title("")
    plt.xlabel(xlabel + unit, fontsize=fs_xlabel)
    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # set ticks
    #n_ticks = 4
    #ylim = np.round(plt.ylim(), decimals=2)
    #steps = ylim[1] / n_ticks
    #rng = np.arange(ylim[0], ylim[1] + steps, steps)
    #plt.yticks(rng)
    
    # turn off y axis ticks
    ax.spines['left'].set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    # get the x and y limits to set for the next plot too
    #xlim_ae = plt.xlim()
    #ylim_ae = plt.ylim()
    #plt.xlim(xlim_ae)
    #plt.ylim(ylim_ae)
    
    # jk, use the ones calculated already
    plt.xlim(xlim)
    plt.ylim(ylim)
    
    # if we're doing pop. density, transform the x tick labels to normal numbers
    if 'POP' in field:
        xt = [0.001, 0.1, 1, 10]
        xl = np.log(xt)
        plt.xticks(xl, xt)
    
    # set x axis ticks
    #n_ticks=3
    #ticker.MaxNLocator(n_ticks, min_n_ticks=n_ticks)
    #ax.xaxis.set_major_locator(ticker)
    
    # clean up and save the dang fig
    plt.tight_layout()
    plt.savefig(plots + 'density_dist/png/aedes-aegypti-' + field + '.png', dpi=150)
    plt.savefig(plots + 'density_dist/svg/aedes-aegypti-' + field + '.svg')
    plt.close()
    
    
    # do it again for albopictus
    # set the figure size 
    plt.figure(figsize=(4,4), dpi=150)
    
    # do the deed
    aei.plot.density_dist([cov_aa, background], plot=plt, color=[c_aa, c_bck])#,
        #xlabel=xlabel)
        
    # set legend and other plot parameters
    plt.title("")
    plt.xlabel(xlabel + unit, fontsize=fs_xlabel)
    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # set ticks
    #n_ticks = 4
    #ylim = np.round(plt.ylim(), decimals=2)
    #steps = ylim[1] / n_ticks
    #rng = np.arange(ylim[0], ylim[1] + steps, steps)
    #plt.yticks(rng)
    
    # turn off y axis ticks
    ax.spines['left'].set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    # set the x and y limits to previous range
    xlim_aa = plt.xlim()
    ylim_aa = plt.ylim()
    plt.xlim(xlim_aa)
    plt.ylim(ylim_aa)
    
    # jk, use the ones calculated already
    #plt.xlim(xlim)
    #plt.ylim(ylim)
    
    # transform the x tick labels to normal numbers
    if 'POP' in field:
        xt = [0.001, 0.1, 1, 10]
        xl = np.log(xt)
        plt.xticks(xl, xt)
    
    # set x axis ticks
    #n_ticks=3
    #ticker.MaxNLocator(n_ticks, min_n_ticks=n_ticks)
    #ax.xaxis.set_major_locator(ticker)
    
    # clean up and save the dang fig
    plt.tight_layout()
    plt.savefig(plots + 'density_dist/png/aedes-albopictus-' + field + '.png', dpi=150)
    plt.savefig(plots + 'density_dist/svg/aedes-albopictus-' + field + '.svg')
    plt.close()
    
    # store the background data for further analysis
    #bck_data.append(background)
    
    # store the min/max xlim and ylim data
    #xlims.append([np.min([xlim_ae[0], xlim_aa[0]]), np.max([xlim_ae[1], xlim_aa[1]])])
    #ylims.append([np.min([ylim_ae[0], ylim_aa[0]]), np.max([ylim_ae[1], ylim_aa[1]])])
    
    #####
    # then do it again for both vectors
    plt.figure(figsize=(4,4), dpi=150)
    
    # do the deed
    aei.plot.density_dist([background, cov_ae, cov_aa], plot=plt, 
        color=[c_bck, c_ae, c_aa], fill=False, linewidth=4)

    # set legend and other plot parameters
    plt.title("")
    plt.xlabel(xlabel + unit, fontsize=fs_xlabel)
    ax = plt.axes()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # turn off y axis ticks
    ax.spines['left'].set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    
    # set the x and y limits to previous range
    xlim_aa = plt.xlim()
    ylim_aa = plt.ylim()
    plt.xlim(xlim_aa)
    plt.ylim(ylim_aa)
    
    # transform the x tick labels to normal numbers
    if 'POP' in field:
        xt = [0.001, 0.1, 1, 10]
        xl = np.log(xt)
        plt.xticks(xl, xt)
    
    # clean up and save the dang fig
    plt.tight_layout()
    plt.savefig(plots + 'density_dist/png/both-' + field + '.png', dpi=150)
    plt.savefig(plots + 'density_dist/svg/both-' + field + '.svg')
    plt.close()
  
    
# do some hacky stuff to run brunner munzel tests
# test mean temperature differences
bck = bck_data[-4]
field = 'LST_m'
cov_ae = np.array(ae[field])
cov_aa = np.array(aa[field])

# subset to just good data values
cov_ae = cov_ae[cov_ae != no_data]
cov_aa = cov_aa[cov_aa != no_data]
bck = bck[bck != no_data]

wae, pae = stats.brunnermunzel(cov_ae, bck)
waa, paa = stats.brunnermunzel(cov_aa, bck)
print('LST significance testing')
print('aedes aegypti   : p = {:0.3f}'.format(pae))
print('aedes albopictus: p = {:0.3f}'.format(paa))

# just do the rest via command line..
