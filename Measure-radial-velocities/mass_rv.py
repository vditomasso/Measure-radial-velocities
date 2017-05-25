import pandas as pd
import NIRSPEC


def mass_rv(obj_filename, obj_name, path_to_df):
    """Runs NIRSPEC.main to calculate the radial velocity of one object using a number of standards.

    Argument: filename of the object's spectum (wavelength and flux), name of the object (as a string), path to a tab separated panda dataframe saved as a csv file (with 'filename', 'std_rv', 'std_unc' columns)

    Returns: a pandas dataframe saved as a tab separated csv file which is the original dataframe with additional 'obj_rv' and 'obj_unc columns"""

    # Reads in the given dataframe
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    errors = []

    # Runs NIRSPEC.main for each standards listed in the DF
    for i, row in df.iterrows():
        rv, error = NIRSPEC.main(['', row['filename'], row['std_rv'], row['std_unc'], obj_filename, 1])
        rvs.append(rv)
        errors.append(error)

    # Creates new columns for the calculated rvs and errors
    df['obj_rv'] = rvs
    df['obj_unc'] = errors

    # Saves the new dataframe (with additional obj_rv and obj_unc columns
    df.to_csv(str(obj_name) + '_against_all_comps.txt', sep='\t')

def mass_rv_outliers(obj_filename, obj_name, path_to_df):
    """
    Runs NIRSPEC.main to calculate the radial velocity of one object using a number of standards when you need to specify acceptable pixel shifts.

    Argument: filename of the object's spectum (wavelength and flux), name of the object (as a string), path to a tab separated panda dataframe saved as a csv file (with 'filename', 'std_rv', 'std_unc', 'lower_pixel shift', 'upper_pixel_shift' columns)

    Output: a pandas dataframe saved as a tab separated csv file which is the original dataframe with additional 'obj_rv' and 'obj_unc columns
    """

    # Reads in the given dataframe
    df = pd.read_csv(path_to_df, sep='\t')

    rvs = []
    errors = []

    # Runs NIRSPEC.main for each standards listed in the DF
    for i, row in df.iterrows():
        rv, error = NIRSPEC.main(
            ['', row['filename'], row['std_rv'], row['std_unc'], obj_filename, 0, 200, row['lower_pixel_shift'],
             row['upper_pixel_shift']])
        rvs.append(rv)
        errors.append(error)

    # Creates new columns for the calculated rvs and errors
    df['obj_rv'] = rvs
    df['obj_unc'] = errors

    # Saves the new dataframe (with additional obj_rv and obj_unc columns
    df.to_csv(str(obj_name) + '_against_all_outliers.txt', sep='\t')
