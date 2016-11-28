#!/usr/bin/env python
import win32api  # needs to download pywin32
import ctypes
from ctypes import sizeof, c_ulong, c_int64, c_void_p

from ctypes.wintypes import BOOL
from ctypes.wintypes import HWND
from ctypes.wintypes import DWORD
from ctypes.wintypes import WORD
from ctypes.wintypes import LONG
from ctypes.wintypes import HKEY
from ctypes.wintypes import BYTE

from edid_parser1 import parse


# some details of the windows API differ between 32 and 64 bit systems..
def is_64bit():
    """Returns true when running on a 64 bit system"""
    return sizeof(c_ulong) != sizeof(c_void_p)


# ULONG_PTR is a an ordinary number, not a pointer and contrary to the name it
# is either 32 or 64 bits, depending on the type of windows...
# so test if this a 32 bit windows...
if is_64bit():
    # assume 64 bits
    ULONG_PTR = c_int64
else:
    # 32 bits
    ULONG_PTR = c_ulong


def ValidHandle(value, func, arguments):
    if value == 0:
        raise ctypes.WinError()
    return value


NULL = 0
HDEVINFO = ctypes.c_void_p
PCTSTR = ctypes.c_char_p
PDWORD = ctypes.POINTER(DWORD)
REGSAM = DWORD


class GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', DWORD),
        ('Data2', WORD),
        ('Data3', WORD),
        ('Data4', BYTE * 8),
    ]

    def __str__(self):
        return "{%08x-%04x-%04x-%s-%s}" % (
            self.Data1,
            self.Data2,
            self.Data3,
            ''.join(["%02x" % d for d in self.Data4[:2]]),
            ''.join(["%02x" % d for d in self.Data4[2:]]),
        )


class SP_DEVINFO_DATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', DWORD),
        ('ClassGuid', GUID),
        ('DevInst', DWORD),
        ('Reserved', ULONG_PTR),
    ]

    def __str__(self):
        return "ClassGuid:%s DevInst:%s" % (self.ClassGuid, self.DevInst)


PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)

setupapi = ctypes.windll.LoadLibrary("setupapi")

SetupDiClassGuidsFromName = setupapi.SetupDiClassGuidsFromNameA
SetupDiClassGuidsFromName.argtypes = [PCTSTR, ctypes.POINTER(GUID), DWORD,
                                      PDWORD]
SetupDiClassGuidsFromName.restype = BOOL

SetupDiGetClassDevs = setupapi.SetupDiGetClassDevsA
SetupDiGetClassDevs.argtypes = [ctypes.POINTER(GUID), PCTSTR, HWND, DWORD]
SetupDiGetClassDevs.restype = HDEVINFO
SetupDiGetClassDevs.errcheck = ValidHandle

SetupDiEnumDeviceInfo = setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.argtypes = [HDEVINFO, DWORD, PSP_DEVINFO_DATA]
SetupDiEnumDeviceInfo.restype = BOOL

SetupDiOpenDevRegKey = setupapi.SetupDiOpenDevRegKey
SetupDiOpenDevRegKey.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD,
                                 DWORD, REGSAM]
SetupDiOpenDevRegKey.restype = HKEY

SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
SetupDiDestroyDeviceInfoList.restype = BOOL

advapi32 = ctypes.windll.LoadLibrary("Advapi32")
RegCloseKey = advapi32.RegCloseKey
RegCloseKey.argtypes = [HKEY]
RegCloseKey.restype = LONG

DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
DICS_FLAG_GLOBAL = 1
DIREG_DEV = 0x00000001
KEY_READ = 0x20019

GUIDs = (GUID * 8)()  # so far only seen one used, so hope 8 are enough...
guids_size = DWORD()
# first argument is PCTSTR that should NOT be UNICODE. So, for Py3 compatibility
# where all strings are Unicode we need to pass bytes object
# bytes are specially designed to pass strict Ascii strings to other systems
if not SetupDiClassGuidsFromName(
        'Monitor'.encode('ascii'),
        GUIDs,
        ctypes.sizeof(GUIDs),
        ctypes.byref(guids_size)):
    raise ctypes.WinError()

for g in GUIDs:
    print(g)

# device information set handle
g_hdi = SetupDiGetClassDevs(
    ctypes.byref(GUIDs[0]),
    None,
    NULL,
    DIGCF_PRESENT)  # was DIGCF_PRESENT|DIGCF_DEVICEINTERFACE which misses CDC ports

print(g_hdi)

devinfo = SP_DEVINFO_DATA()
devinfo.cbSize = ctypes.sizeof(devinfo)

# device index 0 from device information set handle
SetupDiEnumDeviceInfo(g_hdi, 0, ctypes.byref(devinfo))
# returns the structure with class GUID with an index (instance)
# in the device information set
print(devinfo)

# handle for an open registry key with EDID
hkey = SetupDiOpenDevRegKey(
    g_hdi,
    ctypes.byref(devinfo),
    DICS_FLAG_GLOBAL,
    0,
    DIREG_DEV,  # DIREG_DRV for SW info
    KEY_READ)

print('hkey: ', hkey)

# ZDESS !!!
huj = win32api.RegEnumValue(hkey, 0)

RegCloseKey(hkey)
SetupDiDestroyDeviceInfoList(g_hdi)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print(parse(bytearray(huj[1])))
