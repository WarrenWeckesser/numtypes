numtypes
========

Custom data types for numpy.

The following data types are defined in this library:

* `nint32` is a 32 bit signed integer type that uses the most negative
  value as `nan`.
* `complex_int8`, `complex_int16`, `complex_int32` and `complex_int64` are
  complex numbers with integer real and imaginary parts.
* `polarcomplex64` and `polarcomplex128` are complex numbers represented
  in polar coordinates.  (The Python objects and NumPy data types have been
  created, but the NumPy ufuncs are not implemented yet.)

This package is an experimental work in progress.  Use at your own risk!

Examples
--------

Some examples of `nint32`::

    >>> import numpy as np
    >>> from numtypes import nint32

    >>> a = np.array([10, -99, 0, 1234], dtype=nint32)
    >>> a
    array([10, -99, 0, 1234], dtype=nint32)
    >>> a.sum(initial=nint32(0))
    1145

    >>> b = np.array([9, np.nan, 100, -1], dtype=nint32)
    >>> b
    array([9, nan, 100, -1], dtype=nint32)
    >>> b.sum(initial=nint32(0))
    nan
    >>> b // nint32(5)                     # Preserves dtype
    array([1, nan, 20, -1], dtype=nint32)
    >>> b / 5                              # True divide, casts to float64.
    array([ 1.8,  nan, 20. , -0.2])

    >>> a + b
    array([19, nan, 100, 1233], dtype=nint32)
    >>> a * b
    array([90, nan, 0, -1234], dtype=nint32)
    >>> a / b
    array([ 1.11111111e+00,             nan,  0.00000000e+00, -1.23400000e+03])

    >>> a.astype(np.int32)
    array([  10,  -99,    0, 1234], dtype=int32)
    >>> b.astype(np.int32)  # Note that nint32('nan') casts to -2147483648.
    array([          9, -2147483648,         100,          -1], dtype=int32)
    >>> b.astype(np.float32)
    array([  9.,  nan, 100.,  -1.], dtype=float32)

    >>> np.isnan(b)
    array([False,  True, False, False])

The complex integer data types::

    >>> from numtypes import complex_int8, complex_int32

    >>> z8 = np.array([complex_int8(1+2j), complex_int8(3-4j), complex_int8(5+12j)])
    >>> z8
    array([(1+2j), (3-4j), (5+12j)], dtype='complex_int8')

    >>> abs(z8)
    array([ 2.23606798,  5.        , 13.        ])

    >>> z8.conj()
    array([(1-2j), (3+4j), (5-12j)], dtype='complex_int8')

    >>> z8 * z8.conj()
    array([(5+0j), (25+0j), (-87+0j)], dtype='complex_int8')  # Note the overflow!

    >>> z8 + 100
    array([(101+2j), (103-4j), (105+12j)], dtype='complex_int8')

    >>> 3*z8
    array([(3+6j), (9-12j), (15+36j)], dtype='complex_int8')

    >>> z32 = np.array([complex_int32(1j), complex_int32(8+0j), complex_int32(12+5j)])
    >>> z32
    array([(0+1j), (8+0j), (12+5j)], dtype='complex_int32')

    >>> z8 + z32
    array([(1+3j), (11-4j), (17+17j)], dtype='complex_int32')

**Note**:  Currently, the `.real` and `.imag` properties of the `complex_int`
data types do not work correctly!

    >>> z8.real
    array([(1+2j), (3-4j), (5+12j)], dtype='complex_int8')
    >>> z8.imag
    array([(0+0j), (0+0j), (0+0j)], dtype='complex_int8')

Some examples of `polarcomplex64` and `polarcomplex128`:

    >>> from numtypes import polarcomplex64, polarcomplex128

A tuple given to the type holds the magnitude and angle of the complex number.
The attributes `r` and `theta` return these values.

    >>> pz1 = polarcomplex128((2, np.pi/3))
    >>> pz1
    polarcomplex128((2, 1.0471976))
    >>> pz1.r
    2.0
    >>> pz1.theta
    1.0471975511965976

The `real` and `imag` attributes compute the real and imaginary parts of
the complex number.

    >>> pz1.real
    1.0000000000000002
    >>> pz1.imag
    1.7320508075688772

The `conj()` method returns the complex conjugate.  In polar coordinates,
this simply changes the sign of the angle.

    >>> pz1.conj()
    polarcomplex128((4, -0.52359878))

The Python object implements the usual arithmetic operations.
(This also demonstrates passing a Python complex number to the type.)

    >>> pz2 = polarcomplex128(5 + 12j)
    >>> pz2
    >>> -pz2
    polarcomplex128((-13, 1.1760052))
    >>> abs(pz2)
    13.0
    >>> pz2 / pz1
    polarcomplex128((3.25, 0.65240643))
    >>> complex(pz1 + pz2)
    >>> pz1 + pz2
    polarcomplex128((16.359738, 1.0270169))

Check that converting the values to Python complex numbers
gives the same result, whether we add before or after the conversion.

    >>> complex(pz1 + pz2)
    (8.464101615137757+13.999999999999998j)
    >>> complex(pz1) + complex(pz2)
    (8.464101615137755+14j)

The NumPy type `complex64` and `complex128` can be converted to the polar
types.

    >>> a = np.array([1 + 2j, 3+4j, -5j])
    >>> a.astype(polarcomplex64)
    array([polarcomplex64((2.236068, 1.1071488)),
           polarcomplex64((5, 0.92729521)), polarcomplex64((5, -1.5707964))],
          dtype=polarcomplex64)


Related work and links
----------------------

* [quaternion](https://github.com/moble/quaternion)
* [numpy-dtypes](https://github.com/numpy/numpy-dtypes)
  - Includes rational and quaternion, but not actively maintained.
    See moble's github repo for a maintained version of quaternions.
* Stéfan van der Walt's class notes from the 2013 "Dive Into NumPy" class,
      https://github.com/stefanv/teaching/tree/master/2013_scipy_austin_dive_into_numpy
  - The steps in examples/quad_dtype show how to add a dtype for the
    quad precision floating point type provided by gcc.
* NumPy:
      https://github.com/numpy/numpy/blob/master/numpy/core/src/umath/_rational_tests.c.src
  - This implements a rational dtype as a unit test.
* NumPy documentation of [user-defined data types](https://numpy.org/doc/1.17/user/c-info.beyond-basics.html#user-defined-data-types)
* [ora](https://github.com/alexhsamuel/ora) implements time and datetime data types.
