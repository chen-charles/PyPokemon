import ctypes
import time
import inspect
import binascii
import os

getLine = (lambda:inspect.currentframe().f_back.f_lineno)
getName = (lambda:inspect.getfile(inspect.currentframe()))

def getTimestamp(): return int(time.time())

def log(logmsg, logfilename="log.log", rwtyp="a"):
	file = open(logfilename, rwtyp)
	file.write(str(logmsg))
	file.close()

def struct2raw(s):
	length  = ctypes.sizeof(s)
	p       = ctypes.cast(ctypes.pointer(s), ctypes.POINTER(ctypes.c_char * length))
	return p.contents.raw

def raw2struct(string, stype):
	if not issubclass(stype, ctypes.Structure): raise ValueError('The type of the structypes is not a ctypes.Structure')
	length      = ctypes.sizeof(stype)
	stream      = (ctypes.c_char * length)()
	stream.raw  = string
	p           = ctypes.cast(stream, ctypes.POINTER(stype))
	return p.contents

def byte2int(b):
	return b[0]

def byte2bool(b):
	if len(b) > 1: raise ValueError(b)
	result = 8*[False, ]
	b = bin(int(str(binascii.hexlify(b))[2:-1], 16))[2:]
	for i in range(len(b)): result[7-i] = bool(int(b[len(b)-1-i]))
	return result

def bool2byte(li):
	b = []
	for i in map(int, li):
		b.append(str(i))
	return bytes([int("".join(b), 2)])

def bool2int(li):
	b = bool2byte(li)
	return b[0]

def int2bool(i):
	return byte2bool(bytes([i]))

class byte(ctypes.Structure): _fields_ = [("byte", ctypes.c_byte)]
class uint16(ctypes.Structure): _fields_ = [("uint", ctypes.c_uint16)]
class uint32(ctypes.Structure): _fields_ = [("uint", ctypes.c_uint32)]
class uint64(ctypes.Structure): _fields_ = [("uint", ctypes.c_uint64)]
class uint(uint32): pass

def module_path(lambda_):
	fname = os.path.abspath(inspect.getsourcefile(lambda_))
	path = "/".join(fname.split("/")[:-1])
	if not path: path = "\\".join(fname.split("\\")[:-1])
	return path
