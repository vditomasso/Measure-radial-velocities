from Measure-radial-velocities.weighted_stddev import wstddev

def test_weighted_stddev_1():
    assert wstddev([5,6,7],[1,2,1]) == (6.0, 1.0)