# Just a few tests at the moment.

import math
import pytest
from numtypes import polarcomplex64, polarcomplex128


@pytest.mark.parametrize('typ, atol, rtol',
                         [(polarcomplex64, 1e-7, 1e-7),
                          (polarcomplex128, 1e-15, 1e-15)])
def test_comparison(typ, atol, rtol):
    x = typ(-5)
    y = typ(1j)
    z = typ(3+4j)
    assert x == -5
    assert math.isclose(y.real, 0, abs_tol=atol)
    assert math.isclose(y.imag, 1, rel_tol=rtol)
    assert z.r == 5
    assert math.isclose(z.theta, math.atan2(4, 3), rel_tol=rtol)


@pytest.mark.parametrize('typ, rtol',
                         [(polarcomplex64, 1e-7),
                          (polarcomplex128, 1e-15)])
def test_addition(typ, rtol):
    z1 = 1 + 2j
    z2 = 3 - 4j
    p1 = typ(z1)
    p2 = typ(z2)
    zsum = z1 + z2
    psum = p1 + p2
    pzsum = typ(zsum)
    assert math.isclose(psum.r, pzsum.r, rel_tol=rtol)
    assert math.isclose(psum.theta, pzsum.theta, rel_tol=rtol)


@pytest.mark.parametrize('typ, atol, rtol',
                         [(polarcomplex64, 1e-7, 1e-7),
                          (polarcomplex128, 1e-15, 1e-15)])
def test_true_division_int(typ, atol, rtol):
    z = typ(3+4j)
    z2 = z / 2
    # Division of polarcomplex64 by Python number results in cast
    # to polarcomplex128.
    assert isinstance(z2, polarcomplex128)
    assert z2.r == 2.5
    assert math.isclose(z2.theta, math.atan2(4, 3), rel_tol=rtol)


@pytest.mark.parametrize('typ, atol, rtol',
                         [(polarcomplex64, 1e-7, 1e-7),
                          (polarcomplex128, 1e-15, 1e-15)])
def test_multiplication(typ, atol, rtol):
    z1 = typ(3+4j)
    z2 = typ(5+12j)
    w = z1 * z2
    assert w.r == 65
    assert math.isclose(w.theta, math.atan2(4, 3) + math.atan2(12, 5),
                        rel_tol=rtol)


@pytest.mark.parametrize('typ, atol, rtol',
                         [(polarcomplex64, 1e-7, 1e-6),
                          (polarcomplex128, 1e-15, 1e-15)])
def test_true_division(typ, atol, rtol):
    z1 = typ(3+4j)
    z2 = typ(5+12j)
    w = z2 / z1
    assert math.isclose(w.r, 13/5, rel_tol=rtol)
    assert math.isclose(w.theta, math.atan2(12, 5) - math.atan2(4, 3),
                        rel_tol=rtol)
