import pytest
import operator
import math
import numpy as np
from numpy.testing import assert_allclose, assert_equal
from numtypes import logfloat32, logfloat64


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Tests of the scalar types logfloat32 and logfloat64
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('logvalue', [-np.inf, -2.5, 0, 0.5, np.inf])
def test_log_value(typ, logvalue):
    lfx = typ(log=logvalue)
    assert lfx.log == logvalue


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('op', [operator.add, operator.sub,
                                operator.mul, operator.truediv,
                                operator.pow])
def test_basic_binary_ops_for_scalars(typ, op):
    x = 3.0
    y = 2.0
    lfx = typ(x)
    lfy = typ(y)
    lfz = op(lfx, lfy)
    assert isinstance(lfz, typ)
    assert math.isclose(float(lfz), op(x, y),
                        rel_tol=2*np.finfo(lfz.log).resolution)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('op, logexpected',
                         [(operator.add, -999.9211102657074),
                          (operator.sub, -1000.085650483742),
                          (operator.mul, -2002.5),
                          (operator.truediv, 2.5),
                          (operator.pow, 0.0)])
def test_basic_binary_ops_for_scalars_extreme(typ, op, logexpected):
    logx = -1000.0
    logy = -1002.5
    lfx = typ(log=logx)
    lfy = typ(log=logy)
    lfz = op(lfx, lfy)
    assert isinstance(lfz, typ)
    assert math.isclose(lfz.log, logexpected,
                        rel_tol=2*np.finfo(lfz.log).resolution)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_pow_for_scalars_extreme_small(typ):
    logx = -750.0
    logy = -100.0
    lfx = typ(log=logx)
    lfy = typ(log=logy)
    lfz = lfx ** lfy
    assert isinstance(lfz, typ)
    assert math.isclose(lfz.log, -2.790056982015627e-41,
                        rel_tol=25*np.finfo(lfz.log).resolution)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_pow_for_scalars_extreme_big(typ):
    logx = 800.0
    y = 500.0
    lfx = typ(log=logx)
    lfy = typ(y)
    lfz = lfx ** lfy
    assert isinstance(lfz, typ)
    assert math.isclose(lfz.log, 400000.0,
                        rel_tol=25*np.finfo(lfz.log).resolution)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('op', [abs, operator.pos])
def test_basic_unary_ops_for_scalars(typ, op):
    x = 3.0
    lfx = typ(x)
    lfy = op(lfx)
    assert isinstance(lfy, typ)
    # Only testing + and abs, so the result should be equal
    # to the input.
    assert lfy == lfx


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_bool_scalar(typ):
    assert bool(typ(0)) is False
    assert bool(typ(2.0)) is True


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Test of array casting from and to logfloat32 and logfloat64
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_basic_casting_from_logfloat(typ):
    x = np.array([typ(10), typ(1), typ(0.1), typ(0)])
    y = x.astype(np.float64)
    rtol = 5*np.finfo(x[0].log).resolution
    assert_allclose(y, [10, 1, 0.1, 0], rtol=rtol)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_basic_casting_from_double_to_logfloat(typ):
    x = np.array([10, 1, 0.1, 0])
    y = x.astype(typ)
    rtol = 25*np.finfo(typ(1).log).resolution
    with np.errstate(divide='ignore'):
        expected_log = np.log(x)
    assert_allclose([t.log for t in y], expected_log, rtol=rtol)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('inttyp', [np.uint8, np.int8, np.uint16, np.int16,
                                    np.uint32, np.int32, np.uint64, np.int64])
def test_basic_casting_from_int_to_logfloat(typ, inttyp):
    x = np.array([0, 1, 2, 3, 10, 50, 125], dtype=inttyp)
    y = x.astype(typ)
    rtol = 5*np.finfo(typ(1).log).resolution
    with np.errstate(divide='ignore'):
        expected_log = np.log(x, dtype=np.float64)
    assert_allclose([t.log for t in y], expected_log, rtol=rtol)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Tests of ufuncs on arrays with types logfloat32 and logfloat64
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('ufunc', [np.square, np.sqrt, np.cbrt,
                                   np.sign, np.exp, np.exp2, np.expm1,
                                   np.reciprocal])
def test_basic_unary_ufuncs(typ, ufunc):
    x = np.array([0.5, 1.5, 2.0])
    lfx = x.astype(typ)
    lfz = ufunc(lfx)
    assert lfz.dtype == typ
    rtol = 5*np.finfo(typ(1).log).resolution
    with np.errstate(divide='ignore'):
        expected_log = np.log(ufunc(x))
    assert_allclose([t.log for t in lfz], expected_log, rtol=rtol)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
def test_basic_log_ufunc(typ):
    x = np.array([1.0, 1.5, 2.0, 10000.0])
    lfx = x.astype(typ)
    lfz = np.log(lfx)
    assert lfz.dtype == typ
    rtol = 5*np.finfo(typ(1).log).resolution
    with np.errstate(divide='ignore'):
        expected_log = np.log(np.log(x))
    assert_allclose([t.log for t in lfz], expected_log, rtol=rtol)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('ufunc', [np.positive, np.absolute])
def test_basic_unary_ufuncs_equal_check(typ, ufunc):
    x = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
    lfx = x.astype(typ)
    lfz = ufunc(lfx)
    assert lfz.dtype == typ
    assert_equal(lfz, lfx)


@pytest.mark.parametrize('typ', [logfloat32, logfloat64])
@pytest.mark.parametrize('ufunc', [np.add, np.subtract,
                                   np.multiply, np.true_divide,
                                   np.power])
def test_basic_binary_ufuncs(typ, ufunc):
    x = np.array([0.5, 1.5, 2.0])
    y = np.array([0.25, 0.25, 1.0])
    lfx = x.astype(typ)
    lfy = y.astype(typ)
    lfz = ufunc(lfx, lfy)
    assert lfz.dtype == typ
    rtol = 5*np.finfo(typ(1).log).resolution
    assert_allclose([t.log for t in lfz], np.log(ufunc(x, y)), rtol=rtol)
