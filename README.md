numtypes
========

Custom data types for NumPy.

The following data types are defined in this library:

* `logfloat32` and `logfloat64` are nonnegative floating point values
  that store the *logarithm* of the value instead of the value.  Arithmetic
  operations and NumPy ufuncs are implemented to allow operations on these
  types over a large range of values without overflow or underflow.
* `nint32` is a 32 bit signed integer type that uses the most negative
  value as `nan`.
* `polarcomplex64` and `polarcomplex128` are complex numbers represented
  in polar coordinates.  (The Python objects and NumPy data types have been
  created, but the NumPy ufuncs are not implemented yet.)
* `logfloat` is a Python type that represents nonnegative floating point
  numbers.  The type works with the logarithm of the numbers internally,
  so it can do elementary arithmetic with values such as exp(-1200).
  This is a *Python* type only; the NumPy types are `logfloat32` and `logfloat64`.

This package is an experimental work in progress.  Use at your own risk!

Examples
--------

### `logfloat32` and `logfloat64`

The following shows calculations involving floating point values that
would be too small to represent as standard IEEE-754 32 bit floating
point:

    >>> import numpy as np
    >>> from numtypes import logfloat32

Note that `logfloat32(log=-1000)` represents the value whose log is
-1000, which is approximately `5.0759588975e-435`.

    >>> x = np.array([logfloat32(log=-1000), logfloat32(log=-1001.5),
    ...               logfloat32(log=-1002)])
    ...
    >>> x
    array([logfloat32(log=-1000.0), logfloat32(log=-1001.5),
           logfloat32(log=-1002.0)], dtype=logfloat32)
    >>> 2*x
    array([logfloat32(log=-999.3068), logfloat32(log=-1000.8068),
           logfloat32(log=-1001.3068)], dtype=logfloat32)
    >>> np.sqrt(x)
    array([logfloat32(log=-500.0), logfloat32(log=-500.75),
           logfloat32(log=-501.0)], dtype=logfloat32)
    >>> c = np.full(len(x), fill_value=logfloat32(log=-999))
    >>> c
    array([logfloat32(log=-999.0), logfloat32(log=-999.0),
           logfloat32(log=-999.0)], dtype=logfloat32)
    >>> x + c
    array([logfloat32(log=-998.68677), logfloat32(log=-998.9211),
           logfloat32(log=-998.9514)], dtype=logfloat32)
    >>> x * c
    array([logfloat32(log=-1999.0), logfloat32(log=-2000.5),
           logfloat32(log=-2001.0)], dtype=logfloat32)
    >>> x / c
    array([logfloat32(log=-1.0), logfloat32(log=-2.5), logfloat32(log=-3.0)],
           dtype=logfloat32)


### Integers with `nan`, `nint32`

Some examples of `nint32`:

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


### Polar complex types

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
    polarcomplex128((2, -1.0471976))

The Python object implements the usual arithmetic operations.
(This also demonstrates passing a Python complex number to the type.)

    >>> pz2 = polarcomplex128(5 + 12j)
    >>> pz2
    polarcomplex128((13, 1.1760052))
    >>> -pz2
    polarcomplex128((-13, 1.1760052))
    >>> abs(pz2)
    13.0
    >>> pz2 / pz1
    polarcomplex128((6.5, 0.12880766))
    >>> pz1 + pz2
    polarcomplex128((14.985634, 1.158861))

Check that converting the values to Python complex numbers gives the same
result, whether we add before or after the conversion.

    >>> complex(pz1 + pz2)
    (5.999999999999999+13.732050807568877j)
    >>> complex(pz1) + complex(pz2)
    (6.000000000000001+13.732050807568877j)

The NumPy type `complex64` and `complex128` can be converted to the polar
types.

    >>> a = np.array([1 + 2j, 3+4j, -5j])
    >>> a.astype(polarcomplex64)
    array([polarcomplex64((2.236068, 1.1071488)),
           polarcomplex64((5, 0.92729521)), polarcomplex64((5, -1.5707964))],
          dtype=polarcomplex64)


### `logfloat`

`logfloat` represents a nonnegative floating point number. It stores the
logarithm of the number internally, so it can represent a much greater
range of values than the standard Python `float`.  The logarithm is displayed
in the `repr`, and can be accessed with the `.log` attribute.  The basic
Python arithmetic operators have been implemented.

    >>> from numtypes import logfloat
    >>> x = logfloat(log=-1000)
    >>> x
    logfloat(log=-1000)

`x` represents `exp(-1000)`.  The value is too small to be represented
as a regular 64 bit `float`:

    >>> float(x)
    0.0

The basic arithmetic operators are implemented for the `logfloat`
type:

    >>> x/2
    logfloat(log=-1000.6931471805599)
    >>> 1/x
    logfloat(log=1000)
    >>> x**0.5
    logfloat(log=-500)

`y` is another very small value:

    >>> y = logfloat(log=-1002)
    >>> x + y
    logfloat(log=-999.873071988957)
    >>> x - y
    logfloat(log=-1000.1454134578688)
    >>> x/y
    logfloat(log=2)

--------------------------------------------------------------------------

Related work and links
----------------------

* [quaternion](https://github.com/moble/quaternion)
* [numpy-user-dtypes](https://github.com/numpy/numpy-user-dtypes):
  Repository for example user DTypes using the new API.
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
