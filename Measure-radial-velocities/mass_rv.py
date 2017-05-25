import NIRSPEC
import pandas as pd
import numpy as np
import astrometry


def mass_rv(obj_filename, path_to_obj_unc, obj_name, path_to_df):
    df = pd.read_csv(path_to_df, sep='\t')

    RV = []
    error = []

    for i, row in df.iterrows():
        rv_and_error = NIRSPEC.main(['', row['filename'], row['std_rv'], row['std_unc'], obj_filename, 1, row['unc_file'], path_to_obj_unc])
        RV.append(rv_and_error[0])
        error.append(rv_and_error[1])

    df['obj_rv'] = RV
    df['obj_unc'] = error

    df.to_csv(str(obj_name) + '_against_Rice2010_comps_w_uncs.txt', sep='\t')


def avg_rv(path_to_df):
    df = pd.read_csv(path_to_df, sep='\t')

    RV = []
    eRV = []

    for i, row in df.iterrows():
        RV.append(row['obj_rv'])
        eRV.append(row['obj_unc'])

    RV = np.asarray(RV)
    eRV = np.asarray(eRV)

    calc_rv_unc = astrometry.wstddev(RV, eRV)

    print("Avg RV = " + str(calc_rv_unc[0]) + " +/- " + str(calc_rv_unc[1]))

    return calc_rv_unc[0], calc_rv_unc[1]