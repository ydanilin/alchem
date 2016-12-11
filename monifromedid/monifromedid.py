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

from edid_parser import EdidParser


class MoniFromEdid:
    """
    Unexpectedly, it is really pain in the ass to get true values of a display
    resolution. The reason is that easy-way solutions report false figures.
    Maybe that's because they were designed long time ago, in times there were
    800x600 or 1024x768 pixel monitors with a 4:3 ratio. Nowadays, with powerful
    1600x1200 or even 1920x1280 LCDs, these obsolete solutions lie because they
    cannot recognize the increased amount of pixels.
    I was wondered how difficult it turns now to retrieve true values. Seems
    like the only way to proceed is to get from OS the special structure
    provided by a display driver - Extended Display Identification Data (EDID).
    No big effort required to get this info on Unix-like systems - you just need
    to read some config file and that's it. But on Windows this is really
    (as usual) pain in the ass.
    It would seem that we only need to read the Registry, but it turned out that
    it is very difficult to obtain exact place, which registry entry we should
    read. You will see that complexity in a moment.
    Seems the only way to proceed is to deal with so called Setup API. Former
    century that was a service to install software packages. Now everybody is
    using Windows Installer technology for this, but Setup API is retained with
    Windows for installing device drivers. The procedure description follows.
    """

    def __init__(self):
        self.parser = EdidParser()
        # name aliases to respect winapi-style syntax
        self.NULL = 0
        self.HDEVINFO = ctypes.c_void_p
        self.PCTSTR = ctypes.c_char_p
        self.PDWORD = ctypes.POINTER(DWORD)
        self.REGSAM = DWORD
        # some details of the windows API differ between 32 and 64 bit systems..
        # ULONG_PTR is a an ordinary number, not a pointer and contrary to the
        # name it is either 32 or 64 bits, depending on the type of windows...
        # so test if this a 32 bit windows...
        if sizeof(c_ulong) != sizeof(c_void_p):
            # assume 64 bits
            self.ULONG_PTR = c_int64
        else:
            # 32 bits
            self.ULONG_PTR = c_ulong
        # some structures need to be passed to winapi calls
        self.GUID = type('GUID', (ctypes.Structure,),
                         dict(_fields_ = [('Data1', DWORD),
                                            ('Data2', WORD),
                                            ('Data3', WORD),
                                            ('Data4', BYTE * 8)]
                              )
                         )
        self.SP_DEVINFO_DATA = type('SP_DEVINFO_DATA', (ctypes.Structure,),
                                    dict(_fields_ = [('cbSize', DWORD),
                                                  ('ClassGuid', self.GUID),
                                                  ('DevInst', DWORD),
                                                  ('Reserved', self.ULONG_PTR)]
                                    )
                                    )
        self.PSP_DEVINFO_DATA = ctypes.POINTER(self.SP_DEVINFO_DATA)
        # setupapi DLL and registration of its functions needed
        self.setupapi = ctypes.windll.LoadLibrary("setupapi")
        # step 1 - get class GUID for 'Monitor' devices
        self.SetupDiClassGuidsFromName=self.setupapi.SetupDiClassGuidsFromNameA
        self.SetupDiClassGuidsFromName.argtypes = [self.PCTSTR,
                                                   ctypes.POINTER(self.GUID),
                                                   DWORD, self.PDWORD]
        self.SetupDiClassGuidsFromName.restype = BOOL
        # step 2 - obtain handle to a device information set
        self.SetupDiGetClassDevs = self.setupapi.SetupDiGetClassDevsA
        self.SetupDiGetClassDevs.argtypes = [ctypes.POINTER(self.GUID),
                                             self.PCTSTR, HWND, DWORD]
        self.SetupDiGetClassDevs.restype = self.HDEVINFO
        self.SetupDiGetClassDevs.errcheck = self.ValidHandle
        # step 3 - get structure that specifies a device information element
        # in a device information set
        self.SetupDiEnumDeviceInfo = self.setupapi.SetupDiEnumDeviceInfo
        self.SetupDiEnumDeviceInfo.argtypes = [self.HDEVINFO, DWORD,
                                               self.PSP_DEVINFO_DATA]
        self.SetupDiEnumDeviceInfo.restype = BOOL
        # step 4 - obtain ID for the registry key where EDID actually is
        self.SetupDiOpenDevRegKey = self.setupapi.SetupDiOpenDevRegKey
        self.SetupDiOpenDevRegKey.argtypes = [self.HDEVINFO,
                                              self.PSP_DEVINFO_DATA, DWORD,
                                              DWORD, DWORD, self.REGSAM]
        self.SetupDiOpenDevRegKey.restype = HKEY
        # garbage collection for device information
        self.SetupDiDestroyDeviceInfoList = \
            self.setupapi.SetupDiDestroyDeviceInfoList
        self.SetupDiDestroyDeviceInfoList.argtypes = [self.HDEVINFO]
        self.SetupDiDestroyDeviceInfoList.restype = BOOL
        # garbage collection for registry key
        self.advapi32 = ctypes.windll.LoadLibrary("Advapi32")
        self.RegCloseKey = self.advapi32.RegCloseKey
        self.RegCloseKey.argtypes = [HKEY]
        self.RegCloseKey.restype = LONG
        # misc constants for API functions
        self.DIGCF_PRESENT = 2  # for Step 2 function - to return only devices
        # that are currently present in a system
        self.DIGCF_DEVICEINTERFACE = 16
        # next constants are for step 4
        self.DICS_FLAG_GLOBAL = 1  # specifies that we need global
        # configuration information (not specific to a particular hardware
        # profile
        self.DIREG_DEV = 0x00000001  # Open a hardware key for the device
        self.KEY_READ = 0x20019      # need key for read-only mode

        self.GUIDs = (self.GUID * 8)()  # so far only seen one used, so hope
        # 8 are enough...
        self.guids_size = DWORD()

    def ValidHandle(self, value, func, arguments):
        if value == 0:
            raise ctypes.WinError()
        return value

    def getMonitorDimensions(self):
        """
        This is the key function which do stuff.
        Returns dict {'millimetersX', 'millimetersX', pixelX, pixelY}

        for Step 1, the first argument is PCTSTR that should NOT be UNICODE.
        So, for Py3 compatibility, where all strings are Unicode we need to
        pass bytes object. bytes are specially designed to pass plain Ascii
        strings to other systems
        """
        # step 1 - get class GUID
        if not self.SetupDiClassGuidsFromName(
                'Monitor'.encode('ascii'),
                self.GUIDs,
                ctypes.sizeof(self.GUIDs),
                ctypes.byref(self.guids_size)):
            raise ctypes.WinError()

        # step 2 - device information set handle
        g_hdi = self.SetupDiGetClassDevs(
            ctypes.byref(self.GUIDs[0]),
            None,
            self.NULL,
            self.DIGCF_PRESENT)

        # step 3
        devinfo = self.SP_DEVINFO_DATA()
        devinfo.cbSize = ctypes.sizeof(devinfo)
        # device index 0 from device information set handle
        self.SetupDiEnumDeviceInfo(g_hdi, 0, ctypes.byref(devinfo))

        # step 4 - handle for an open registry key with EDID
        hkey = self.SetupDiOpenDevRegKey(
            g_hdi,
            ctypes.byref(devinfo),
            self.DICS_FLAG_GLOBAL,  # global configuration information
            0,                      # current hardware profile should be opened
            self.DIREG_DEV,         # Open a hardware key for the device
            self.KEY_READ)          # need key for read-only mode

        # finally open the key value by handle
        edidTuple = win32api.RegEnumValue(hkey, 0)

        # now "garbage collection"
        self.RegCloseKey(hkey)
        self.SetupDiDestroyDeviceInfoList(g_hdi)

        # complicated process finished )))
        output = self.parser.parse(bytearray(edidTuple[1]))
        return {'millimetersX': output[0], 'millimetersY': output[1],
                'pixelX': output[2], 'pixelY': output[3]}


if __name__ == '__main__':
    edid = MoniFromEdid()
    moniDims = edid.getMonitorDimensions()
    print(moniDims)
