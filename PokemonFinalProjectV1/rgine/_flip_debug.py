import os
import sys
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(path))

__DEBUG__ = b'\x00'
with open(path+os.sep+"__DEBUG__", "rb") as f:
    __DEBUG__ = f.read(1)[0]
if input("Current DEBUG Status: %s \nEnter 'c' To Change ... \n"%str(bool(__DEBUG__))).lower() == 'c':
    with open(path+os.sep+"__DEBUG__", "wb") as f:
        f.write(bytes([1-__DEBUG__]))

    print("Previous DEBUG Status: %s "%str(bool(__DEBUG__)))
    input("Current DEBUG Status: %s \n"%str(bool(1-__DEBUG__)))
