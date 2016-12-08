#include <Python.h>
#include <math.h>

//#define PY3

//The Structure:
typedef struct Point {
    double x,y;
} Point;

double distance(Point *p1, Point *p2) {
    return hypot(p1->x - p2->x, p1->y - p2->y);
}

/* Utility functions */
static Point *PyPoint_AsPoint(PyObject *obj) {
    return (Point *) PyCapsule_GetPointer(obj, "Point");
}

static PyObject *PyPoint_FromPoint(Point *p, int must_free) {
    return PyCapsule_New(p, "Point", NULL);
//    return PyCapsule_New(p, "Point", must_free ? del_Point : NULL);
}

/* Create a new Point object */
static PyObject *py_Point(PyObject *self, PyObject *args) {
    Point *p;
    double x,y;
    if (!PyArg_ParseTuple(args,"dd",&x,&y)) {
        return NULL;
    }
    p = (Point *) malloc(sizeof(Point));
    p->x = x;
    p->y = y;
    return PyPoint_FromPoint(p, 1);
}

static PyObject *py_distance(PyObject *self, PyObject *args) {
    Point *p1, *p2;
    PyObject *py_p1, *py_p2;
    double result;
    if (!PyArg_ParseTuple(args,"OO",&py_p1, &py_p2)) {
        return NULL;
    }
    if (!(p1 = PyPoint_AsPoint(py_p1))) {
        return NULL;
    }
    if (!(p2 = PyPoint_AsPoint(py_p2))) {
        return NULL;
    }
    result = distance(p1,p2);
    return Py_BuildValue("d", result);
}

/* Methods registration */
static PyMethodDef module_methods[] = {
    {"Point", py_Point, METH_VARARGS, "Create new Point"},
    {"distance", py_distance, METH_VARARGS, "Calculates distance"},
    {NULL, NULL, 0, NULL}
};

/* New to Python 3: module description structure */
#ifdef PY3
    static struct PyModuleDef thismodule = {
       PyModuleDef_HEAD_INIT,
       "pointsample",          /* name of module */
       module_docstring, /* module documentation, may be NULL */
       -1,               /* size of per-interpreter state of the module, */
                      /* or -1 if the module keeps state in global variables. */
       module_methods
    };
#endif

/* When Python imports a C module named 'X' it loads the module */
/* then looks for a method named "PyInit_"+X and calls it.  Hence */
/* for the module "djhuj" the initialization function is */
/* "PyInit_djhuj".  The PyMODINIT_FUNC helps with portability */
/* across operating systems and between C and C++ compilers */
PyMODINIT_FUNC
#ifdef PY3
    /* For Python 3*/
    PyInit_pointsample(void)
#else
    /* For Python 2 */
    initpointsample(void)
#endif
{
#ifdef PY3
    return PyModule_Create(&thismodule);
#else
    (void) Py_InitModule3("pointsample", module_methods, "Capsule pointers demo");
#endif
}
