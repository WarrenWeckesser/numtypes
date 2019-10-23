
# FIXME:
# Without this import of numpy here, attempting to import nint32
# before importing numpy results in the error
#    ImportError: dlopen(/Users/warren/mc37numpy/lib/python3.7/site-packages/numtypes/_nint.cpython-37m-darwin.so, 2): Symbol not found: _npy_half_isnan
#      Referenced from: /Users/warren/mc37numpy/lib/python3.7/site-packages/numtypes/_nint.cpython-37m-darwin.so
#      Expected in: flat namespace
#     in /Users/warren/mc37numpy/lib/python3.7/site-packages/numtypes/_nint.cpython-37m-darwin.so
# Probably need to fix this in setup.py to ensure that the npy_math library is
# linked to the extension module.
import numpy as _np

from ._nint import nint32
from ._complex_int import (complex_int8, complex_int16,
                           complex_int32, complex_int64)
