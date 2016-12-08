from distutils.core import setup, Extension

# build_ext --inplace

setup(
    name='pointsample',
    ext_modules=[Extension("pointsample",
                           ["point.cpp"],
                           # libraries=["cdt", "cgraph", "gvc"],
                           )
                 ]
)
