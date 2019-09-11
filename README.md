# numtypes
Custom data types for numpy

This package is experimental and currently incomplete.

### Related work and links

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
