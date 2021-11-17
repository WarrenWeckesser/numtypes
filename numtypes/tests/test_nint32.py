
import pytest
import math
import numpy as np
from numpy.testing import assert_equal
from numtypes import nint32


def test_basic():
    x = nint32(3)
    assert x == 3
    assert int(x) == 3


@pytest.mark.parametrize('typ', [np.int8, np.uint8, np.int16, np.uint16,
                                 np.int32, np.uint32, np.int64, np.uint64])
def test_init_np_types(typ):
    x = nint32(typ(123))
    assert x == 123


def test_init_str_type():
    x = nint32("123")
    assert x == 123


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


@pytest.mark.parametrize('arg', [2.5, None, 'abc'])
def test_init_bad_arg(arg):
    with pytest.raises(TypeError, match='argument must be'):
        nint32(arg)


@pytest.mark.parametrize('extreme_func, expected',
                         [(np.maximum, [20, 10, 18]),
                          (np.minimum, [10, -2, 10])])
def test_extreme_func(extreme_func, expected):
    a = np.array([10, -2, 18], dtype=np.int32).astype(nint32)
    b = np.array([20, 10, 10], dtype=np.int32).astype(nint32)
    m = extreme_func(a, b)
    assert m.dtype == nint32
    assert_equal(m, expected)


@pytest.mark.parametrize('methodname, expected', [('min', -2), ('max', 18)])
def test_extreme_method(methodname, expected):
    a = np.array([10, -2, 18], dtype=nint32)
    m = getattr(a, methodname)()
    assert m.dtype == nint32
    assert m == expected


@pytest.mark.parametrize('methodname', ['min', 'max'])
def test_extreme_method_with_nan(methodname):
    a = np.array([10, np.nan, -2, 18], dtype=nint32)
    m = getattr(a, methodname)()
    assert m.dtype == nint32
    assert np.isnan(m)
