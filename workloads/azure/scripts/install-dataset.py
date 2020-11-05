#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A script for downloading the AzureFunctionsDataset2019 into the current directory
"""

import os
import pandas as pd
import requests
import tarfile 

TAR_FILENAME = "azurefunctions-dataset2019.tar.xz"
URL = f"https://azurecloudpublicdataset2.blob.core.windows.net/azurepublicdatasetv2/azurefunctions_dataset2019/{TAR_FILENAME}"

# Download file
resp = requests.get(URL, allow_redirects=True, stream=True)

tar_path = os.path.join(os.getcwd(), TAR_FILENAME)
dir_name = TAR_FILENAME.split(".")[0]

with open(tar_path, 'wb') as tf:
    tf.write(resp.content)

# Extract tar
tar = tarfile.open(tar_path)
tar.extractall(dir_name)

# Delete tar
os.remove(tar_path)

# Join and rename files in dataset
dataset_dir = os.path.join(os.getcwd(), dir_name)
memory_files = []
function_duration_files = []
function_invocation_files = []
for entry in os.scandir(dataset_dir):
    if "app" in entry.path:
        memory_files.append(entry.path)
    elif "durations" in entry.path:
        function_duration_files.append(entry.path)
    elif "invocations" in entry.path:
        function_invocation_files.append(entry.path)
    else:
        print(f"Unknown file: {entry.path}")

# Do some sorting
function_files = zip(sorted(function_duration_files), sorted(function_invocation_files))
memory_files = sorted(memory_files)


# Rename memory files
for (i, entry) in enumerate(memory_files):
     new_path = os.path.join(dataset_dir, f"memory.d{i+1}.csv")
     os.rename(entry, new_path)

# Join the function files
for (i, (dur, inv)) in enumerate(function_files):
   dur_csv = pd.read_csv(dur)
   inv_csv = pd.read_csv(inv)
   merged = dur_csv.merge(inv_csv, on=['HashOwner', 'HashApp', 'HashFunction'])
   new_path = os.path.join(dataset_dir, f"functions.d{i+1}.csv")
   merged.to_csv(new_path, index=False)
   
   # Remove old data
   os.remove(dur)
   os.remove(inv)

