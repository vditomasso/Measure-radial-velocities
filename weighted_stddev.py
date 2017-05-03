import numpy as np


# Weighted Standard Devation taken from http://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
def wstddev(x, u):

    x = np.asarray(x)
    u = np.asarray(u)

    w = 1 / (u ** 2)
    average = np.average(x, weights=w)
    variance = np.dot(w, (x - average) ** 2) / w.sum()

    return average, np.sqrt(variance)
