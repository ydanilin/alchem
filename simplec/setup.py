from distutils.core import setup, Extension

setup(
    name='djhuj',
    ext_modules=[Extension("djhuj", ["_djhuj.cpp", "djhuj.cpp"])]
    # include_dirs=numpy.distutils.misc_util.get_numpy_include_dirs(),
)
