import aei
import
import numpy as np
import geopandas as gpd
import matplotlib as mpl
from matplotlib import ticker
from matplotlib import pyplot as plt

# set the base files to use
base = '/home/salo/src/mosquito-mapping/'
plot_path = base + 'plots/'
plot_probabilities = base + 'vector/sites-extracted-probabilities.shp'

# set the font size
mpl.rcParams.update({'font.size': 18})
fs_xlabel = 20

# set vector-specific colors
c_ae = '#CC79A7'
c_aa = '#E69F00'
c_bck = '#424243'

# set plot size info
figsize = (6, 6)
dpi = 150

# set the data labels
data_labels = ['absence sites', 'presence sites']
xlabel = 'predicted occurrence\nprobability (cumulative)'

#####
# read the plot data into memory
plots = gpd.read_file(plot_probabilities)

# get the index for true positive / true negative values
tp = plots['aedes'] > 0
tn = np.invert(tp)

# subset to each extent
pe = plots['country'] == 'PE'
cr = plots['country'] == 'CR'

# set the label for each vector's column
ae = 'aegypti_s'
aa = 'albo_s'


#####
## set up some calculations

# first, aegypti
tn_ae = plots[tn & pe][ae]
tp_ae = plots[tp & pe][ae]
n_tn = len(tn_ae)
n_tp = len(tp_ae)

# set up binary/probabilities arrays
bin = np.zeros((n_tn + n_tp))
prb = np.zeros((n_tn + n_tp))
bin[n_tn:] = 1
prb[0:n_tn] = tn_ae / 100
prb[n_tn:] = tp_ae / 100

# and calculate the metrics
ae_auc = ccb.metrics.roc_auc(bin, prb)
ae_pre = ccb.metrics.precision(bin, prb)
ae_rec = ccb.metrics.recall(bin, prb)
ae_spe = ccb.metrics.specificity(bin, prb)

# next, albopictus
tn_aa = plots[tn & cr][aa]
tp_aa = plots[tp & cr][aa]
n_tn = len(tn_aa)
n_tp = len(tp_aa)

# set up binary/probabilities arrays
bin = np.zeros((n_tn + n_tp))
prb = np.zeros((n_tn + n_tp))
bin[n_tn:] = 1
prb[0:n_tn] = tn_aa / 100
prb[n_tn:] = tp_aa / 100

# and calculate the metrics
aa_auc = ccb.metrics.roc_auc(bin, prb)
aa_pre = ccb.metrics.precision(bin, prb)
aa_rec = ccb.metrics.recall(bin, prb)
aa_spe = ccb.metrics.specificity(bin, prb)



#####
# plot the distributions for probabilities in true positives / negatives

# first, aegypti
plt.figure(figsize=figsize, dpi=dpi)

# base density distribution
plot_data = [tn_ae, tp_ae]
aei.plot.density_dist(plot_data, color=[c_bck, c_ae], plot=plt,
    label=data_labels)
    
# label the plots
plt.xlabel(xlabel)
plt.ylabel('frequency')
plt.title('Model predictions in field sites\n$\it{Aedes\ aegypti}$')
plt.tight_layout()

# save it
plt.savefig(plot_path + 'field-comparison-aegypti.png', dpi=200)
plt.close()


# again, for albopictus
plt.figure(figsize=figsize, dpi=dpi)

# base density distribution
plot_data = [tn_aa, tp_aa]
aei.plot.density_dist(plot_data, color=[c_bck, c_aa], plot=plt,
    label=data_labels)
    
# label the plots
plt.xlabel(xlabel)
plt.ylabel('frequency')
plt.title('Model predictions in field sites\n$\it{Aedes\ albopictus}$')
plt.tight_layout()

# save it
plt.savefig(plot_path + 'field-comparison-albopictus.png', dpi=200)
plt.close()