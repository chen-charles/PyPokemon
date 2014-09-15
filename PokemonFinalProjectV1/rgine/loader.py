import os
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
f = open(path+os.sep+"__DEBUG__", "rb")
__DEBUG__ = f.read(1)[0]
f.close()

if __DEBUG__:
	from common import *
else:
	from rgine.common import *

_kernel32 = ctypes.windll.kernel32
_shell32 = ctypes.windll.shell32

_NULL = 0
_SW_SHOWNORMAL = 1
def _ShellOPEN(handle, FileAddress, ExecParameters=_NULL, SW_flags=_SW_SHOWNORMAL):
	return _shell32.ShellExecuteW(handle, "open", FileAddress, ExecParameters, _NULL, SW_flags)

##_path = sys.path[0]
##if not _path: _path = sys.path[1]
_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_exec = _path+"/PgbarLoader.exe"

class Loader(object):
	def __init__(self, title, evt_name):
		self._released = False
		self._evt = evt_name
		self.title = title

	def init(self):
		if not self._released:
			self.release()

		_ShellOPEN(0, _exec, "%s %s"%(self.title.replace(" ", "\x1f"), self._evt))
		self._released = False

	def release(self):
		if not self._released:
			self._released = True
			hEvt = _kernel32.OpenEventA(2, 1, bytes(self._evt, "utf-8"))
			if not hEvt: return
			_kernel32.SetEvent(hEvt)
			_kernel32.CloseHandle(hEvt)

	def __del__(self):
		self.release()

if __name__ == "__main__":
	loader = Loader("Demo ...", "evtname")
	loader.init()
	input("Enter to exit ... ")
	loader.release()


