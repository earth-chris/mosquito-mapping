import ccb


# set the paths to the 
base = '/home/cba/src/mosquito-mapping/'
samples = base + 'vector/culicidae-nontarget-maxent.csv'
model_dir = base + 'maxent-outputs/bias_file'
env_layers = base + 'maxent-rasters'
layer = 'population-ln'
output_format = 'raw'

# create the maxent object
mx = ccb.maxent(samples=samples, env_layers=env_layers, model_dir=model_dir)
mx.set_layers(layer)
mx.set_parameters(output_format=output_format)

# fit the model
mx.fit()