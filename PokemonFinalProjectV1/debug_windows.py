__author__ = 'Charles-Jianye Chen'
from rgine.windows import *
import rgine

pygame.init()
screen = pygame.display.set_mode((800, 600))
wm = WindowsManager((800, 600))
def init(self, hWnd):   #init
	print("Hello World! From hWnd: %d" % hWnd)
	self._handle = hWnd
	self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)

def cb(self, event, uMsg):  #callback
	self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
	# if uMsg == WindowsMacros.WM_SETFOCUS or uMsg == WindowsMacros.WM_KILLFOCUS:
	# 	print("In Loop: ", uMsg, self._handle)
	# if self._handle == 10 and self._wm.isWindowPresent(11):
	# 	print("In Loop: XXX", event.getMousePos(), self._wm.getInstance(11).getRect())
	for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
		self._bk_.blit(surface, pos)
	# if self._handle == 11:
	# 	# print(self._frame._frame_args["frameMessage"])
	# 	# print(self._frame._frame_args["state"], self._frame._frame_args["frameMessage"], 11)
	# 	# pass
	# 	# print(event.getMousePos()[0]+1, event.getMousePos()[1]+16, self.getAbsoluteClientRect(), self.getRect())
	# else:
	# 	print(self._frame._frame_args["state"], self._frame._frame_args["frameMessage"], 10)
	# 	# print(event.getMousePos()[0]+1, event.getMousePos()[1]+16, self.getAbsoluteClientRect(), self.getRect(), end="")
	return True

def rd(self):   #render
	return self._bk_

def getMsg(self):
	return 0

def rel(self):  #release
	self._wm.Release()

surf = pygame.Surface((200, 200), pygame.SRCALPHA)
surf.fill((128, 128, 128, 256*2//3))
hwnd0 = wm.CreateWindow(wm.RegisterClass(True, init, cb, rd, getMsg, rel), ((200, 200), surf, "this is 0",
											  pygame.font.SysFont('Times New Romen', 16),
											  True, (255, 255, 255)))
t = wm.getInstance(hwnd0)._wm.CreateWindow(
	wm.getInstance(hwnd0)._wm.RegisterClass(True, init, cb, rd, getMsg, rel), ((200, 200), surf,
                                                                                             "this is 0x"))
wm.getInstance(hwnd0)._wm.DestroyWindow(t)
wm.getInstance(hwnd0)._wm.CreateWindow(
	wm.getInstance(hwnd0)._wm.RegisterClass(True, init, cb, rd, getMsg, rel), ((100, 100), surf,
                                                                                             "this is 0x"))
running = True
evt = rgine.Event()
while running:

	evt.update()

	if evt.type == pygame.QUIT:
		running = False
	screen.fill((0, 0, 0))
	for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
		screen.blit(surface, pos)
	pygame.display.flip()


wm.Release()
pygame.quit()