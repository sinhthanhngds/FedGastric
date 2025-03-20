import os 
import numpy as np
import shutil 

## Check if the folders are created - if not create them for each clinic
## Save the data for each clinic in test and train folders 

# Path to folder where you want the data stored 
root = os.path.realpath('..')
proc = os.path.join(root, 'data', 'processed')
# sub folders in each clinic folder 
fols = ['train', 'test', 'validate']
classes = ['Abnormal', 'Normal']
## Create clinic folders and train/test/validate with normal and abnormal
## folders 
for clin in range(4):
    direct = os.path.join(proc, 'clin_'+str(clin)) 
    if os.path.exists(direct) == False:
        os.mkdir(direct)
        for folder in fols:
            sub = os.path.join(direct, folder)
            os.mkdir(sub)
            for abnor in classes:
                subdir = os.path.join(direct,folder, abnor)
                os.mkdir(subdir)
    else:
        ## this will remove any directories that were there and all the contents
        ## for standard folders and file structures 
        shutil.rmtree(direct)
        os.mkdir(direct)
        for folder in fols:
            sub = os.path.join(direct, folder)
            os.mkdir(sub)
            for abnor in classes:
                subdir = os.path.join(direct,folder, abnor)
                os.mkdir(subdir)


## Cycles through the file structure from the downloaded zip file and 
## splits the data into four clinics. In the clinic environments there 
## is a train, validate and test set of data created. 
## All three image sizes are used and randomly separated across all four clinic locations.
## Seed is set to provide a level of certainty that the data will be the same across different implementations

classes = ['Abnormal', 'Normal']
img_sizes = ['80', '120', '160']
root = os.path.realpath('../data')

for size in img_sizes:
    ## cycle through the different image sizes 
    for clas in classes:
        src = os.path.join(root,'raw', 'GasHisSDB', size, clas) ## Create path for source folders 
        print(src) # check paths for folders 

        ## Get a list of all the filies in the folders 
        allfiles = os.listdir(src)
        ## shuffle the files 
        np.random.seed(13)
        np.random.shuffle(allfiles)

        ## Create the split 70/25/5 

        train_files, val_files, test_files = np.split(np.array(allfiles), [int(len(allfiles)*.7), int(len(allfiles)*.95)])
        print(len(train_files))
        print(len(val_files))
        print(len(test_files))
        train_array = np.array_split(train_files, 4)
        val_array = np.array_split(val_files, 4)
        test_array = np.array_split(test_files, 4)

        for clin in range(4):
            train_names = [src+ '/' + name for name in train_array[clin]]
            val_names = [src +'/' + name for name in val_array[clin]]
            test_names = [src +'/' + name for name in test_array[clin]]
            
            for idx, name in enumerate(train_names):
                shutil.copyfile(name, root + '/processed/' + 'clin_' +str(clin) + '/train/' + clas + '/' + size + '-' + train_array[clin][idx])

            for idx1, name in enumerate(val_names):
                shutil.copyfile(name, root + '/processed/' + 'clin_' +str(clin) + '/validate/' + clas + '/' + size + '-' + val_array[clin][idx1])
            
            for idx2, name in enumerate(test_names):
                shutil.copyfile(name, root + '/processed/' + 'clin_' +str(clin) + '/test/' + clas + '/' + size + '-' + test_array[clin][idx2])