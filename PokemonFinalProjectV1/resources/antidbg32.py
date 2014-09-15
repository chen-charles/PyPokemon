import ctypes as _ctypes
import ctypes.wintypes as _wintypes
_kernel32 = _ctypes.windll.kernel32
_pbDebuggerPresent = _wintypes.PBOOL(_ctypes.pointer(_ctypes.c_long(0)))
_hProcess = _kernel32.GetCurrentProcess()
if _kernel32.CheckRemoteDebuggerPresent(_hProcess, _pbDebuggerPresent):
    bResult = bool(_pbDebuggerPresent.contents.value)
else:
    raise SystemError()

print(bResult)
import inspect as _inspect
_bCall = _inspect.stack()
print(_bCall)