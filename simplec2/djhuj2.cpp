/* #include "djhuj.h" */
//#include "C:/Program Files (x86)/Graphviz2.38/include/graphviz/gvc.h"
#include <stdio.h>     // for printf
#include <iostream>    // cout
#include <typeinfo>    // for 'typeid'
#include "graphviz/gvc.h"

int puk(int i) {
    return i + 36;
}



void* bduk() {
    GVC_t *gvc;
    Agraph_t *ag;
    Agnode_t *node1;
    Agnode_t *node2;
    Agedge_t *edge;
//    char * neim;
    #ifndef WITH_CGRAPH
        aginit();
    #else
        printf("With CGRAPH!\n");
    #endif

    gvc = gvContext();

    ag = agopen("test",  Agdirected, 0);
    printf("Agraph instantiated\n");
    std::cout << typeid(ag).name() << std::endl;
    std::cout << sizeof(*ag) << std::endl;

    node1 = agnode(ag, "huj1", 1);
    node2 = agnode(ag, "huj2", 1);
    edge = agedge(ag, node1, node2, 0, 1);
    std::cout << typeid(node1).name() << std::endl;
    std::cout << sizeof(*node1) << std::endl;


    gvLayout(gvc, ag, "dot");

//    neim = agget(ag, "bb");
//    attribut(ag);

//    std::cout << typeid(*neim).name() << std::endl;
//    std::cout << sizeof(*neim) << std::endl;
//    printf("%s\n", neim);

    agwrite(ag, stdout);

    int cnt;
    Agsym_t *attr;
    cnt = 0; attr = 0;
    while (attr = agnxtattr(ag, AGNODE, attr)) cnt++;
        printf("The graph %s has %d attributes\n",agnameof(ag),cnt);
    return ag;

//    agclose(ag);
//    printf("Agraph closed");
}

void attribut(void* gra) {
    Agraph_t* ag;
    char* neim;
    ag = (Agraph_t*)gra;
    neim = agget(ag, "bb");
    printf("Output from attribut(): %s\n", neim);
    agwrite(ag, stdout);
}