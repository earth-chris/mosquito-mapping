import ccb


# set the paths to the input files
base = '/home/salo/src/mosquito-mapping/'
samples = base + 'maxent-inputs/culicidae-nontarget.csv'
out_dir = base + 'maxent-outputs/bias-file'
layers_dir = base + 'raster/'
#layer = 'population-ln'
#output_format = 'logistic'
output_format = 'cumulative'

layers = [
    'LAI-kurtosis',
    'LAI-mean',
    'LAI-skew',
    'LAI-variance',
    'CLD-kurtosis',
    'CLD-mean',
    'CLD-skew',
    'CLD-variance',
    'LST-kurtosis',
    'LST-mean',
    'LST-skew',
    'LST-variance'
]

# set the output resolutions
res = [1000, 5000, 10000, 50000, 100000]
#res = [100000]

# create the maxent object
for i in range(len(res)):
    env_layers = '{dir}{r:06d}-m/'.format(dir=layers_dir, r=res[i])
    model_dir = '{dir}-{r:06d}-m/'.format(dir=out_dir, r=res[i])
    mx = ccb.maxent(samples=samples, env_layers=env_layers, model_dir=model_dir)
    mx.set_layers(layers)
    mx.set_parameters(output_format=output_format, write_grids=True)
    
    # fit the model
    mx.fit()