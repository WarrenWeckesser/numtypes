numtypes
========

Custom data types for numpy.

Currently the only new data type defined here is `numtypes.nint32`, a 32 bit
signed integer type that uses the most negative value as `nan`.

This package is an experimental work in progress.

Examples
--------

The `nint32` dtype is still a work in progress.  Here are some examples
of what is implemented so far::

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

    >>> a + b
    array([19, nan, 100, 1233], dtype=nint32)
    >>> a * b
    array([90, nan, 0, -1234], dtype=nint32)

    >>> a.astype(np.int32)
    array([  10,  -99,    0, 1234], dtype=int32)
    >>> b.astype(np.int32)
    array([          9, -2147483648,         100,          -1], dtype=int32)
    >>> b.astype(np.float32)
    array([  9.,  nan, 100.,  -1.], dtype=float32)

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
* NumPy "floatint" example in
      https://github.com/numpy/numpy/tree/master/doc/newdtype_example
  - Not well documented, not updated for Python 3.
* NumPy:
      https://github.com/numpy/numpy/blob/master/numpy/core/src/umath/_rational_tests.c.src
  - This implements a rational dtype as a unit test.
* NumPy documentation of [user-defined data types](https://numpy.org/doc/1.17/user/c-info.beyond-basics.html#user-defined-data-types)
* [ora](https://github.com/alexhsamuel/ora) implements time and datetime data types.
