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


_logfmt = \
'''================================================================================
Level		: %s
Timestamp	: %d
Exc.Type    : %s
RuntimeMsg	: %s
Traceback	: %s
'''

_stackinfo = \
'''
	Stack %s
		fname		: %s
		lineno		: %s
		func		: %s
		codectx		: %s
		index		: %s

'''

class error(Exception):
	def __init__(self, msg, exception=Exception, e_level="Exception", c_context=10, logfile="Exception.log"):
		self.msg = msg
		stackinfo = []
		j = 0
		if not issubclass(exception, Exception): exception = Exception
		self._exception = exception
		try: c_context = int(c_context)
		except ValueError: c_context = 10
		stack = inspect.trace(c_context)
		try:
			for i in map(list, stack):
				i[4] = "\n"+"".join(list(map(lambda x: "\t"*5+x, i[4])))
				t = (str(j), ) + tuple(map(str, i[1:]))
				stackinfo.append(_stackinfo%t)
				j += 1
		except Exception:
			pass
		finally:
			del stack

		log(
			_logfmt%(str(e_level), getTimestamp(), exception.__name__, msg, "".join(stackinfo)),
			str(logfile),
		)

	def __str__(self): return self._exception.__name__ + ": " + self.msg

def _main(): raise error("An Exception Is Raised!", ValueError)
if __name__ == "__main__": exit(_main())
