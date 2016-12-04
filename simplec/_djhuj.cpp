#include <Python.h>
#include "djhuj.h"

static char module_docstring[] =
    "This module provides the famous djhuj function";
static char puk_docstring[] =
    "Returns arg + 36";

/* The wrapper to the underlying C function */
static PyObject *djhuj_puk(PyObject *self, PyObject *args) {
    int i;
    if (!PyArg_ParseTuple(args, "i", &i))
        return NULL;
    int output = puk(i);
    PyObject *ret = Py_BuildValue("i", output);
    return ret;
}
/* A list of all the methods defined by this module. */
/* "puk" is the name seen inside of Python */
/* "djhuj_puk" is the name of the C WRAPPER function handling the Python call */
/* "METH_VARGS" tells Python how to call the handler */
/* The {NULL, NULL} entry indicates the end of the method definitions */
static PyMethodDef module_methods[] = {
    {"puk", djhuj_puk, METH_VARARGS, puk_docstring},
    {NULL, NULL, 0, NULL}
};

/* New to Python 3: module description structure */
static struct PyModuleDef djhujmodule = {
   PyModuleDef_HEAD_INIT,
   "djhuj",   /* name of module */
   module_docstring, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   module_methods
};

/* When Python imports a C module named 'X' it loads the module */
/* then looks for a method named "PyInit_"+X and calls it.  Hence */
/* for the module "djhuj" the initialization function is */
/* "PyInit_djhuj".  The PyMODINIT_FUNC helps with portability */
/* across operating systems and between C and C++ compilers */
PyMODINIT_FUNC
PyInit_djhuj(void)
{
    /* New to Python 3: instead of calling Py_InitModule3 you must return: */
    return PyModule_Create(&djhujmodule);
}