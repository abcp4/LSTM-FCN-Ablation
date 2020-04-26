"""
Parallel processing of the dataset archive obtained from UCR.


Usage:
1) Place inside the directory extracted from the zip-archive.
   Must be inside the directory, but outside any of the subfolders.

2) Run using `python extract_all_datasets.py`. Will require Joblib >= 0.12.

3) Once extracted, a new folder called `_data` will be created with a
   large number of extracted datasets in a flattened hierarchy.

4) Rename this folder as `data` and place it at the root of the LSTM-FCN directory.

"""
import os
import glob
import numpy as np
import pandas as pd
import shutil
from joblib import Parallel, delayed

path = '_data'

if not os.path.exists(path):
    os.makedirs(path)


def process_file(fn):
    file_name = os.path.split(fn)[-1]
    file_name = file_name[:-4]
    new_path = os.path.join(path, file_name)

    # Load the Tab seperated values in the dataset
    df = pd.read_table(fn, header=None, encoding='latin-1')

    # Fill the empty timesteps with 0.0
    df.fillna(0.0, inplace=True)

    # Save the prepared dataset as a CSV file that the dataset reader can use
    df.to_csv(new_path, sep=',', index=False, header=None, encoding='latin-1')

    # shutil.copy(fn, new_path)
    print("Copied file from %s to %s" % (fn, new_path))


with Parallel(n_jobs=-1, backend='loky', verbose=1) as engine:
    engine([delayed(process_file)(fn) for fn in glob.glob("/content/LSTM-FCN-Ablation/utils/UCRArchive_2018/*/*.tsv")])


print()
print("Extracted all files. Transfer all these files to the `data` directory")
