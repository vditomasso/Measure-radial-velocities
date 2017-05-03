import pandas as pd
import numpy as np
import weighted_stddev


def avg_rv(path_to_df):
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    uncs = []

    for i, row in df.iterrows():
        rvs.append(row['obj_rv'])
        uncs.append(row['obj_unc'])

    rvs = np.asarray(rvs)
    uncs = np.asarray(uncs)

    rv,unc = weighted_stddev.wstddev(rvs, uncs)

    return rv,unc

    # print("Avg RV = " + str(rv) + " +/- " + str(unc))
