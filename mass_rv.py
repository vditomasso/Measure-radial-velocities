import NIRSPEC
import pandas as pd
import numpy as np


def mass_rv(obj_filename, obj_name, path_to_df):
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    errors = []

    for i, row in df.iterrows():
        rv, error = NIRSPEC.main(['', row['filename'], row['std_rv'], row['std_unc'], obj_filename, 1])
        rvs.append(rv)
        errors.append(error)

    df['obj_rv'] = rvs
    df['obj_unc'] = errors

    df.to_csv(str(obj_name) + '_against_all_comps.txt', sep='\t')

def mass_rv_outliers(obj_filename, obj_name, path_to_df):
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    errors = []

    for i, row in df.iterrows():
        rv, error = NIRSPEC.main(
            ['', row['filename'], row['std_rv'], row['std_unc'], obj_filename, 0, 200, row['lower_pixel_shift'],
             row['upper_pixel_shift']])
        rvs.append(rv)
        errors.append(error)

    df['obj_rv'] = rvs
    df['obj_unc'] = errors

    df.to_csv(str(obj_name) + '_against_all_outliers.txt', sep='\t')