import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import NIRSPEC
import astrometry
import avg_rv


def rv_vis(path_to_rv_results_minus_df, obj_spec_type=30):
    df = pd.read_csv(path_to_rv_results_minus_df, sep='\t')

    plt.clf()

    for i, row in df.iterrows():
        spec_type = row['std_opt_spec_type']
        spec_type = spec_type.replace('M', '0').replace('L', '1').replace('T', '2')

        spec_type = spec_type.split(' ')[0]

        spec_type = float(spec_type)

    # plt.scatter(spec_type,row['obj_rv'],color='black')

    # 		plt.errorbar(spec_type, row['obj_rv'], yerr=row['obj_unc'],color='black',alpha=0.7)

    beginning_of_path = path_to_rv_results_minus_df.split('/')[6]
    obj_name = beginning_of_path.split('_')[0]
    # 	print obj_name

    rv, unc = avg_rv.avg_rv(path_to_rv_results_minus_df)

    plt.scatter(obj_spec_type, rv, marker='*', s=200, color='blue')
    plt.annotate(str(obj_name), xycoords='axes fraction', xy=(.77, .05), size=15)
    eleven = float(13)
    obj_spec_type_position = float(obj_spec_type) - 5.0
    xmax = obj_spec_type_position / eleven

    plt.xlim([5, 18])
    plt.ylim([-1.5, 6.5])
    # 	plt.axhline(y=rv, xmax=xmax, color='blue', ls='--',alpha=0.5)
    plt.fill_between(range(5, 19), rv + unc, rv - unc, interpolate=True, alpha=0.3)

    spec_type_range = [6, 8, 10, 12, 14, 16, 18]
    labels = ['M6', 'M8', 'L0', 'L2', 'L4', 'L6', 'L8']
    plt.xticks(spec_type_range, labels)

    plt.xlabel('Spectral Type')
    plt.ylabel('Calculated RV')

    plt.savefig(str(obj_name)+'_calculated_rvs.png')

    plt.show()