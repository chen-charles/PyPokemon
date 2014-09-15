import os
import inspect
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
f = open(path+os.sep+"__DEBUG__", "rb")
__DEBUG__ = f.read(1)[0]
f.close()

if __DEBUG__:
	import common
else:
	import rgine.common as common

def _main():
	import os
	import platform

	def cls(): os.system("cls" if platform.system() == "Windows" else "clear")
	_help = '''For more information, see the documentation
BUMP		BUMP(name, value)
CLS		CLS()
CREATE		CREATE(name, value)
DELETE		DELETE(name)
EXIT		EXIT()
GET		GET(name)
HELP		HELP()'''

	print(".buildinfo Toolset\nBy Charles-Jianye Chen\n")
	while True:
		uin = input(".buildinfo->").lower()
		if uin == "":
			continue
		elif uin == "help":
			print(_help)
		elif uin == "exit":
			break
		elif uin == "get":
			name = input(".buildinfo->%s->name->"%uin)
			try:
				ver = (eval(uin)(name))
				print("Current %s Build -> "%name+str(common.raw2struct(ver, common.uint64).uint)+"\nRaw -> "+str(ver))
			except Exception: print("Exception")
		elif uin == "bump":
			name = input(".buildinfo->%s->name->"%uin)
			while 1:
				try:
					value = int(input(".buildinfo->%s->value->"%uin))
					break
				except ValueError: continue
			try:
				ver = (eval(uin)(name, value))
				print("Current %s Build -> "%name+str(common.raw2struct(ver, common.uint64).uint)+"\nRaw -> "+str(ver))
			except Exception: print("Exception")
		elif uin == "create":
			name = input(".buildinfo->%s->name->"%uin)
			while 1:
				try:
					value = int(input(".buildinfo->%s->value->"%uin))
					break
				except ValueError: continue
			try:
				ver = (eval(uin)(name, value))
				print("Current %s Build -> "%name+str(common.raw2struct(ver, common.uint64).uint)+"\nRaw -> "+str(ver))
			except Exception: print("Exception")
		elif uin == "delete":
			name = input(".buildinfo->%s->name->"%uin)
			if delete(name):
				print("%s deleted. ")
			else:
				print("Exception")
		elif uin == "cls":
			eval("%s"%uin)()
		else:
			print("'%s' is not recognized as an internal commend. "%uin)

		print()
	return 0

def get(name): return open(name+".buildinfo", "rb").read()

def bump(name, value):
	ver = common.raw2struct(get(name), common.uint64)
	ver.uint += value
	open(name+".buildinfo", "wb").write(common.struct2raw(ver))
	return common.struct2raw(ver)

def create(name, initvalue):
	ver = common.uint64(int(initvalue))
	open(name+".buildinfo", "wb").write(common.struct2raw(ver))
	return common.struct2raw(ver)

def delete(name):
	import os
	try:
		os.remove(name)
		return True
	except Exception:
		return False

if __name__ == "__main__": exit(_main())
