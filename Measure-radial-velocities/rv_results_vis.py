import avg_rv
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

def rv_vis(path_to_rv_results_minus_df,tar_spec_type):
    """
    Creates a plot of spectral type of the RV standard object vs the calculated RV for a single object using that given standard.

    Argument: path to the tab separated pandas dataframe saved as a csv file and the spectral type of the object whose RV you're measuring

    Return: saves the file as a png
    """

    # Reads in the given database
    df = pd.read_csv(path_to_rv_results_minus_df, sep='\t')

    plt.clf()

    # Creates the axes for the plot
    ax = plt.subplot(111)

    # Loops through the rows of the dataframe, plotting the calculated RV using each of the standards
    for i, row in df.iterrows():

        # Turns the spectral type of the standard into an number (ex M7 -> 07, L4 -> 15)
        spec_type = row['std_opt_spec_type']
        spec_type = spec_type.replace('M', '0').replace('L', '1').replace('T', '2')

        # Takes any gravity suffix off of the spectral type
        spec_type = spec_type.split(' ')[0]

        # Turns the spectral type into a float
        spec_type = float(spec_type)

        # Plots the calculated RV as a point with errorbars
        ax.scatter(spec_type,row['obj_rv'],color='black')
        ax.errorbar(spec_type, row['obj_rv'], yerr=row['obj_unc'],color='black',alpha=0.7)

    # Finds the object name using the path to the dataframe (will have to be changed for different file structures
    beginning_of_path = path_to_rv_results_minus_df.split('/')[6]
    obj_name = beginning_of_path.split('_')[0]
    # 	print obj_name

    # Calculated the weighted average radial velocity and uncertainty, which is used to plot the grey bar of uncertainty on the final RV calculation
    calc_rv_unc = avg_rv.avg_rv(path_to_rv_results_minus_df)
    rv = calc_rv_unc[0]
    unc = calc_rv_unc[1]

    # Prints the name of the object and the object's spectral type on the plot
    plt.annotate(str(obj_name)+' '+str(tar_spec_type), xycoords='axes fraction', xy=(.72, .05), size=15)

    # Sets the x limits
    ax.set_xlim([5, 18])

    # Creates the grey bar of uncertainty on the final averaged RV measurement
    ax.fill_between(range(5, 19), rv + unc, rv - unc, interpolate=True, alpha=0.3, color='grey')

    # Sets the x labels to be the spectral type between M6 and L8
    spec_type_range = [6, 8, 10, 12, 14, 16, 18]
    labels = ['M6', 'M8', 'L0', 'L2', 'L4', 'L6', 'L8']
    ax.set_xticks(spec_type_range)
    ax.set_xticklabels(labels)

    # Assigns highest and lowest y-value to y_axis_max and y_axis_min variables
    y_axis_min = ax.get_ylim()[0]
    y_axis_max = ax.get_ylim()[1]

    # Sets the y-axis ticks to the lowest y-value, highest y-value, the average RV and the limits of the final averaged RV uncertainty
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    y_axis_ticks=[y_axis_min, rv-unc, rv, rv+unc, y_axis_max]
    ax.set_yticks(y_axis_ticks)

    # Sets x and y labels
    ax.set_xlabel("Spectral Type of RV Standard")
    ax.set_ylabel('Calculated RV (km/s)')

    # Gets rid of the top and right hand borders
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Saves the plot
    plt.savefig(str(obj_name) + '_rv_results.png')

    plt.show()
