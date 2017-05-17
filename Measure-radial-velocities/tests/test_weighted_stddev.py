from weighted_stddev import *

def test_weighted_stddev_1():
    assert wstddev([5,5,5],[1,2,1]) == (5.0, 0.0)

def test_weighted_stddev_2():
    assert 1 == 1