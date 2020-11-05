#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A script for downloading the AzureFunctionsDataset2019 into the current directory
"""

import os
import tarfile 
import requests

TAR_FILENAME = "azurefunctions-dataset2019.tar.xz"
URL = f"https://azurecloudpublicdataset2.blob.core.windows.net/azurepublicdatasetv2/azurefunctions_dataset2019/{TAR_FILENAME}"

# Download file
resp = requests.get(URL, allow_redirects=True, stream=True)

tar_path = os.path.join(os.getcwd(), TAR_FILENAME)
file_name = TAR_FILENAME.split(".")[0]

with open(tar_path, 'wb') as tf:
    tf.write(resp.content)

# Extract tar
tar = tarfile.open(tar_path)
tar.extractall(file_name)

# Delete tar
os.remove(tar_path)
