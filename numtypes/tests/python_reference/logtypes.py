
import math
import cmath


class logfloat:
    """
    An instance of logfloat represents a nonnegative floating point value.

    The log of the value is stored internally.
    """

    def __init__(self, *args, logx=None):
        if len(args) > 1:
            raise ValueError('at most one positional argument may be given')
        if len(args) == 1 and logx is not None:
            raise ValueError('either a positional argument or logx can be given, '
                             'but not both')
        if logx is None and len(args) == 0:
            # No arguments given.  Since float() returns 0 and complex()
            # returns 0j, we'll return log(0) which is -math.inf.
            self._logx = -math.inf
        else:
            if logx is not None:
                self._logx = float(logx)
            else:
                arg = args[0]
                if isinstance(arg, logfloat):
                    self._logx = arg._logx
                else:
                    if arg == 0:
                        self._logx = -math.inf
                    else:
                        self._logx = math.log(arg)   

    def __repr__(self):
        return f"logfloat(logx={self._logx!r})"

    def __neg__(self):
        raise ValueError("math domain error; can't negate a logfloat instance")

    def __add__(self, other):
        # This is basically logaddexp.
        if not isinstance(other, logfloat):
            try:
                x2 = float(other)
            except Exception:
                return NotImplemented
            other = logfloat(x2)
        # Reorder so the first has the larger magnitude.
        if self._logx < other._logx:
            self, other = other, self
        logsum = self._logx + math.log1p(math.exp(other._logx - self._logx))
        return logfloat(logx=logsum)

    def __sub__(self, other):
        if not isinstance(other, logfloat):
            try:
                x2 = float(other)
            except Exception:
                return NotImplemented
            other = floata(z2)
        if self._logx < other._logx:
            raise ValueError("math domain error: can't subtract a larger "
                             "value from a smaller one")
        logdiff = self._logx  + math.log1p(-math.exp(other._logx - self._logx))
        return logfloat(logx=logdiff)

    def __mul__(self, other):
        if not isinstance(other, logfloat):
            try:
                x2 = float(other)
            except Exception:
                return NotImplemented
            other = logfloat(x2)
        return logfloat(logx=self._logx + other._logx)

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if not isinstance(other, logfloat):
            try:
                x2 = float(other)
            except Exception:
                return NotImplemented
            other = logfloat(x2)
        return logfloat(logx=self._logx - other._logx)

    def __rtruediv__(self, other):
        # invself is 1/self.
        invself = logfloat(logx=-self._logx)
        return invself*other

    def __pow__(self, other):
        x2 = float(other)
        return logfloat(logx=self._logx * x2)

    def __rpow__(self, other):
        if isinstance(other, logfloat):
            logy = other._logx
        else:
            logy = math.log(float(other))
        return logfloat(logx=float(self)*logy)

    def __float__(self):
        return math.exp(self._logx)

    def __bool__(self):
        return self._logx != -math.inf

    def __abs__(self):
        return self


def _reim(z):
    "Unpack the real and imaginary parts of z into a tuple."
    return z.real, z.imag


class logcomplex:
    """
    An instance of logcomplex represents a complex number.

    The log of the value is stored internally.
    """

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Python special methods.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, *args, logz=None):
        if len(args) > 1:
            raise ValueError('at most one positional argument may be given')
        if len(args) == 1 and logz is not None:
            raise ValueError('either a positional argument or logz can be given, '
                             'but not both')
        if logz is None and len(args) == 0:
            # No arguments given.  Since float() returns 0 and complex()
            # returns 0j, we'll return log(0j) which is -math.inf.
            self._logz = -math.inf + 0j
        else:
            if logz is not None:
                logz = complex(logz)
                # I'm not sure restricting the phase to [-pi, pi] is
                # a good idea.  It might be better leave it as given.
                self._logz = logz.real + 1j*math.remainder(logz.imag, math.tau)
            else:
                z = args[0]
                if isinstance(z, logcomplex):
                    self._logz = z._logz
                else:
                    self._logz = cmath.log(z)

    def __repr__(self):
        return f"logcomplex(logz={self._logz})"

    def __neg__(self):
        return logcomplex(logz=(self._logz.real +
                                1j*math.remainder(self._logz.imag + math.pi, math.tau)))

    def __add__(self, other):
        # This is basically logaddexp for complex inputs.
        if not isinstance(other, logcomplex):
            try:
                z2 = complex(other)
            except Exception:
                return NotImplemented
            other = logcomplex(z2)
        logr1, theta1 = _reim(self._logz)
        logr2, theta2 = _reim(other._logz)
        # Reorder so the first has the larger magnitude.
        if logr1 < logr2:
            logr1, logr2 = logr2, logr1
            theta1, theta2 = theta2, theta1
        ndiff = -(logr1 - logr2)
        s = math.exp(ndiff)
        logr = logr1 + 0.5*math.log1p(s*(s + 2*math.cos(theta1 - theta2)))
        theta = math.atan2(math.sin(theta1) + s*math.sin(theta2),
                            math.cos(theta1) + s*math.cos(theta2))
        return logcomplex(logz=complex(logr, theta))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if not isinstance(other, logcomplex):
            try:
                z2 = complex(other)
            except Exception:
                return NotImplemented
            other = logcomplex(z2)
        logr1, theta1 = _reim(self._logz)
        logr2, theta2 = _reim(other._logz)
        # Reorder so the first has the larger magnitude.
        sgn = 1
        if logr1 < logr2:
            logr1, logr2 = logr2, logr1
            theta1, theta2 = theta2, theta1
            sgn = -1
        ndiff = -(logr1 - logr2)
        s = math.exp(ndiff)
        logr = logr1 + 0.5*math.log1p(s*(s - 2*math.cos(theta1 - theta2)))
        theta = math.atan2(sgn*(math.sin(theta1) - s*math.sin(theta2)),
                            sgn*(math.cos(theta1) - s*math.cos(theta2)))
        return logcomplex(logz=complex(logr, theta))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if not isinstance(other, logcomplex):
            try:
                z2 = complex(other)
            except Exception:
                return NotImplemented
            other = logcomplex(z2)
        return logcomplex(logz=self._logz + other._logz)

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if not isinstance(other, logcomplex):
            try:
                z2 = complex(other)
            except Exception:
                return NotImplemented
            other = logcomplex(z2)
        return logcomplex(logz=self._logz - other._logz)

    def __rtruediv__(self, other):
        # invself is 1/self.
        invself = logcomplex(logz=-self._logz)
        return invself*other

    def __pow__(self, other):
        p = self._logz * complex(other)
        return logcomplex(logz=complex(p.real, math.remainder(p.imag, math.tau)))

    def __rpow__(self, other):
        if isinstance(other, logcomplex):
            log_other = other._logz
        else:
            log_other = cmath.log(complex(other)) 
        p = complex(self)*log_other
        return logcomplex(logz=complex(p.real, math.remainder(p.imag, math.tau)))

    def __abs__(self):
        return math.exp(self._logz.real)

    def __complex__(self):
        return cmath.exp(self._logz)

    def __bool__(self):
        return self._logz.real != -math.inf

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Attributes and methods.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @property
    def real(self):
        return math.exp(self._logz.real)*math.cos(self._logz.imag)

    @property
    def imag(self):
        return math.exp(self._logz.real)*math.sin(self._logz.imag)

    def conjugate(self):
        return logcomplex(logz=self._logz.conjugate())
