# Just a few tests at the moment.

import pytest
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


@pytest.mark.parametrize('nanstr', ['nan', '\t+NAN ', '-nAn'])
def test_nan_str(nanstr):
    z = nint32(nanstr)
    assert math.isnan(float(z))
    assert math.isnan(z + 1.5)


def test_nan():
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


@pytest.mark.parametrize('value', [2**31, -2**31, 2**65])
def test_init_arg_too_big(value):
    with pytest.raises(OverflowError, match='int too big to convert'):
        nint32(value)


@pytest.mark.parameterize('arg', [2.5, None, 'abc'])
def test_init_bad_arg(arg):
    with pytest.raises(TypeError, match='argument must be'):
        nint32(arg)
