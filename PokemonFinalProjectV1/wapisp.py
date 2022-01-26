#wapisp.py
'''
WindowsAPIs Support Package (WAPISP)/(WSP)

'''
import ctypes
user32 = ctypes.windll.LoadLibrary("user32.dll")
kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
shell32 = ctypes.windll.LoadLibrary("shell32.dll")
comdlg32 = ctypes.windll.LoadLibrary("comdlg32.dll")
gdi32 = ctypes.windll.LoadLibrary("gdi32.dll")
from ctypes.wintypes import *
import struct


#define sys
NULL            =   0
PM_REMOVE       =   1
HWND_TOPMOST    =   -1
HWND_NOTOPMOST  =   -2
HWND_BOTTOM     =   1
HWND_TOP        =   0
SWP_NOSIZE      =   0x0001
SWP_NOMOVE      =   0x0002
WM_CREATE       =   0x0001
WM_KILLFOCUS    =   0x0008
WM_COMMAND      =   0x0111
WM_SYSCOMMAND   =   0x0112
WM_CLOSE        =   0x0010
WM_SIZE         =   0x0005
WM_PAINT        =   0x000F
WM_LBUTTONDOWN  =   0x0201
WM_LBUTTONUP    =   0x0202
WM_RBUTTONDOWN  =   0x0204
WM_RBUTTONUP    =   0x0205
WM_MOUSEWHEEL   =   0x020A
MK_SHIFT        =   0x0004
MK_CONTROL      =   0x0008
CS_DBLCLKS      =   0x0008
GCL_STYLE       =   -26
WM_LBUTTONDBLCLK=   0x0203
WM_MBUTTONDBLCLK=   0x0209
WM_RBUTTONDBLCLK=   0x0206
WM_NULL         =   0x0000
WM_INITDIALOG   =   0x0110
EM_SETSEL       =   0x00B1
WindowProc      =   ctypes.WINFUNCTYPE(ctypes.c_int,HWND,ctypes.c_uint,WPARAM,LPARAM)
WNDPROC         =   WindowProc
CB_ADDSTRING    =   0x0143
CB_SETCURSEL    =   0x014E
CBN_SELCHANGE   =   1
CB_GETCURSEL    =   0x0147
CB_GETLBTEXT    =   0x0148
BM_GETCHECK     =   0x00F0
BST_UNCHECKED   =   0x0000
BST_CHECKED     =   0x0001
BST_INDETERMINATE=  0x0002
MF_BYCOMMAND    =   0x00000000
MF_BYPOSITION   =   0x00000400
MF_DISABLED     =   0x00000002
MF_ENABLED      =   0x00000000
MF_GREYED       =   0x00000001
CS_HREDRAW      =   0x0002
CS_VREDRAW      =   0x0001
CS_OWNDC        =   0x0020
WS_EX_LAYERED   =   0x00080000
LWA_ALPHA       =   0x00000002
STM_SETIMAGE    =   0x0172
IMAGE_BITMAP    =   0

#Window Styles
WS_BORDER = 0x00800000
WS_CAPTION = 0x00C00000
WS_CHILD = 0x40000000
WS_CHILDWINDOW = 0x40000000
WS_CLIPCHILDREN = 0x02000000
WS_CLIPSIBLINGS = 0x04000000
WS_DISABLED = 0x08000000
WS_DLGFRAME = 0x00400000
WS_GROUP = 0x00020000
WS_HSCROLL = 0x00100000
WS_ICONIC = 0x20000000
WS_MAXIMIZE = 0x01000000
WS_MAXIMIZEBOX = 0x00010000
WS_MINIMIZE = 0x20000000
WS_MINIMIZEBOX = 0x00020000
WS_OVERLAPPED = 0x00000000
WS_SIZEBOX = 0x00040000
WS_SYSMENU = 0x00080000
WS_TABSTOP = 0x00010000
WS_THICKFRAME = 0x00040000
WS_TILED = 0x00000000
WS_POPUP = 0x80000000
WS_VISIBLE = 0x10000000
WS_VSCROLL = 0x00200000
WS_OVERLAPPEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX
WS_POPUPWINDOW = WS_POPUP | WS_BORDER | WS_SYSMENU
WS_TILEDWINDOW = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_THICKFRAME | WS_MINIMIZEBOX | WS_MAXIMIZEBOX

#Scroll Bar Control Styles
SBS_HORZ        =   0
SBS_VERT        =   1
SBS_BOTTOMALIGN =   4
SBS_LEFTALIGN   =   2
SBS_RIGHTALIGN  =   4
SBS_TOPALIGN    =   2

#SW_FLAGS
SW_FORCEMINIMIZE=   11
SW_HIDE         =   0
SW_MAXIMIZE     =   3
SW_MINIMIZE     =   6
SW_RESTORE      =   9
SW_SHOW         =   5
SW_SHOWDEFAULT  =   10
SW_SHOWMAXIMIZED=   3
SW_SHOWMINIMIZED=   2
SW_SHOWMINNOACTIVE= 7
SW_SHOWNA       =   8
SW_SHOWNOACTIVATE=  4
SW_SHOWNORMAL   =   1

#VK
VK_CAPITAL      =   0x14
VK_SHIFT        =   0x10

#MB
IDOK            =   1
IDCANCEL        =   2
IDABORT         =   3
IDRETRY         =   4
IDIGNORE        =   5
IDYES           =   6
IDNO            =   7
IDTRYAGAIN      =   10
IDCONTINUE      =   11
MB_OK           =   0x00000000
MB_OKCANCEL     =   0x00000001
MB_ABORTRETRYIGNORE=0x00000002
MB_YESNOCANCEL  =   0x00000003
MB_YESNO        =   0x00000004
MB_RETRYCANCEL  =   0x00000005
MB_CANCELTRYCONTINUE=0x00000006
MB_HELP         =   0x00004000

#define
INI_CLIENT      =   0x0400
MP_RESERVERD    =   [0x0400,0xffff]

class CHOOSECOLOR(ctypes.Structure):
	_fields_ = [("lStructSize", ctypes.c_ulong),
				("hwndOwner", ctypes.c_ulong),
				("hInstance", ctypes.c_ulong),
				("rgbResult",ctypes.c_uint),
				("lpCustColors",ctypes.c_wchar_p),
				("Flags",ctypes.c_ulong),
				("lCustData",ctypes.c_void_p),
				("lpfnHook",ctypes.c_void_p),
				("lpTemplateName",ctypes.c_void_p),
				]

##class KEYBDINPUT(ctypes.Structure):
##    _fields_ = [("wVK", WORD), 
##                ("wScan", WORD), 
##                ("dwFlags", DWORD),
##                ("time", DWORD),
##                ("dwExtraInfo",LPVOID),
##                ]
##
##class INPUT(ctypes.Structure):
##    _fields_ = [("type", DWORD), 
##                ("typ", WORD), 
##                ]
##    
def COLORREF(r, g, b):
	r &= 0xFF
	g &= 0xFF
	b &= 0xFF
	return (b << 16) | (g << 8) | r

def RGB(COLORREF_VALUE):
	color = str(bin(COLORREF_VALUE))[2:]
	while len(color)<24:
		color = "0"+color
	output = [[]for i in range(3)]
	for i in range(3):
		for t in range(8):
			output[i] = output[i]+[color[t]]
		color = color[8:]
	b="".join(output[0])
	g="".join(output[1])
	r="".join(output[2])
	return int(r, 2), int(g, 2), int(b, 2)


CC_ANYCOLOR     =   0x00000100
CC_ENABLEHOOK   =   0x00000010
CC_ENABLETEMPLATE=  0x00000020
CC_ENABLETEMPLATEHANDLE=0x00000040
CC_FULLOPEN     =   0x00000002
CC_PREVENTFULLOPEN= 0x00000004
CC_RGBINIT      =   0x00000001
CC_SHOWHELP     =   0x00000008
CC_SOLIDCOLOR   =   0x00000080

class OPENFILENAMEW(ctypes.Structure):  #three hours
	_fields_ = [("lStructSize", ctypes.c_ulong),
				("hwndOwner", ctypes.c_void_p),
				("hInstance", ctypes.c_void_p),
				("lpstrFilter",ctypes.c_wchar_p),
				("lpstrCustomFilter", ctypes.c_void_p),
				("nMaxCustFilter", ctypes.c_ulong),
				("nFilterIndex", ctypes.c_ulong),
				("lpstrFile", ctypes.c_wchar_p),
				("nMaxFile", ctypes.c_long),
				("lpstrFileTitle", ctypes.c_void_p),
				("nMaxFileTitle", ctypes.c_ulong),
				("lpstrInitialDir", ctypes.c_void_p),
				("lpstrTitle", ctypes.c_void_p),
				("Flags", ctypes.c_ulong),
				("nFileOffset", ctypes.c_ushort),
				("nFileExtension", ctypes.c_ushort),
				("lpstrDefExt", ctypes.c_void_p),
				("lCustData", ctypes.c_void_p),
				("lpfnHook", ctypes.c_void_p),
				("lpTemplateName", ctypes.c_void_p),
				("pvReserved", ctypes.c_void_p),
				("dwReserved", ctypes.c_ulong),
				("FlagsEx", ctypes.c_ulong),
				]

#OFN
OFN_FILEMUSTEXIST=  0x00001000
OFN_PATHMUSTEXIST=  0x00000800
OFN_EXPLORER    =   0x00080000
OFN_HIDEREADONLY=   0x00000004

class RECT(ctypes.Structure):
	_fields_ = [("left",ctypes.c_long),
				("top",ctypes.c_long),
				("right",ctypes.c_long),
				("bottom",ctypes.c_long),
				]

class RECTL(ctypes.Structure):
	_fields_ = [("left",ctypes.c_long),
				("top",ctypes.c_long),
				("right",ctypes.c_long),
				("bottom",ctypes.c_long),
				]

class POINT(ctypes.Structure):
	_fields_ = [("x",ctypes.c_long),
				("y",ctypes.c_long)
				]

class WNDCLASSEX(ctypes.Structure):
	_fields_ = [("cbSize", ctypes.c_uint),
				("style", ctypes.c_uint),
				("lpfnWndProc", WindowProc),
				("cbClsExtra", ctypes.c_int),
				("cbWndExtra", ctypes.c_int),
				("hInstance", HANDLE),
				("hIcon", HANDLE),
				("hCursor", HANDLE),
				("hBrush", HANDLE),
				("lpszMenuName", LPCWSTR),
				("lpszClassName", LPCWSTR),
				("hIconSm", HANDLE)
				]

class BITMAPINFO(ctypes.Structure):
	_fields_ = [("biSize", ctypes.c_ulong), #DWORD biSize
				("biWidth", ctypes.c_long), #LONG  biWidth
				("biHeight", ctypes.c_long), # LONG biHeight
				("biPlanes", ctypes.c_ushort), # WORD  biPlanes
				("biBitCount", ctypes.c_ushort), # WORD  biBitCount
				("biCompression", ctypes.c_ulong), #  DWORD biCompression
				("biSizeImage", ctypes.c_ulong), #  DWORD biSizeImage
				("biXPelsPerMeter", ctypes.c_long), #  LONG  biXPelsPerMeter
				("biYPelsPerMeter", ctypes.c_long), #  LONG  biYPelsPerMeter
				("biClrUsed", ctypes.c_ulong), #  DWORD biClrUsed
				("biClrImportant", ctypes.c_ulong), #  DWORD biClrImportant
				("biColors", ctypes.c_ulong), #  4byte colors array
				]

__version__ = "0.01a Beta"
__author__ = ['"Charles Chen" <chenchen.charles@yahoo.ca>']




##============================================================
def SetWindowPos(handle,HWNDFLAG,x,y,cx,cy,flag):
	user32.SetWindowPos(handle,HWNDFLAG,x,y,cx,cy,flag)


def PeekMessage(handle,ifremove=0,IF_EXACT_MOUS=True):  #NOT PASSING EXIT MESSAGE   #DO NOT USE IF POSSIBLE
	umsg = struct.pack("@5L2l",0,0,0,0,0,0,0)
	if user32.PeekMessageW(umsg, handle, NULL, NULL, ifremove) == 0: return 0, 0, 0, 0, 0  #WM_NULL
	a,message,wParam,lParam,e,f,g = struct.unpack("@5L2l", umsg)
	if IF_EXACT_MOUS:
		return (message,wParam,lParam)+MOUSPOSEXACT(handle,(f,g))
	return message, wParam, lParam, f, g


def GetMessage(handle,IF_STOP=False):  #PASS EXIT MESSAGE  #WHEN WM_CLOSE NOT FROM THE WINDOW, GETMESSAGE WILL PROCESS IT.  #USE IF POSSIBLE
	umsg = struct.pack("@5L2l",0,0,0,0,0,0,0)
	if not IF_STOP:
		if user32.PeekMessageW(umsg,handle,0,0,0):
			if user32.GetMessageW(umsg, handle, NULL, NULL) == 0: return WM_CLOSE, 0, 0, 0, 0
			a,message,wParam,lParam,e,f,g = struct.unpack("@5L2l", umsg)
			return message, wParam, lParam, f, g
		else: return 0, 0, 0, 0, 0
	else:
		if user32.GetMessageW(umsg, handle, NULL, NULL) == 0: return WM_CLOSE, 0, 0, 0, 0
		a,message,wParam,lParam,e,f,g = struct.unpack("@5L2l", umsg)
		return message, wParam, lParam, f, g


def GetCursorPos(handle,IF_EXACT_MOUS=True):
	upt = struct.pack("@2L", 0,0)
	if user32.GetCursorPos(upt)==0:
			raise SystemError("func: GetCursorPos fails")
	f,g = struct.unpack("@2L", upt)
	try:
		if IF_EXACT_MOUS:return MOUSPOSEXACT(handle,(f,g))
		else: return f, g
	except SystemError:
		return -1, -1


def MOUSPOSEXACT(handle,MousPOS):
	pt = ScreenToClient(handle,MousPOS)
	return pt.x, pt.y


def ScreenToClient(handle,GLOBALMOUSEPOS):
	x,y = GLOBALMOUSEPOS
	pt = POINT()
	pt.x = x
	pt.y = y
	if not user32.ScreenToClient(handle,ctypes.pointer(pt)):raise SystemError()
	else:return pt

def GetWindowRect(handle):
	urect = struct.pack("@4L", 0,0,0,0)
	if user32.GetWindowRect(handle,urect)==0:
			raise SystemError("func: GetWindowRect fails")
	a,b,c,d = struct.unpack("@4L", urect)
	return a, b, c, d


def GetClientRect(handle,IFRETURNCLASS=False):
	rect = RECT()
	if not user32.GetClientRect(handle,ctypes.pointer(rect)):raise SystemError()
	if IFRETURNCLASS:return rect
	return rect.left, rect.top, rect.right, rect.bottom


def ShowWindow(handle,SW_FLAG):
	user32.ShowWindow(handle,SW_FLAG)

def PostMessage(handle,message,wParam=NULL,lParam=NULL):
	if not isinstance(wParam,int) or not isinstance(lParam,int):
		raise ValueError("INT ONLY")
	if wParam>0xffffffff or lParam>0xffffffff:
		raise ValueError("Params: OUT OF RANGE")
	user32.PostMessageW(handle,message,wParam,lParam)
##============================================================
def GetHandle(TitleName,ClassName=NULL):
	return user32.FindWindowW(ClassName,TitleName)
def LoadLibrary(windll_name):
	hRes = kernel32.LoadLibraryW(windll_name)
	return hRes
def GetOpenFileName(handle,strFilter=None):
	'''
"type0def"+"\\x00"+"type0attr0;type0attr1..."+"\\x00"+...end:"\\x00\\x00"

	'''
	ofn = OPENFILENAMEW()
	ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW())
	ofn.hwndOwner = handle

	if strFilter is None:
		ofn.lpstrFilter = ctypes.c_wchar_p("All Files(*.*)"+'\x00'+"*.*"+'\x00\x00')
	else:
		ofn.lpstrFilter = ctypes.c_wchar_p(strFilter)

	output = ctypes.c_wchar_p('\x00'*256)
	ofn.lpstrFile = output
	ofn.nMaxFile = 255
	ofn.Flags = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_EXPLORER | OFN_HIDEREADONLY

	return comdlg32.GetOpenFileNameW(ctypes.pointer(ofn)), ctypes.wstring_at(output)


def GetSaveFileName(handle,strFilter=None):
	'''
"type0def"+"\\x00"+"type0attr0;type0attr1..."+"\\x00"+...end:"\\x00\\x00"

	'''
	ofn = OPENFILENAMEW()
	ofn.lStructSize = ctypes.sizeof(OPENFILENAMEW())
	ofn.hwndOwner = handle

	if strFilter is None:
		ofn.lpstrFilter = ctypes.c_wchar_p("All Files(*.*)"+'\x00'+"*.*"+'\x00\x00')
	else:
		ofn.lpstrFilter = ctypes.c_wchar_p(strFilter)

	output = ctypes.c_wchar_p('\x00'*256)
	ofn.lpstrFile = output
	ofn.nMaxFile = 255
	ofn.Flags = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_EXPLORER | OFN_HIDEREADONLY

	return comdlg32.GetSaveFileNameW(ctypes.pointer(ofn)), ctypes.wstring_at(output)


def LoadMenu(handle,hRes,res_id):
	hMenu = user32.LoadMenuW(hRes,res_id)
	user32.SetMenu(handle,hMenu)
	return hMenu
def ClearMenu(handle):
	user32.SetMenu(handle,0)
def DestroyMenu(handle,hMenu):
	user32.SetMenu(handle,0)
	user32.DestroyMenu(hMenu)
def EnableMenuItem(hmenu,iditem,status=MF_ENABLED):
	if user32.EnableMenuItem(hmenu,iditem,status) == -1:
		raise ValueError("ITEM NOT EXIST")
	else:return True
def DefWindowProc(handle,msg,wparam,lparam):
	return user32.DefWindowProcW(handle,msg,wparam,lparam)
def SetActiveWindow(handle):
	user32.SetActiveWindow(handle)
##============================================================
def GetCurrentThread():
	return kernel32.GetCurrentThread()
def TerminateThread(hThread):
	return kernel32.TerminateThread(hThread,0)
##============================================================
def ClipCursor(handle,Rect=NULL):#ltrb infunc
	if Rect== NULL:
		urect = struct.pack("@llll", 0,0,0,0)
		if user32.GetWindowRect(handle,urect)==0:
			raise SystemError("func: GetWindowRect fails")
		if not user32.ClipCursor(urect):raise SystemError("func: 'ClipCursor' fails")
	else:print ("RESERVED: Rect must be NULL(0)")
def CursorRelease(handle):
	return user32.ClipCursor(0)
##============================================================
def GetKeyState(VirtKey):
	gks = user32.GetKeyState(VirtKey)
	return gks
##============================================================
def ShellExecute(handle,Operation,FileAddress,ExecParameters,Directory,SW_flags):
	return shell32.ShellExecuteW(handle,Operation,FileAddress,ExecParameters,Directory,SW_flags)
def ShellOPEN(handle,FileAddress,ExecParameters=NULL,SW_flags=SW_SHOWNORMAL):
	return shell32.ShellExecuteW(handle,"open",FileAddress,ExecParameters,NULL,SW_flags)
##============================================================
def MessageBox(handle,text,caption,flags=MB_OK):
	'''
Please Check MSDN if you are not sure what the return values are.  
	'''
	return user32.MessageBoxW(handle,text,caption,flags)
##============================================================
def ChooseColor(handle,currentcolor):
	r,g,b = currentcolor
	cust = ctypes.c_wchar_p('\x00'*8)
	cc = CHOOSECOLOR(0,0,0,0,0,0,0,0,0)
	cc.lStructSize = ctypes.sizeof(cc)
	cc.hwndOwner = handle
	cc.rgbResult = COLORREF(r,g,b)
	cc.lpCustColors = cust
	cc.Flags = CC_ANYCOLOR|CC_FULLOPEN|CC_RGBINIT
	if comdlg32.ChooseColorW(ctypes.pointer(cc)):return RGB(cc.rgbResult)
	else: return -1, -1, -1


##============================================================
def GetClassLongPtr(handle,nIndex):     
	try:
		ret = user32.GetClassLongPtrW(handle,nIndex)
	except AttributeError:
		ret = user32.GetClassLongW(handle,nIndex)
	if not ret:raise SystemError()
	else:return ret
def SetClassLongPtr(handle,nIndex,newvalue,IFWARNING=True):         
	t = ctypes.c_long(newvalue)
	try:
		ret = user32.SetClassLongPtrW(handle,nIndex,t)
	except AttributeError:
		ret = user32.SetClassLongW(handle,nIndex,t)
	if not ret and IFWARNING:input("WARNING: SETCLASSLONGPTR IS RETURNING ZERO.  ")
	return ret
##============================================================
