
    printf("1. structure Agstrictundirected\n");
    printf("   field directed: type %s, value %d\n", typeid(Agstrictundirected.directed).name(), Agstrictundirected.directed);
    printf("   field strict: type %s, value %d\n", typeid(Agstrictundirected.strict).name(), Agstrictundirected.strict);
    printf("   field no_loop: type %s, value %d\n", typeid(Agstrictundirected.no_loop).name(), Agstrictundirected.no_loop);
    printf("   field maingraph: type %s, value %d\n", typeid(Agstrictundirected.maingraph).name(), Agstrictundirected.maingraph);
    printf("   field flatlock: type %s, value %d\n", typeid(Agstrictundirected.flatlock).name(), Agstrictundirected.flatlock);
    printf("   field no_write: type %s, value %d\n", typeid(Agstrictundirected.no_write).name(), Agstrictundirected.no_write);
    printf("   field has_attrs: type %s, value %d\n", typeid(Agstrictundirected.has_attrs).name(), Agstrictundirected.has_attrs);
    printf("   field has_cmpnd: type %s, value %d\n", typeid(Agstrictundirected.has_cmpnd).name(), Agstrictundirected.has_cmpnd);

    printf("2. structure Agstrictdirected\n");
    printf("   field directed: type %s, value %d\n", typeid(Agstrictdirected.directed).name(), Agstrictdirected.directed);
    printf("   field strict: type %s, value %d\n", typeid(Agstrictdirected.strict).name(), Agstrictdirected.strict);
    printf("   field no_loop: type %s, value %d\n", typeid(Agstrictdirected.no_loop).name(), Agstrictdirected.no_loop);
    printf("   field maingraph: type %s, value %d\n", typeid(Agstrictdirected.maingraph).name(), Agstrictdirected.maingraph);
    printf("   field flatlock: type %s, value %d\n", typeid(Agstrictdirected.flatlock).name(), Agstrictdirected.flatlock);
    printf("   field no_write: type %s, value %d\n", typeid(Agstrictdirected.no_write).name(), Agstrictdirected.no_write);
    printf("   field has_attrs: type %s, value %d\n", typeid(Agstrictdirected.has_attrs).name(), Agstrictdirected.has_attrs);
    printf("   field has_cmpnd: type %s, value %d\n", typeid(Agstrictdirected.has_cmpnd).name(), Agstrictdirected.has_cmpnd);

    printf("3. structure Agundirected\n");
    printf("   field directed: type %s, value %d\n", typeid(Agundirected.directed).name(), Agundirected.directed);
    printf("   field strict: type %s, value %d\n", typeid(Agundirected.strict).name(), Agundirected.strict);
    printf("   field no_loop: type %s, value %d\n", typeid(Agundirected.no_loop).name(), Agundirected.no_loop);
    printf("   field maingraph: type %s, value %d\n", typeid(Agundirected.maingraph).name(), Agundirected.maingraph);
    printf("   field flatlock: type %s, value %d\n", typeid(Agundirected.flatlock).name(), Agundirected.flatlock);
    printf("   field no_write: type %s, value %d\n", typeid(Agundirected.no_write).name(), Agundirected.no_write);
    printf("   field has_attrs: type %s, value %d\n", typeid(Agundirected.has_attrs).name(), Agundirected.has_attrs);
    printf("   field has_cmpnd: type %s, value %d\n", typeid(Agundirected.has_cmpnd).name(), Agundirected.has_cmpnd);

    printf("4. structure Agdirected\n");
    printf("   field directed: type %s, value %d\n", typeid(Agdirected.directed).name(), Agdirected.directed);
    printf("   field strict: type %s, value %d\n", typeid(Agdirected.strict).name(), Agdirected.strict);
    printf("   field no_loop: type %s, value %d\n", typeid(Agdirected.no_loop).name(), Agdirected.no_loop);
    printf("   field maingraph: type %s, value %d\n", typeid(Agdirected.maingraph).name(), Agdirected.maingraph);
    printf("   field flatlock: type %s, value %d\n", typeid(Agdirected.flatlock).name(), Agdirected.flatlock);
    printf("   field no_write: type %s, value %d\n", typeid(Agdirected.no_write).name(), Agdirected.no_write);
    printf("   field has_attrs: type %s, value %d\n", typeid(Agdirected.has_attrs).name(), Agdirected.has_attrs);
    printf("   field has_cmpnd: type %s, value %d\n", typeid(Agdirected.has_cmpnd).name(), Agdirected.has_cmpnd);

    std::cout << typeid(Agstrictundirected.directed).name() << std::endl;
    std::cout << Agstrictundirected.directed << std::endl;

    printf("Retrieved Agraph has name %s, directed=%d, strict=%d, undir=%d\n", agnameof(ag), agisdirected(ag), agisstrict(ag), agisundirected(ag));

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
//    PyObject* dict = PyDict_New();

    PyObject* output = PyList_New(1);
    PyList_SET_ITEM(output, 0, Py_BuildValue("{sdsd}", "arrowtipX", arrowtip2.x,
                                                       "arrowtipY", arrowtip2.y));
//    Py_RETURN_NONE;
