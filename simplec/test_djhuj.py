# coding=utf-8
import ctypes
import djhuj


# Developer command prompt for VS2015
# cl /LD pukdll.cpp
ct_puk = ctypes.CDLL('pukdll.dll').puk
ct_puk.restype = ctypes.c_int
ct_puk.argtypes = [ctypes.c_int]

t = djhuj.puk(100)
print(t)

tt = ct_puk(100)
print(tt)
