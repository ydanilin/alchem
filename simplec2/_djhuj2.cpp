#include <Python.h>
#include "djhuj2.h"

#define PY3

static char module_docstring[] =
    "This module provides the famous djhuj function";
static char puk_docstring[] =
    "Returns arg + 36";

/* The wrapper to the underlying C function */
static PyObject *wrap_puk(PyObject *self, PyObject *args) {
    int i;
    if (!PyArg_ParseTuple(args, "i", &i))
        return NULL;
    int output = puk(i);
    PyObject *ret = Py_BuildValue("i", output);
    return ret;
}

static PyObject *wrap_bduk(PyObject *self, PyObject *args) {
    void* pointer;
    pointer = bduk();
    return PyCapsule_New(pointer, "Graph", NULL);
//    Py_RETURN_NONE;
}

static PyObject *wrap_attribut(PyObject *self, PyObject *args) {
    PyObject* py_ptr;
    void* gptr;
    if (!PyArg_ParseTuple(args, "O", &py_ptr))
        return NULL;
    gptr = (void *)PyCapsule_GetPointer(py_ptr, "Graph");
    attribut(gptr);
    Py_RETURN_NONE;
}

/* A list of all the methods defined by this module. */
/* "puk" is the name seen inside of Python */
/* "djhuj_puk" is the name of the C WRAPPER function handling the Python call */
/* "METH_VARGS" tells Python how to call the handler */
/* The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef module_methods[] = {
    {"puk", wrap_puk, METH_VARARGS, puk_docstring},
    {"bduk", wrap_bduk, METH_NOARGS, puk_docstring},
    {"attribut", wrap_attribut, METH_VARARGS, puk_docstring},
    {NULL, NULL, 0, NULL}
};

/* New to Python 3: module description structure */
#ifdef PY3
    static struct PyModuleDef thismodule = {
       PyModuleDef_HEAD_INIT,
       "djhuj2",          /* name of module */
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
    PyInit_djhuj2(void)
#else
    /* For Python 2 */
    initdjhuj2(void)
#endif
{
#ifdef PY3
    return PyModule_Create(&thismodule);
#else
    (void) Py_InitModule3("djhuj2", module_methods, module_docstring);
#endif
}
