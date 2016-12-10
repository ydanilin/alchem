#include <stdio.h>     // for printf
#include <iostream>    // cout
#include <Python.h>
/* Make sure the path to Graghviz include library is on your system path
   "C:/Program Files (x86)/Graphviz2.38/include" */
#include "graphviz/gvc.h"
#include "graphviz/types.h"

/* Extension procedure is slightly different for Py2 and Py3 so uncomment
   the following #define for Py3 */
#define PY3

#define MODULE_NAME "gvzpassage"
#define MODULEINIT_PY3(NAME) PyInit_ ## NAME(void)
#define MODULEINIT_PY2(NAME) init ## NAME(void)

/* non-exposed procedures */
static Agraph_t *retrieve_graph(PyObject *obj) {
    return (Agraph_t *) PyCapsule_GetPointer(obj, "Agraph");
}

static Agnode_t *retrieve_node(PyObject *obj) {
    return (Agnode_t *) PyCapsule_GetPointer(obj, "Agnode");
}

static Agedge_t *retrieve_edge(PyObject *obj) {
    return (Agedge_t *) PyCapsule_GetPointer(obj, "Agedge");
}

/* core procedures here */
static PyObject *wrap_agraphnew(PyObject *self, PyObject *args, PyObject *kwargs) {
    Agraph_t *ag;
    char* name;
    static char* kwlist[] = {"name", "directed", NULL};
    int directed = 0;
    Agdesc_t gtype;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|b", kwlist, &name, &directed))
        return NULL;
    gtype = Agstrictdirected;
    /* Shitty bug: all Agdesc_t variables are THE SAME...
       therefore will set individual bits manually */
    if (directed == 1) {
        gtype.directed = 1;}
    else {
        gtype.directed = 0;}
    ag = agopen(name, gtype, 0);
    return PyCapsule_New(ag, "Agraph", NULL);
}

static PyObject *wrap_addNode(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    char* label;
    Agraph_t* ag;
    Agnode_t* node;
    if (!PyArg_ParseTuple(args, "Os", &gra_ptr, &label)) {
        return NULL;
    }
    if (!(ag = retrieve_graph(gra_ptr))) {
        return NULL;
    }
    node = agnode(ag, label, 1);
    return PyCapsule_New(node, "Agnode", NULL);
}

static PyObject *wrap_addEdge(PyObject *self, PyObject *args, PyObject *kwargs) {
    PyObject* gra_ptr;
    PyObject* node1_ptr;
    PyObject* node2_ptr;
    char* label = "";
    Agraph_t* ag;
    Agnode_t* node1;
    Agnode_t* node2;
    Agedge_t* edge;
    static char* kwlist[] = {"graph", "node1", "node2", "label", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OOO|s", kwlist, &gra_ptr, &node1_ptr, &node2_ptr, &label))
        return NULL;
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    if (!(node1 = retrieve_node(node1_ptr)))
        return NULL;
    if (!(node2 = retrieve_node(node2_ptr)))
        return NULL;
    edge = agedge(ag, node1, node2, label, 1);
    return PyCapsule_New(edge, "Agedge", NULL);
}

static PyObject *wrap_layout(PyObject *self, PyObject *args) {
    PyObject* gra_ptr;
    Agraph_t* ag;
    GVC_t *gvc;
    if (!PyArg_ParseTuple(args, "O", &gra_ptr))
        return NULL;
    if (!(ag = retrieve_graph(gra_ptr)))
        return NULL;
    gvc = gvContext();
    gvLayout(gvc, ag, "dot");
    boxf bbox = GD_bb(ag);
    double LLx = bbox.LL.x;
    double LLy = bbox.LL.y;
    double URx = bbox.UR.x;
    double URy = bbox.UR.y;
    return Py_BuildValue("{sdsdsdsd}", "LLx", LLx,
                                       "LLy", LLy,
                                       "URx", URx,
                                       "URy", URy);
}

static PyObject *node_geometry(PyObject *self, PyObject *args) {
    PyObject* node_ptr;
    Agnode_t* node;
    if (!PyArg_ParseTuple(args, "O", &node_ptr)) {
        return NULL;
    }
    if (!(node = retrieve_node(node_ptr))) {
        return NULL;
    }
    pointf center = ND_coord(node);
    double x = center.x;
    double y = center.y;
    double width = ND_width(node);
    double height = ND_height(node);
    char* shape = ND_shape(node)->name;
    return Py_BuildValue("{sdsdsdsdss}", "centerX", x,
                                       "centerY", y,
                                       "width", width,
                                       "height", height,
                                       "shape", shape);
}

static PyObject *edge_geometry(PyObject *self, PyObject *args) {
    PyObject* edge_ptr;
    Agedge_t* edge;
    if (!PyArg_ParseTuple(args, "O", &edge_ptr)) {
        return NULL;
    }
    if (!(edge = retrieve_edge(edge_ptr))) {
        return NULL;
    }
    splines* splines = ED_spl(edge);
    printf("Amount of Splines: %d\n", splines->size);
    bezier* list = splines->list;
    bezier spline = list[0];
    printf("Spline index 0 details:\n");
    printf("Sflag: %d\n", spline.sflag);
    printf("Eflag: %d\n", spline.eflag);
    printf("Has %d points\n", spline.size);
    pointf tochka1 = spline.list[0];
    pointf arrowtip1 = spline.sp;
    pointf tochka2 = spline.list[spline.size-1];
    pointf arrowtip2 = spline.ep;
    printf("Start point edge(x,y): (%f, %f)\n", tochka1.x, tochka1.y);
    printf("Start point arrowtip(x,y): (%f, %f)\n", arrowtip1.x, arrowtip1.y);
    printf("End point edge(x,y): (%f, %f)\n", tochka2.x, tochka2.y);
    printf("End point arrowtip(x,y): (%f, %f)\n", arrowtip2.x, arrowtip2.y);
    Py_RETURN_NONE;
}

/* Methods registration */
static PyMethodDef module_methods[] = {
    {"agraphNew", (PyCFunction)wrap_agraphnew, METH_VARARGS | METH_KEYWORDS, "Creates new Agraph"},
    {"addNode", wrap_addNode, METH_VARARGS, "Add a new node"},
    {"addEdge", (PyCFunction)wrap_addEdge, METH_VARARGS | METH_KEYWORDS, "Add a new edge"},
    {"layout", wrap_layout, METH_VARARGS, "Create layout"},
    {"node_geometry", node_geometry, METH_VARARGS, "Gets node geometry after layout"},
    {"edge_geometry", edge_geometry, METH_VARARGS, "Gets edge geometry after layout"},
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
     initgvzpassage(void)
#endif
{
#ifdef PY3
    return PyModule_Create(&thismodule);
#else
    (void) Py_InitModule3(MODULE_NAME, module_methods, "Capsule pointers demo");
#endif
}