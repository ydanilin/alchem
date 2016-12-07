# coding=utf-8
import djhuj2

# build but not install:
# build_ext --inplace

# to make DLL instead of PYD:
# Developer command prompt for VS2015
# cl /LD pukdll.cpp

t = djhuj2.puk(100)
print(t)

ghandle = djhuj2.bduk()

# djhuj2.attribut(ghandle)
djhuj2.attribut(100)
# if ghandle:
#     print('HUJ')
    # print(type(ghandle))
