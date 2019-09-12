# Just a few tests at the moment.

import math
from numtypes import nint32


def test_basic():
    x = nint32(3)
    assert x == 3
    assert int(x) == 3


def test_comparison():
    x = nint32(100)
    y = nint32(-500)
    assert x > 0
    assert x < 200
    assert x < 123.4
    assert x <= 200
    assert 200 >= x
    assert x == 100
    assert x > y
    assert x >= y
    assert y < x
    assert y <= x
    assert x != y


def test_true_division():
    x = nint32(20)
    y = nint32(10)
    z = x / y
    assert isinstance(z, float)
    assert z == 2.0


def test_nan():
    z = nint32('nan')
    assert math.isnan(float(z))
    assert math.isnan(z + 1.5)

    z = nint32(math.nan)
    assert math.isnan(float(z))
    assert z != z


def test_bool():
    assert bool(nint32(123))
    assert bool(nint32('nan'))
    assert not bool(nint32(0))


def test_other():
    z = 1.0 + 2.0j
    a = nint32(2)
    w = z / a
    assert w == z/2
