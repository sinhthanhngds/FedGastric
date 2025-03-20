import zipfile 

with zipfile.ZipFile('/home/james/Projects/240801_36105_iLab/ilab-07-2/data/raw/GasHisSDB.zip', 'r') as zip_ref:
    zip_ref.extractall('/home/james/Projects/240801_36105_iLab/ilab-07-2/data/raw')