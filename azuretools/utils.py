"""Utilities for reading and processing the AzureFunctions dataset."""
import os

import pandas as pd

# Pulls Azure Function data at the granularity of days
def read_function_invocations(path_to_dir, triggers=['http', 'timer', 'event', 'queue', 'storage', 'orchestration', 'other'], start=1, end=20160):
    start_file_index = (start - 1) // 1440 + 1
    end_file_index = (end - 1) // 1440 + 1

    files = []
    for i in range(start_file_index, end_file_index + 1):
        if i > 9:
            files.append((i, os.path.join(path_to_dir, f'invocations_per_function_md.anon.d{i}.csv')))
        else:
            files.append((i, os.path.join(path_to_dir, f'invocations_per_function_md.anon.d0{i}.csv')))

    all_invocations = None
    for i, (ind, f) in enumerate(files):
        invocs = pd.read_csv(f, engine='c')
        invocs = invocs[invocs['Trigger'].isin(triggers)]
        name_mapping = {f'{min}': f'{(ind - 1) * 1440 + min}' for min in range(1, 1441)}
        renamed_invocs = invocs.rename(columns=name_mapping)
        if all_invocations is not None:
            all_invocations = all_invocations.merge(renamed_invocs, on=['HashOwner', 'HashApp', 'HashFunction', 'Trigger'])
        else:
            all_invocations = renamed_invocs

    return all_invocations




