import avg_rv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

def rv_vis(path_to_rv_results_minus_df,tar_spec_type):
    df = pd.read_csv(path_to_rv_results_minus_df, sep='\t')

    plt.clf()

    ax = plt.subplot(111)

    for i, row in df.iterrows():
        spec_type = row['std_opt_spec_type']
        spec_type = spec_type.replace('M', '0').replace('L', '1').replace('T', '2')

        spec_type = spec_type.split(' ')[0]

        spec_type = float(spec_type)

        ax.scatter(spec_type,row['obj_rv'],color='black')
        ax.errorbar(spec_type, row['obj_rv'], yerr=row['obj_unc'],color='black',alpha=0.7)

    beginning_of_path = path_to_rv_results_minus_df.split('/')[6]
    obj_name = beginning_of_path.split('_')[0]
    # 	print obj_name

    calc_rv_unc = avg_rv.avg_rv(path_to_rv_results_minus_df)
    rv = calc_rv_unc[0]
    unc = calc_rv_unc[1]

    plt.annotate(str(obj_name)+' '+str(tar_spec_type), xycoords='axes fraction', xy=(.72, .05), size=15)
    # eleven = float(13)
    # obj_spec_type_position = float(obj_spec_type) - 5.0
    # xmax = obj_spec_type_position / eleven

    ax.set_xlim([5, 18])
    ax.set_ylim([-1.5, 6.5])
    # 	plt.axhline(y=rv, xmax=xmax, color='blue', ls='--',alpha=0.5)
    ax.fill_between(range(5, 19), rv + unc, rv - unc, interpolate=True, alpha=0.3, color='grey')

    spec_type_range = [6, 8, 10, 12, 14, 16, 18]
    labels = ['M6', 'M8', 'L0', 'L2', 'L4', 'L6', 'L8']
    ax.set_xticks(spec_type_range)
    ax.set_xticklabels(labels)

    y_axis_min = ax.dataLim.bounds[1]
    y_axis_max = ax.dataLim.bounds[3]

    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    y_axis_ticks=[y_axis_min, rv-unc, rv, rv+unc, y_axis_max]
    ax.set_yticks(y_axis_ticks)

    ax.set_xlabel("Spectral Type of RV Standard")
    ax.set_ylabel('Calculated RV (km/s)')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # plt.savefig(str(obj_name) + '_rv_results.png')

    plt.show()
