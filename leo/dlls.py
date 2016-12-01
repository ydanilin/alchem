from ctypes import WinDLL, windll, CDLL
from ctypes.util import find_library

# liba = find_library('wpcap.dll')
# liba = WinDLL('wpcap.dll')
# liba = CDLL('wpcap.dll')
liba = windll.wpcap

puk = 1

