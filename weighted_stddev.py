import numpy

# Weighted Standard Devation taken from http://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
def wstddev(x,u):
    w = 1/(u**2)
    average = numpy.average(x,weights=w)
    variance = numpy.dot(w,(x-average)**2)/w.sum()
    return average,numpy.sqrt(variance)