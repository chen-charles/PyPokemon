import os
import sys
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(path))


try:
    f = open(path+os.sep+"__DEBUG__", "wb")
    f.write(b'\x00')
    f.close()
    from rgine.exception import *
except:
    f = open(path+os.sep+"__DEBUG__", "wb")
    f.write(b'\x01')
    f.close()
    from exception import *

__DEBUG__ = b'\x00'
with open(path+os.sep+"__DEBUG__", "rb") as f:
    __DEBUG__ = f.read(1)[0]

if __DEBUG__:
    from exception import *
    from event import *
    from terrain import *
    from progressbar import *
    from world import *
    from loader import *
    import buildinfo
    import windows
    import surface_buffer
else:
    from rgine.exception import *
    from rgine.event import *
    from rgine.terrain import *
    from rgine.progressbar import *
    from rgine.world import *
    from rgine.loader import *
    import rgine.buildinfo as buildinfo
    import rgine.windows as windows
    import rgine.surface_buffer as surface_buffer
    
__version__ = buildinfo.get(path+"/__init__")
__author__ = 'Charles-Jianye Chen'
sys.path.pop(0)
