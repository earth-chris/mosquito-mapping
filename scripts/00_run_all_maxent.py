import ccb
import numpy as np
import pickle


# set the paths to the input files
base = '/home/salo/src/mosquito-mapping/'
samples_dir = base + 'maxent-inputs/'
layers = base + 'raster/'
bias = base + 'maxent-outputs/'
outdir = base + 'maxent-outputs/'
output_format = 'cumulative'
features = ['hinge'] #['auto']
beta_multiplier = 1.5
n_folds = 4

# set the species to assess
spl = ['Aedes aegypti', 'Aedes albopictus']
sp = ['aedes-aegypti', 'aedes-albopictus']

# set the resolutions to assess
res = [1000, 5000, 10000, 50000, 100000]

# set the sample geography data
#geo = ['all', 'cam', 'car', 'sam']
geo = ['all']

# set the environmental subsets
#env = ['clim', 'lcov', 'envs']
#climlist = ['temp-max', 'temp-med', 'temp-min']
#lcovlist = ['vegetation', 'trees', 'impervious', 'soil']
#envslist = climlist + lcovlist

env = ['cld', 'lst', 'luc', 'pop', 'all']

luclist = [
    #'LC-Bare',
    'LC-Trees',
    'LAI-mean',
    'LAI-variance'
]    

cldlist = [
    #'CLD-kurtosis',
    'CLD-mean',
    'CLD-skew',
    'CLD-variance'
]

lstlist = [
    #'LST-kurtosis',
    'LST-mean',
    'LST-skew',
    'LST-variance'
]

poplist = ['Population-ln-nd']

lucpoplist = luclist + poplist
lstpoplist = lstlist + poplist
all = cldlist + lstlist + luclist + poplist

envslist = [cldlist, lstlist, luclist, poplist, all]

# set the maxent run options
test_pct = 25
nodata = -9999

# create an array to store auc and f-score values
auc_ae_mn = np.zeros((n_folds, len(env), len(geo), len(res)))
auc_aa_mn = np.zeros((n_folds, len(env), len(geo), len(res)))
auc_mn_lst = [auc_ae_mn, auc_aa_mn]

fsc_ae_mn = np.zeros((n_folds, len(env), len(geo), len(res)))
fsc_aa_mn = np.zeros((n_folds, len(env), len(geo), len(res)))
fsc_mn_lst = [fsc_ae_mn, fsc_aa_mn]

# report starting!
ccb.prnt.status('starting maxent runs!')

# then set up a big ol' loop structure to run through all the different maxent permutations
for s in range(len(sp)):
    for r in range(len(res)-1, -1, -1):
        for g in range(len(geo)):
            for e in range(len(env)):
                for f in range(n_folds):
                    
                    # create a fresh maxent object
                    mx = ccb.maxent()
                    
                    # set the output directory
                    model_dir = '{outdir}{env}-{res:06d}-{geo}-{fold}'.format(
                        outdir=outdir, env=env[e], res=res[r], geo=geo[g], fold=f+1)
                        
                    # set the input sample path
                    samples = '{samples}{sp}-{geo}-training-{fold}.csv'.format(
                        samples=samples_dir, sp=sp[s], geo=geo[g], fold=f+1)
                        
                    # set the environmental layers directory
                    env_layers = '{layers}{res:06d}-m/'.format(
                        layers=layers, res=res[r])
                        
                    # and the layers to use
                    #if env[e] == 'clim':
                    #    layer_list = climlist
                    #elif env[e] == 'lcov':
                    #    layer_list = lcovlist
                    #else:
                    #    layer_list = envslist
                        
                    #if env[e] == 'lai':
                    #    layer_list = lailist
                    #elif env[e] == 'cld':
                    #    layer_list = cldlist
                    #elif env[e] == 'lst':
                    #    layer_list = lstlist
                    #elif env[e] == 'pop':
                    #    layer_list = poplist
                    #else:
                    #    layer_list = envslist
                        
                    layer_list = envslist[e]
                        
                    # set the bias file path
                    bias_file = '{bias}bias-file-{res:06d}-m/Culicidae.asc'.format(
                        bias=bias, res=res[r])
                        
                    # set a flag to output the maps when using all variables
                    if env[e] == 'all':
                        write_grids = True
                    #if res[r] == 1000:
                    #    write_grids = True
                    else:
                        write_grids = False
                        
                    # set the parameters in the maxent object
                    mx.set_parameters(model_dir=model_dir, samples=samples, env_layers=env_layers,
                        bias_file=bias_file, write_grids=write_grids, nodata=nodata,
                        output_format=output_format, features=features, verbose=False,
                        skip_if_exists=False, beta_multiplier=beta_multiplier)
                        
                    # set the layers
                    mx.set_layers(layer_list)
                    
                    # and set the test data based on the extent
                    if geo[g] == 'all':
                        #mx.set_parameters(pct_test_points=test_pct)
                        test_samples = '{samples}{sp}-{geo}-testing-{fold}.csv'.format(
                            samples=samples_dir, sp=sp[s], geo=geo[g], fold=f+1)
                        mx.set_parameters(test_samples=test_samples)
                    else:
                        test_samples = '{samples}{sp}-{geo}-testing.csv'.format(
                            samples=samples_dir, sp=sp[s], geo=geo[g])
                        mx.set_parameters(test_samples=test_samples)
                        
                    # print out the command to run
                    ccb.prnt.status(mx.build_cmd())
                    mx.fit()
                    
                    # pull the output auc values
                    try:
                        # get the predictions
                        ytrue, ypred = mx.get_predictions(spl[s], test=True,
                            prediction_type='cumulative')
                        
                        # get the number of test data
                        test_ind = ytrue == 1
                        n_test = test_ind.sum()
                        test_true = ytrue[test_ind]
                        test_pred = ypred[test_ind]
                        
                        # get the indices of the background points to subset
                        ind_bck = ytrue == 0
                        n_bck = ind_bck.sum()
                        back_true = ytrue[ind_bck]
                        back_pred = ypred[ind_bck]
                        
                        # loop through some number of times, randomly sample the background,
                        #  and calculate auc scores
                        n_rndm = 5
                        auc = np.zeros(n_rndm)
                        fsc = np.zeros(n_rndm)
                        for i in range(n_rndm):
                            # get random indices
                            rndm = np.random.randint(0, n_bck, n_test)
                            
                            # stick the test/background data together
                            auc_true = np.append(test_true, back_true[rndm])
                            auc_pred = np.append(test_pred, back_pred[rndm])
                            auc[i] = ccb.metrics.roc_auc(auc_true, auc_pred)
                            fsc[i] = ccb.metrics.f1_score(auc_true/100., auc_pred/100.)
                        
                        # then add this value to the array
                        auc_mn_lst[s][f,e,g,r] = auc.mean()
                        fsc_mn_lst[s][f,e,g,r] = fsc.mean()
                    except:
                        pass
                
# export the results to a picle file
pck_ae = base + 'scripts/ae-auc.pck'
pck_aa = base + 'scripts/aa-auc.pck'
pck_aef = base + 'scripts/ae-fsc.pck'
pck_aaf = base + 'scripts/aa-fsc.pck'

with open(pck_ae, 'wb') as f:
    pickle.dump(auc_ae_mn, f)
    
with open(pck_aa, 'wb') as f:
    pickle.dump(auc_aa_mn, f)
    
with open(pck_aef, 'wb') as f:
    pickle.dump(fsc_ae_mn, f)
    
with open(pck_aaf, 'wb') as f:
    pickle.dump(fsc_aa_mn, f)
    

# and run two final models with all data included
for s in range(len(sp)):
    # create a fresh maxent object
    mx = ccb.maxent()
    
    # set the output directory
    model_dir = '{outdir}{env}-{res:06d}-{geo}'.format(
        outdir=outdir, env='all', res=res[0], geo='all')
        
    # set the input sample path
    samples = '{samples}{sp}-resampled.csv'.format(
        samples=samples_dir, sp=sp[s])
        
    # set the environmental layers directory
    env_layers = '{layers}{res:06d}-m/'.format(
        layers=layers, res=res[0])
        
    layer_list = all
        
    # set the bias file path
    bias_file = '{bias}bias-file-{res:06d}-m/Culicidae.asc'.format(
        bias=bias, res=res[0])
        
    # output the maps
    write_grids = True
    
    # set the cross validation
    replicate_type = 'crossvalidate'
        
    # set the parameters in the maxent object
    mx.set_parameters(model_dir=model_dir, samples=samples, env_layers=env_layers,
        bias_file=bias_file, write_grids=write_grids, nodata=nodata,
        output_format=output_format, features=features, verbose=False,
        skip_if_exists=False, beta_multiplier=beta_multiplier,
        n_replicates=n_folds, replicate_type=replicate_type)
        
    # set the layers
    mx.set_layers(layer_list)
        
    # print out the command to run
    ccb.prnt.status(mx.build_cmd())
    mx.fit()
    