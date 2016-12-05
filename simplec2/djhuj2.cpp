/* #include "djhuj.h" */
//#include "C:/Program Files (x86)/Graphviz2.38/include/graphviz/gvc.h"
#include "graphviz/gvc.h"

int puk(int i) {
    return i + 36;
}

void bduk() {
    Agraph_t *ag;
    ag = (Agraph_t*)agopen("test",  Agdirected, 0);
}