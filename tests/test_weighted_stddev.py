from Measure-radial-velocity.weighted_stddev import *
import pytest

def test_weighted_stddev_1():
    assert wstddev([5,6,7],[1,2,1]) == (6.0, 1.0)

def test_weighted_stddev_2():
    assert 1 == 1

# def f():
#     return 3
#
# def test_function():
#     assert f() == 3