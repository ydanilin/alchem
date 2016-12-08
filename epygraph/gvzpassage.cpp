#include <stdio.h>     // for printf
#include <Python.h>
/* Make sure the path to Graghviz include library is on your system path
   "C:/Program Files (x86)/Graphviz2.38/include" */
#include "graphviz/gvc.h"

/* Extension procedure is slightly different for Py2 and Py3 so uncomment
   the following #define for Py3 */
#define PY3

#define MODULE_NAME "gvzpassage"
#define MODULEINIT_PY3(NAME) PyInit_ ## NAME(void)
#define MODULEINIT_PY2(NAME) init ## NAME(void)

/* core procedures here */

static PyObject *wrap_agraphnew(PyObject *self, PyObject *args, PyObject *kwargs) {
    char* name;
    static char* kwlist[] = {"name", "directed", NULL};
    int directed = 0;
    Agdesc_t gtype;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|b", kwlist, &name, &directed))
        return NULL;
    if (directed) {
        gtype = Agstrictdirected;}
    else {
        gtype = Agstrictundirected;}
    printf("The graph named %s has directed value of %d\n", name, directed);
    Py_RETURN_NONE;
}
//(PyCFunction)
/* Methods registration */
static PyMethodDef module_methods[] = {
    {"agraphNew", (PyCFunction)wrap_agraphnew, METH_VARARGS | METH_KEYWORDS, "Creates new Agraph"},
    {NULL, NULL, 0, NULL}
};

/* New to Python 3: module description structure */
#ifdef PY3
    static struct PyModuleDef thismodule = {
       PyModuleDef_HEAD_INIT,
       MODULE_NAME,          /* name of module */
       NULL, /* module documentation, may be NULL */
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
     PyInit_gvzpassage(void)
#else
    /* For Python 2 */
    // initpointsample(void)
    MODULEINIT_PY2(MODULE_NAME)
#endif
{
#ifdef PY3
    return PyModule_Create(&thismodule);
#else
    (void) Py_InitModule3(MODULE_NAME, module_methods, "Capsule pointers demo");
#endif
}