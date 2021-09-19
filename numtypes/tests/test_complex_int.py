
import pytest
import numpy as np
from numpy.testing import assert_equal
import numtypes as nt


_complex_int_types = [nt.complex_int8, nt.complex_int16, nt.complex_int32,
                      nt.complex_int64]


@pytest.mark.parametrize('typ', _complex_int_types)
def test_array_nonzero(typ):
    za = np.array([typ(0j), typ(1+2j), typ(-3j), typ(0j), typ(5+0j)])
    assert_equal(za.nonzero()[0], np.array([1, 2, 4]))
