import aei
import ccb
import glob
import numpy as np
import geopandas as gpd
import matplotlib as mpl
from matplotlib import ticker
from matplotlib import pyplot as plt

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
plots = base + 'plots/'
rpath = base + 'raster/001000-m/'
bias_file = base + '/maxent-outputs/bias-file-001000-m/Culicidae.asc'
ae_file = base + 'vector/aegypti-54009-3.shp'
aa_file = base + 'vector/albopictus-54009-3.shp'

# set the font size
mpl.rcParams.update({'font.size': 20})
fs_xlabel = 25

# set the colors
c_cld = "#56B4E9" 
c_lst = "#E69F00"
c_lc = "#009E73" 
c_pop = "#CC79A7"
c_bck = "#424243"

# set vector-specific colors
c_ae = '#CC79A7'
c_aa = '#E69F00'

# set the number of points
n_pts = 10000

# set the seed for consistent random sampling
np.random.seed(1985)

# read the bias file into memory
no_data = -9999
bias_ref = ccb.read.raster(bias_file)
bias_ref.read_all()
gd = bias_ref.data != no_data
bias = bias_ref.data[gd]

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

# set the corresponding vector fields with the raster data to read
fields = ['LAI_k', 'LAI_m', 'LAI_s', 'LAI_v', 'LC-bare', 'LC-trees',
          'CLD_k', 'CLD_m', 'CLD_s', 'CLD_v', 'LST_k',
          'LST_m', 'LST_s', 'LST_v', 'POP']

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
           'Population-ln-nd.asc']
           
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
           'population density\n(ln)']
           
# loop through each one and plot
for field, raster, xlabel in zip(fields, rasters, xlabels):
    
    # read the raster data
    ref = ccb.read.raster(rpath+raster)
    ref.read_all()
    
    # subset the background points
    background = ref.data[gd][samples]
    
    # clear mem
    ref.data = None
    ref = None
    
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
    elif 'CLD' in field:
        col = c_cld
    elif 'LST' in field:
        col = c_lst
    elif 'POP' in field:
        col = c_pop
        # and log transform the extracted data
        cov_ae = np.log(cov_ae)
        cov_aa = np.log(cov_aa)
        
    # infinity check
    if np.isinf(cov_ae).any():
        infs = np.isinf(cov_ae)
        finite = np.invert(infs)
        cov_ae = cov_ae[finite]
        
    # ok! ready to begin plotting
    # set the figure size 
    plt.figure(figsize=(4,4), dpi=160)
    
    # do the deed
    aei.plot.density_dist([cov_ae, background], plot=plt, color=[c_ae, c_bck])#,
        #xlabel=xlabel)
        
    # set legend and other plot parameters
    plt.title("")
    plt.xlabel(xlabel, fontsize=fs_xlabel)
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
    
    # set x axis ticks
    #n_ticks=3
    #ticker.MaxNLocator(n_ticks, min_n_ticks=n_ticks)
    #ax.xaxis.set_major_locator(ticker)
    
    # clean up and save the dang fig
    plt.tight_layout()
    plt.savefig(plots + 'density_dist/aedes-aegypti-' + field + '.png', dpi=150)
    plt.close()
    
    
    # do it again for albopictus
    # set the figure size 
    plt.figure(figsize=(4,4), dpi=150)
    
    # do the deed
    aei.plot.density_dist([cov_aa, background], plot=plt, color=[c_aa, c_bck])#,
        #xlabel=xlabel)
        
    # set legend and other plot parameters
    plt.title("")
    plt.xlabel(xlabel, fontsize=fs_xlabel)
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
    
    # set x axis ticks
    #n_ticks=3
    #ticker.MaxNLocator(n_ticks, min_n_ticks=n_ticks)
    #ax.xaxis.set_major_locator(ticker)
    
    # clean up and save the dang fig
    plt.tight_layout()
    plt.savefig(plots + 'density_dist/aedes-albopictus-' + field + '.png', dpi=150)
    plt.close()