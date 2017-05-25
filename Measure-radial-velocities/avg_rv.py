import pandas as pd
import numpy as np
import weighted_stddev


def avg_rv(path_to_df):
    """
    Calculates a weighted average and uncertainty of the radial velocities in a given dataframe

    Argument: path to pandas dataframe with columns 'obj_rv' and 'obj_unc'

    Returns: rv, unc
    """

    # Reads in given dataframe
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    uncs = []

    # Creates a list of the rvs and uncs from the dataframe
    for i, row in df.iterrows():
        rvs.append(row['obj_rv'])
        uncs.append(row['obj_unc'])

    # Turns the rv and unc lists into arrays
    rvs = np.asarray(rvs)
    uncs = np.asarray(uncs)

    # Calculates the weighted average with uncertainty
    rv_wtavg,unc_wtavg = weighted_stddev.wstddev(rvs, uncs)

    return rv_wtavg,unc_wtavg

    # print("Avg RV = " + str(rv) + " +/- " + str(unc))
