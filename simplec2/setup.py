from distutils.core import setup, Extension

# build_ext --inplace

setup(
    name='djhuj2',
    ext_modules=[Extension("djhuj2",
                           ["_djhuj2.cpp", "djhuj2.cpp"],
                           define_macros=[('GVDLL', None)],
# http://stackoverflow.com/questions/2885750/difficulties-getting-graphviz-working-as-a-library-in-c
                           include_dirs=['C://Program Files (x86)//Graphviz2.38//include'],
                           library_dirs=['C://Program Files (x86)//Graphviz2.38//lib//release//lib'],
                           libraries=["cdt", "cgraph"],
                           )
                 ]

    # include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
