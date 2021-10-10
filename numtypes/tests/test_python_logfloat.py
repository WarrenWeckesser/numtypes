import pytest
import math
import operator
from fractions import Fraction
from numtypes import logfloat


@pytest.mark.parametrize('value, log', [(3, math.log(3)),
                                        (1000, math.log(1000)),
                                        (0, -math.inf),
                                        (Fraction(1, 2), math.log(0.5))])
def test_creation(value, log):
    x = logfloat(value)
    # XXX Using equality for comparing float values!  This assumes
    # the C math lib log function gives the same result as Python's
    # math.log.
    assert x.log == log


@pytest.mark.parametrize('logvalue', [20000, 2, 0.9, 0, -1.5, -25000,
                                      Fraction(1, 4)])
def test_creation_from_log(logvalue):
    x = logfloat(log=logvalue)
    assert x.log == float(logvalue)


def test_no_empty_args():
    x = logfloat()
    assert x.log == -math.inf


def test_too_many_inputs():
    with pytest.raises(TypeError, match='either a positional argument or'):
        logfloat(3, log=1.5)


def test_too_many_positional():
    with pytest.raises(TypeError, match='at most 1 positional'):
        logfloat(3, 1.5)


def test_negate():
    x = logfloat(3)
    with pytest.raises(ValueError, match='domain error'):
        -x


def test_abs():
    x = logfloat(3)
    y = abs(x)
    assert y.log == x.log


@pytest.mark.parametrize('log, value', [(99, True),
                                        (0.0, True),
                                        (-10, True),
                                        (-math.inf, False)])
def test_bool(log, value):
    x = logfloat(log=log)
    assert bool(x) == value


def test_add():
    # Use moderate values so we can test the result against the
    # naive formula.
    x = logfloat(3)
    y = logfloat(4)
    z = x + y
    assert math.isclose(z.log, math.log(math.exp(x.log) + math.exp(y.log)),
                        rel_tol=5e-15)


def test_add_extreme1():
    # With these values, the exponentials in the naive formula
    # would underflow to 0.0.  The exact value for the log of
    # the sum was computed with mpmath:
    #   >>> import mpmath
    #   >>> mpmath.mp.dps = 100  # Lots of digits
    #   >>> float(mpmath.log(mpmath.exp(-1200) + mpmath.exp(-1210)))
    #   -1199.9999546011009
    x = logfloat(log=-1200.0)
    y = logfloat(log=-1210.0)
    assert math.isclose((x + y).log, -1199.9999546011009, rel_tol=5e-15)


def test_add_extreme2():
    x = logfloat(log=-200)
    # The expected value can be evaluated as math.log1p(math.exp(-200)).
    assert math.isclose((x + 1).log, 1.3838965267367376e-87, rel_tol=5e-15)


def test_subtract():
    # Use moderate values so we can test the result against the
    # naive formula.
    x = logfloat(5.0)
    y = logfloat(0.25)
    z = x - y
    assert math.isclose(z.log, math.log(math.exp(x.log) - math.exp(y.log)),
                        rel_tol=5e-15)


def test_subtract_extreme1():
    # With these values, the exponentials in the naive formula
    # would underflow to 0.0.  The exact value for the log of
    # the difference was computed with mpmath:
    #   >>> import mpmath
    #   >>> mpmath.mp.dps = 100  # Lots of digits
    #   >>> float(mpmath.log(mpmath.exp(-1200) - mpmath.exp(-1210)))
    #   -1200.0000454009603
    x = logfloat(log=-1200.0)
    y = logfloat(log=-1210.0)
    assert math.isclose((x - y).log, -1200.0000454009603, rel_tol=5e-15)


def test_substract_extreme2():
    x = logfloat(log=-200)
    # The expected value can be evaluated as math.log1p(-math.exp(-200)).
    assert math.isclose((1 - x).log, -1.3838965267367376e-87, rel_tol=5e-15)


def test_invalid_subtract():
    x = logfloat(3)
    y = logfloat(5)
    with pytest.raises(ValueError, match='domain error'):
        x - y


def test_multiply():
    x = logfloat(log=-20)
    y = logfloat(log=123.5)
    z = x*y
    assert math.isclose(z.log, x.log + y.log, rel_tol=5e-15)


def test_divide():
    x = logfloat(log=-20)
    y = logfloat(log=123.5)
    z = x / y
    assert math.isclose(z.log, x.log - y.log, rel_tol=5e-15)


def test_power1():
    x = logfloat(log=2)
    assert (x**3).log == 6.0


def test_power2():
    x = logfloat(4)
    assert math.isclose((3**x).log, 4*math.log(3), rel_tol=5e-15)


@pytest.mark.parametrize('op', [operator.lt, operator.le, operator.eq,
                                operator.ne, operator.gt, operator.ge])
@pytest.mark.parametrize('compare_value', [3.0, 4.0, 5.0, logfloat(3.0),
                                           logfloat(4.0), logfloat(5.0)])
def test_comparison(op, compare_value):
    x = logfloat(4.0)
    assert op(compare_value, x) == op(compare_value, 4.0)
    assert op(x, compare_value) == op(4.0, compare_value)
