import math
import numpy
import find_rv
from astropy.io import ascii
from astropy import coordinates
from astropy import time
from astropy import units
# from astrolib import baryvel
import sys
import matplotlib.pyplot as plt


def deg2HMS(input):
    deg = int(input)
    min = (input - deg) * 60.
    sec = (((input - deg) * 60.) - min) * 60.

    return [deg, min, sec]


def HMS2deg(input):
    if len(input) == 1:
        deg = abs(float(input[0]))
    elif len(input) == 2:
        deg = abs(float(input[0])) + float(input[1]) / 60.
    elif len(input) == 3:
        deg = abs(float(input[0])) + float(input[1]) / 60. + float(input[2]) / 3600.

    if float(input[0]) < 0:
        deg = deg * -1
    return deg


# Weighted Standard Devation taken from http://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
def wstddev(x, w):
    average = numpy.average(x, weights=w)
    variance = numpy.dot(w, (x - average) ** 2) / w.sum()
    return average, math.sqrt(variance)


# AR 2012.1203: Remove telluric features entirely.
# AR 2012.1227: Now a slightly more generic one-d clipping routine.  Assumes a[0] is the index being tested
def clip(a, start, end):
    # Returns the linked arrays 'a' with the entries from 'start' to 'end' clipped out.
    # change 3 arrays:
    #    (wave[0], wave[1], wave[2]...; flux[0], flux[1], flux[2]...; er[0], err[1], err[2]...)
    # into 1 array of paired tuples:
    #    ([wave[0],flux[0], err[0]], [wave[1],flux[1],err[1]], [wave[2],flux[2],err[2]], ...).
    b = zip(*a)
    indices = []
    c = []
    # make a new array of just the good elements
    for i in range(len(b)):
        wave = b[i][0]
        # print(wave)
        if not (wave > start and wave < end):
            c.append(b[i])
            indices.append(i)

            out = zip(*c)
    # return an un-zipped array
    return numpy.asarray(out)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    std_path = argv[1]

    rv_std = float(argv[2])
    rv_std_err = float(argv[3])
    obj_path = argv[4]
    crop = float(argv[5])
    try:
        xcorr_width = float(
            argv[8])  # I changed the xcorr_width, cutstart and cutend to the 8th, 9th and 10th arguments
    except IndexError:
        xcorr_width = float(200)
    try:
        cutstart = argv[9]
        cutend = argv[10]
        cut = 1
    except IndexError:
        cutstart = 0
        cutend = 0
        cut = 0
    try:
        obj_snr_path = argv[6]  # The 6th argument is the paths to the object uncertainty file
        obj_snr_read = ascii.read(obj_snr_path)  # I tried to emulate the way the spectra files are read in
        # obj_unc = zip(*obj_unc_read)
        obj_snr = numpy.asarray(obj_snr_read['snr'])

    except IndexError:
        obj_snr = 10
    try:
        std_snr_path = argv[7]  # The 7th argument is the path to the standard uncertainty file
        std_snr_read = ascii.read(std_snr_path)
        # std_unc = zip(*std_unc_read)
        # std_unc = numpy.asarray(std_unc['snr'])
        std_snr = numpy.asarray(std_snr_read['snr'])

    except IndexError:
        std_snr = 10

    # print(std_unc)
    # print(avg_unc)

    spec_obj = ascii.read(obj_path)
    spec_std = ascii.read(std_path)

    # Extract the name and order of the spectrum from the title of the file.
    # example: 2M1935_62.22may14_ascii_hc
    head_obj = obj_path.split('_')
    head_std = std_path.split('_')

    # print('head_obj = ',head_obj)
    # print('head_std = ',head_std)

    starname_obj = head_obj[1].split('/')[1]
    starname_std = head_std[1].split('/')[2]
    order_obj = int(head_obj[2].split('.')[0])  # .split('.')[0])
    order_std = int(head_std[3].split('.')[0])

    if order_obj != order_std:
        raise ValueError

    # obj = spec_obj
    # std = spec_std

    # spec_obj.close()
    # spec_std.close()
    obj_wave = numpy.asarray(spec_obj['col1'])
    obj_flux = numpy.asarray(spec_obj['col2'])

    avg_snr = numpy.sum(obj_snr) / len(obj_snr)
    if avg_snr > 4.0:
        obj_unc = 1.0 / obj_snr
    else:
        obj_unc = obj_snr

    std_wave = numpy.asarray(spec_std['col1'])
    std_flux = numpy.asarray(spec_std['col2'])

    avg_snr = numpy.sum(std_snr) / len(std_snr)
    if avg_snr > 4.0:
        std_unc = 1.0 / std_snr
    else:
        std_unc = std_snr

    # remove spikes (bad pixels, etc) from the spectrum. Use with caution.
    if crop == 1:
        # find spikes.  Select all that are NOT.
        mask = numpy.where(abs(obj_flux - numpy.mean(obj_flux)) < 3.0 * numpy.std(obj_flux, ddof=1))
        obj_wave = obj_wave[mask]
        obj_flux = obj_flux[mask]
        obj_unc = obj_unc[mask]

        # print(wave_obj)
    stardata_obj = []
    stardata_std = []

    # print('stardata_std = ',stardata_std,'starname_obj = ',starname_obj)

    # open an output file to put the data in.
    outputname = 'std_{0:}_for_obj_{1:}.txt'.format(starname_std, starname_obj)
    g = open(outputname, 'w')

    # This actually runs the RV fitting routine.
    # obj_wave,obj_flux,obj_unc,std_wave,std_flux,std_unc,obj_name,std_name,order,xcorr_width,cut?,cutstart,cutend
    rv_meas, rv_meas_err = find_rv.radial_velocity(obj_wave, obj_flux, obj_unc, std_wave, std_flux, std_unc,
                                                   starname_obj, starname_std, rv_std, rv_std_err, order_obj,
                                                   xcorr_width, cut, cutstart, cutend)

    g.write('rv_meas = {0:>+.2f} +/- {1:>+.2f}\n'.format(rv_meas, rv_meas_err))
    # correct radial velocity to standard
    # we can calculate the correct measured RV here.
    rv_obj = rv_std + rv_meas
    # we only want to add together the per-measurement errors and weight them appropriately.
    #  Leave the fixed error on the RV standard out of this. (add in at the end)
    rv_obj_err = numpy.sqrt(rv_meas_err ** 2 + rv_std_err ** 2)

    return [rv_obj, rv_obj_err]

    outstring1 = "std:{1:} obj:{0:}  Order {2:>2d} rv={3:>6.3f} +/- {4:>6.3f}\n".format(starname_obj, starname_std, order_obj, rv_obj, rv_obj_err)
    print(outstring1)
    g.write(outstring1)

    g.close()


if __name__ == "__main__":
    main()
