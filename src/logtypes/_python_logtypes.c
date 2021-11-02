//
//  Create the Python types logfloat and logcomplex.
//
//  These types represent float and complex values, but
//  internally the log of the value is stored.
//
//  Note that "logfloat" uses "float" in the same sense
//  as Python (and not as in C).  The underlying values
//  use 64 bit floating point.
//
//  Requires C99.
//

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

//#include <complex.h>
#include <math.h>

//
// C functions for adding and subtracting log-based `double` values.
//


static double
log_no_fp_error(double value)
{
    if (value < 0.0) {
        return NAN;
    }
    if (value == 0.0) {
        return -INFINITY;
    }
    return log(value);
}

//
// Compute log(exp(log1) + exp(log2))
//
static double
logaddexp(double log1, double log2)
{
    return ((log1 > log2) ? log1 : log2) + log1p(exp(-fabs(log2 - log1)));
}

//
// Compute log(exp(log1) - exp(log2))
//
// if log2 > log1, nan is returned.
//
static double
logsubexp(double log1, double log2)
{
    if (log1 < log2) {
        return NAN;
    }
    if (log1 == log2) {
        return -INFINITY;
    }
    return log1 + log1p(-exp(log2 - log1));
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// Create the Python type logfloat
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

typedef struct {
    PyObject_HEAD
    double log;  // The natural log of the value.
} PyLogFloat;

// Forward declaration.
static PyTypeObject PyLogFloat_Type;

static inline int
PyLogFloat_Check(PyObject* object) {
    return PyObject_IsInstance(object, (PyObject*) &PyLogFloat_Type);
}


// Utility function.
// On return *perror is 0 on success, or -1 on error.
static double
get_log_from_object(PyObject *o, int *perror)
{
    double value;

    *perror = 0;

    if (PyLogFloat_Check(o)) {
        return ((PyLogFloat *) o)->log;
    }
    value = PyFloat_AsDouble(o);
    if (value == -1.0 && PyErr_Occurred()) {
        *perror = -1;
        return -1.0;
    }
    return log_no_fp_error(value);
}


static PyObject*
PyLogFloat_from_log(double value) {
    PyLogFloat *p = (PyLogFloat *) PyLogFloat_Type.tp_alloc(&PyLogFloat_Type, 0);
    if (p) {
        p->log = value;
    }
    return (PyObject*) p;
}


static int
PyLogFloat_init(PyLogFloat *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"", "log", NULL};
    PyObject *arg = NULL;
    PyObject *logobj = NULL;
    double argvalue;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O$O", kwlist,
                                     &arg, &logobj)) {
        return -1;
    }

    if (arg != NULL && logobj != NULL) {
        PyErr_SetString(PyExc_TypeError,
                        "either a positional argument or the log keyword can "
                        "be given, but not both");
        return -1;
    }

    if (arg == NULL && logobj == NULL) {
        // No arguments given.  Since float() returns 0 and complex()
        // returns 0j, we'll set self->log to the "value" of log(0),
        // which is -inf.
        self->log = -INFINITY;
        return 0;
    }

    if (logobj != NULL) {
        // Got the keyword parameter log=value
        self->log = PyFloat_AsDouble(logobj);
        if (self->log == -1.0 && PyErr_Occurred()) {
            return -1;
        }
        return 0;
    }

    // Got a single positional argument.
    if (PyLogFloat_Check(arg)) {
        self->log = ((PyLogFloat *) arg)->log;
        return 0;
    }

    argvalue = PyFloat_AsDouble(arg);
    if (argvalue == -1.0 && PyErr_Occurred()) {
        return -1;
    }
    self->log = log(argvalue);
    return 0;
}

static PyObject*
PyLogFloat_str(PyObject* self)
{
    PyObject *obj;
    char *log_str = PyOS_double_to_string(((PyLogFloat *) self)->log, 'r',
                                          0, 0, NULL);
    if (log_str == NULL) {
        return NULL;
    }
    obj = PyUnicode_FromFormat("logfloat(log=%s)", log_str);
    PyMem_Free(log_str);
    return obj;
}

static Py_hash_t
PyLogFloat_hash(PyObject* self)
{
    Py_hash_t h = (Py_hash_t) ((PyLogFloat *) self)->log;
    /* Never return the special error value -1 */
    return h == -1 ? 2 : h;
}

static int
PyLogFloat_nb_bool(PyLogFloat *o) {
    return (o->log != -INFINITY);
}

static PyObject *
PyLogFloat_float(PyLogFloat *o) {
    return PyFloat_FromDouble(exp(o->log));
}

static PyObject *
PyLogFloat_long(PyLogFloat *o) {
    return PyLong_FromDouble(exp(o->log));
}

//
// Python number protocol: unary methods
//

static PyObject *
PyLogFloat_nb_negative(PyLogFloat *o)
{
    PyErr_SetString(PyExc_ValueError,
                    "math domain error; can't negate a logfloat instance");
    return NULL;
}


static PyObject *
PyLogFloat_nb_positive(PyLogFloat *o) {
    Py_INCREF(o);
    return (PyObject *) o;
}


static PyObject *
PyLogFloat_nb_absolute(PyLogFloat *o) {
    Py_INCREF(o);
    return (PyObject *) o;
}


static PyObject*
PyLogFloat_richcompare(PyObject* a, PyObject* b, int op)
{
    double b_log;

    if (PyLogFloat_Check(b)) {
        b_log = ((PyLogFloat *) b)->log;
    }
    else {
        double b_value;
        b_value = PyFloat_AsDouble(b);
        if (b_value == -1.0 && PyErr_Occurred()) {
            return NULL;
        }
        if (b_value < 0.0) {
            Py_RETURN_RICHCOMPARE(0.0, b_value, op);
        }
        if (b_value == 0.0) {
            b_log = -INFINITY;
        }
        else {
            b_log = log(b_value);
        }
    }
    Py_RETURN_RICHCOMPARE(((PyLogFloat *) a)->log, b_log, op);
}


//
// Python number protocol: binary methods
//

static PyObject *
PyLogFloat_nb_add(PyObject *o1, PyObject *o2)
{
    double log1, log2;
    int error;

    // Ensure that o1 is a PyLogFloat instance.
    if (PyLogFloat_Check(o2)) {
        PyObject *tmp = o1;
        o1 = o2;
        o2 = tmp;
    }
    log1 = ((PyLogFloat *) o1)->log;
    log2 = get_log_from_object(o2, &error);
    if (error == -1) {
        return NULL;
    }
    return (PyObject *) PyLogFloat_from_log(logaddexp(log1, log2));
}


static PyObject *
PyLogFloat_nb_subtract(PyObject *o1, PyObject *o2)
{
    double log1, log2, logdiff;
    int error;

    log1 = get_log_from_object(o1, &error);
    if (error == -1) {
        return NULL;
    }
    log2 = get_log_from_object(o2, &error);
    if (error == -1) {
        return NULL;
    }
    // XXX Check for log1 or log2 being nan or -inf.

    if (log1 < log2) {
        PyErr_SetString(PyExc_ValueError,
                        "math domain error: can't subtract a larger logfloat "
                        "value from a smaller one");
        return NULL;
    }
    logdiff = logsubexp(log1, log2);
    return (PyObject *) PyLogFloat_from_log(logdiff);
}


static PyObject *
PyLogFloat_nb_multiply(PyObject *o1, PyObject *o2)
{
    double log1, log2;
    int error;

    log1 = get_log_from_object(o1, &error);
    if (error == -1) {
        return NULL;
    }
    log2 = get_log_from_object(o2, &error);
    if (error == -1) {
        return NULL;
    }
    // XXX Check for log1 or log2 being nan or -inf.
    return (PyObject *) PyLogFloat_from_log(log1 + log2);
}

static PyObject *
PyLogFloat_nb_true_divide(PyObject *o1, PyObject *o2)
{
    double log1, log2;
    int error;

    log1 = get_log_from_object(o1, &error);
    if (error == -1) {
        return NULL;
    }
    log2 = get_log_from_object(o2, &error);
    if (error == -1) {
        return NULL;
    }
    // XXX Check for log1 or log2 being nan or -inf.
    return (PyObject *) PyLogFloat_from_log(log1 - log2);
}


// XXX o3 is unused!  This is the 'mod' parameter.
static PyObject *
PyLogFloat_nb_power(PyObject *o1, PyObject *o2, PyObject *o3)
{
    double log1, value2;
    int error;

    log1 = get_log_from_object(o1, &error);
    if (error == -1) {
        return NULL;
    }
    value2 = PyFloat_AsDouble(o2);
    if (value2 == -1.0 && PyErr_Occurred()) {
        return NULL;
    }
    // XXX Check for log1 or value2 being nan or -inf.
    return (PyObject *) PyLogFloat_from_log(value2*log1);
}


//
// Attributes and methods
//

PyObject *PyLogFloat_get_real(PyObject* self, void *ignore)
{
    Py_INCREF(self);
    return self;
}

PyObject *PyLogFloat_get_imag(PyObject* self, void *ignore)
{
    return PyFloat_FromDouble(0.0);
}

PyObject *PyLogFloat_get_log(PyObject* self, void *ignore)
{
    return PyFloat_FromDouble(((PyLogFloat *)self)->log);
}

// The attributes are read-only.

static PyGetSetDef PyLogFloat_getset[] = {
    {"real", PyLogFloat_get_real, NULL, "real part", NULL},
    {"imag", PyLogFloat_get_imag, NULL, "imaginary part", NULL},
    {"log", PyLogFloat_get_log, NULL, "natural log of the number", NULL},
    {NULL}, // Sentinel
};

static PyObject *
PyLogFloat_conj(PyLogFloat *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self);
    return (PyObject *) self;
}


static PyMethodDef PyLogFloat_methods[] = {
    {"conjugate", (PyCFunction) PyLogFloat_conj, METH_NOARGS, "complex conjugate"},
    {NULL}  /* Sentinel */
};


//
// Python number protocol methods for logfloat.
//
static PyNumberMethods PyLogFloat_as_number = {
    .nb_negative     = (unaryfunc) PyLogFloat_nb_negative,
    .nb_positive     = (unaryfunc) PyLogFloat_nb_positive,
    .nb_absolute     = (unaryfunc) PyLogFloat_nb_absolute,
    .nb_bool         = (inquiry) PyLogFloat_nb_bool,
    .nb_float        = (unaryfunc) PyLogFloat_float,
    .nb_int          = (unaryfunc) PyLogFloat_long,
    .nb_add          = PyLogFloat_nb_add,
    .nb_subtract     = PyLogFloat_nb_subtract,
    .nb_multiply     = PyLogFloat_nb_multiply,
    .nb_true_divide  = PyLogFloat_nb_true_divide,
    .nb_power        = PyLogFloat_nb_power,
};

#define DOC_LOGFLOAT "logfloat type (TODO: finish this docstring)"

//
// Python type object for logfloat.
//
static PyTypeObject PyLogFloat_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name        = "logfloat",
    .tp_doc         = DOC_LOGFLOAT,
    .tp_basicsize   = sizeof(PyLogFloat),
    .tp_repr        = PyLogFloat_str,
    .tp_as_number   = &PyLogFloat_as_number,
    .tp_hash        = PyLogFloat_hash,
    .tp_str         = PyLogFloat_str,
    .tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_richcompare = PyLogFloat_richcompare,
    .tp_init        = (initproc) PyLogFloat_init,
    .tp_new         = PyType_GenericNew,
    .tp_getset      = PyLogFloat_getset,
    .tp_methods     = PyLogFloat_methods
};

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// Python extension module definition.
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

PyMethodDef module_methods[] = {
    {0} // sentinel
};

static struct PyModuleDef moduledef = {
    .m_base     = PyModuleDef_HEAD_INIT,
    .m_name     = "_python_logtypes",
    .m_doc      = "Module that defines the logfloat object",
    .m_size     = -1,
    .m_methods  = module_methods,  // XXX Not needed?
};


PyMODINIT_FUNC
PyInit__python_logtypes(void)
{
    PyObject *module;

    if (PyType_Ready(&PyLogFloat_Type) < 0) {
        return NULL;
    }

    module = PyModule_Create(&moduledef);
    if (module == NULL) {
        return NULL;
    }

    Py_INCREF(&PyLogFloat_Type);
    if (PyModule_AddObject(module, "logfloat", (PyObject*) &PyLogFloat_Type) < 0) {
        Py_DECREF(&PyLogFloat_Type);
        Py_DECREF(module);
        return NULL;
    };

    return module;
}
