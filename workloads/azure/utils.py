"""Utilities for reading and processing the AzureFunctions dataset."""
import os

import pandas as pd


def read_function_invocations(path_to_dir, triggers=['http'], start=1, end=20160):
    start_file_index = (start - 1) // 1440 + 1
    end_file_index = (end - 1) // 1440 + 1

    files = []
    for i in range(start_file_index, end_file_index + 1):
        print(i)
        if i > 9:
            files.append((i, os.path.join(path_to_dir, f'invocations_per_function_md.anon.d{i}.csv')))
        else:
            files.append((i, os.path.join(path_to_dir, f'invocations_per_function_md.anon.d0{i}.csv')))

    all_invocations = None
    for i, (ind, f) in enumerate(files):
        invocs = pd.read_csv(f, engine='c')
        http_invocs = invocs[invocs['Trigger'].isin(triggers)]
        name_mapping = {f'{min}': f'{(ind - 1) * 1440 + min}' for min in range(1, 1441)}
        http_invocs = http_invocs.rename(columns=name_mapping)
        if all_invocations is not None:
            all_invocations = all_invocations.merge(http_invocs, on=['HashOwner', 'HashApp', 'HashFunction', 'Trigger'])
        else:
            all_invocations = http_invocs

    return all_invocations




