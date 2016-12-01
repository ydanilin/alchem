from pydbg import *
from pydbg.defines import *
import os
import struct
# installing pydbg:
# http://www.securityaddicted.com/tag/pydbg/
# the article:
# https://www.htbridge.com/blog/how_to_use_pydbg_as_a_powerful_multitasking_debugger.html
# also:
# http://2006.recon.cx/en/f/pamini-five-finger.pdf
# http://reverseengineering.stackexchange.com/questions/13761/getting-pydbg-working-on-windows-10


os.system('CLS')
dbg = pydbg()
target_process = 'acrobat.exe'
pid_is_there = False

print('[+] Observing CreateFile(A-W)')

def handler_CreateFileW(dbg):
    Filename = ''
    addr_FilePointer = dbg.read_process_memory(dbg.context.Esp + 0x4, 4)
    addr_FilePointer = struct.unpack('<L', addr_FilePointer)[0]
    Filename = dbg.smart_dereference(addr_FilePointer, True)
    print('CreateFileW -> {0}'.format(Filename))
    return DBG_CONTINUE

def handler_CreateFileA(dbg):
    offset = 0
    buffer_FileA = ''
    addr_buffer_data = dbg.read_process_memory(dbg.context.Esp + 0x4, 4)
    addr_buffer_data = struct.unpack('<L', addr_buffer_data)[0]
    buffer_FileA = dbg.smart_dereference(addr_buffer_data, True)
    print('CreateFileA -> {0}'.format(buffer_FileA))
    return DBG_CONTINUE

for (pid, name) in dbg.enumerate_processes():
    # print(name.lower())
    if name.lower() == target_process:
        pid_is_there = True
        print('Attaching to the process {0}'.format(target_process))
        dbg.attach(pid)
        function2 = 'CreateFileW'
        function3 = 'CreateFileA'
        CreateFileW = dbg.func_resolve_debuggee('kernel32.dll', 'CreateFileW')
        CreateFileA = dbg.func_resolve_debuggee('kernel32.dll', 'CreateFileA')
        print('[+] resolving {0} @ {1}08x'.format(function2, CreateFileW))
        print('[+] resolving {0} @ {1}08x'.format(function3, CreateFileA))
        dbg.bp_set(CreateFileA, description='CreateFileA',
                   handler=handler_CreateFileA)
        dbg.bp_set(CreateFileW, description='CreateFileW',
                   handler=handler_CreateFileW)
        dbg.debug_event_loop()

if not pid_is_there:
    print('Process {0} not found'.format(target_process))
