import ccb
import pandas as pd
from sklearn import model_selection


# set paths
base = '/home/salo/src/mosquito-mapping/maxent-inputs/'
vecs = ['aedes-aegypti', 'aedes-albopictus']
exts = ['cam', 'car', 'sam']


# set up the k-fold cross validation parameters
n_splits = 4
shuffle = True # shuffles the order of the input data
random_state = 1985 # the seed
kf = model_selection.KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)

# split the global data first
for vec in vecs:
    # read the input data
    #pts = pd.read_csv(base + vec + '-all.csv')
    pts = pd.read_csv(base + vec + '-resampled.csv')
    
    # set the counter for writing train/test subsets
    i = 1
    
    # loop through the kfolds, split the data, and write to output files
    for train_index, test_index in kf.split(pts):
        train_pts = pts.iloc[train_index]
        test_pts = pts.iloc[test_index]
        
        # write these to output files
        train_file = base + vec + '-all-training-{}.csv'.format(i)
        test_file = base + vec + '-all-testing-{}.csv'.format(i)
        
        train_pts.to_csv(train_file, index=False)
        test_pts.to_csv(test_file, index=False)
        
        # and update the counter
        i += 1
        

# then do this for each region
for vec in vecs:
    for ext in exts:
        # read the input data
        pts = pd.read_csv(base + vec + '-' + ext + '-training.csv')
        
        # set the counter
        i = 1
        
        # loop through the k-folds
        for train_index, test_index in kf.split(pts):
            train_pts = pts.iloc[train_index]
            test_pts = pts.iloc[test_index]
            
            # write these to output files
            train_file = base + vec + '-{}-training-{}.csv'.format(ext, i)
            test_file = base + vec + '-{}-testing-{}.csv'.format(ext, i)
            
            train_pts.to_csv(train_file, index=False)
            test_pts.to_csv(test_file, index=False)
            
            # and update the counter
            i += 1