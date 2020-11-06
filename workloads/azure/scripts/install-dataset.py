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

tar_path = os.path.join(os.getcwd(), TAR_FILENAME)
dir_name = TAR_FILENAME.split(".")[0]

# Download file
resp = requests.get(URL, allow_redirects=True, stream=True)

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
duration_files = []
invocation_files = []
for entry in os.scandir(dataset_dir):
    if "app" in entry.path:
        memory_files.append(entry.path)
    elif "function_durations" in entry.path:
        duration_files.append(entry.path)
    elif "invocations_per" in entry.path:
        invocation_files.append(entry.path)
    else:
        print(f"Unknown file: {entry.path}")

# Do some sorting
duration_files = sorted(duration_files)
invocation_files = sorted(invocation_files)
memory_files = sorted(memory_files)

# Join the memory files
cumm_memory = None
for (i, entry) in enumerate(memory_files):
   csv = pd.read_csv(entry)
   csv['Day'] = i + 1
   if cumm_memory is not None:
       cumm_memory = pd.concat([cumm_memory, csv], ignore_index=True)
   else:
       cumm_memory = csv
   os.remove(entry)
new_path = os.path.join(dataset_dir, 'memory.csv')
cumm_memory.to_csv(new_path, index=False)

# Join all invocations
cumm_invocations = None
for (i, entry) in enumerate(invocation_files):
    name_mapping = {f'{min}':f'{i * 1440 + min}' for min in range(1, 1441)}
    csv = pd.read_csv(entry)
    csv = csv.rename(columns=name_mapping)
    if cumm_invocations is not None:
        cumm_invocations = cumm_invocations.merge(csv, on=['HashOwner', 'HashApp', 'HashFunction', 'Trigger'])
    else:
        cumm_invocations = csv
    os.remove(entry)
new_path = os.path.join(dataset_dir, 'invocations.csv')
cumm_invocations.to_csv(new_path, index=False)

# Join the function files
cumm_durations = None
for (i, entry) in enumerate(duration_files):
   csv = pd.read_csv(entry)
   csv['Day'] = i + 1
   if cumm_durations is not None:
       cumm_durations = pd.concat([cumm_durations, csv], ignore_index=True)
   else:
       cumm_durations = csv
   os.remove(entry)
new_path = os.path.join(dataset_dir, 'durations.csv')
cumm_durations.to_csv(new_path, index=False)



