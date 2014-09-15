import pygame


class Event(object):

	MOUSE_LEFT = 1
	MOUSE_MIDDLE = 2
	MOUSE_RIGHT = 3
	MOUSE_SCROLL_UP = 4
	MOUSE_SCROLL_DOWN = 5

	def __init__(self):
		self.KEYDOWN = set()
		self.MOUSEDOWN = set()
		self.type = 0
		self.dict = {}
		self._pos = [0, 0]
		self._relpos = [0, 0]
		self._mousemotionX = 0
		self._mousemotionY = 0

	def update(self):
		evt = pygame.event.poll()
		if evt.type == pygame.MOUSEMOTION:
			tx, ty = pygame.mouse.get_rel()
			self._mousemotionX+=tx
			self._mousemotionY+=ty
			return self.update()
		if evt.type == pygame.KEYDOWN:
			self.KEYDOWN.add(evt.dict["key"])
		elif evt.type == pygame.KEYUP:
			try: self.KEYDOWN.remove(evt.dict["key"])
			except Exception: pass
		elif evt.type == pygame.MOUSEBUTTONDOWN:
			self.MOUSEDOWN.add(evt.dict["button"])
		elif evt.type == pygame.MOUSEBUTTONUP:
			try: self.MOUSEDOWN.remove(evt.dict["button"])
			except Exception: pass
		self.type = evt.type
		self.dict = evt.dict
		self._pos = list(pygame.mouse.get_pos())
		tx, ty = pygame.mouse.get_rel()
		self._relpos =[tx+self._mousemotionX, ty+self._mousemotionY]
		self._mousemotionX = self._mousemotionY = 0

	def shiftMousePos(self, x, y):
		self._pos[0] += x
		self._pos[1] += y

	def getMousePos(self):
		return self._pos

	def getMouseRel(self):
		return self._relpos

	def isKeyDown(self, key):
		"""
		Check if the specific key is down.
		:keycode key:
		:return bool:
		"""
		if key in self.KEYDOWN: return True
		return False

	def isKeyHit(self, key):
		"""
		Check if the specific key is hit.
		:keycode key:
		:return bool:
		"""
		if self.type == pygame.KEYDOWN and self.dict["key"] == key: return True
		return False

	def isKeyUp(self, key):
		if self.type == pygame.KEYUP and self.dict["key"] == key: return True
		return False

	def isMouseDown(self, key):
		"""
		Check if the specific key is down.
		:rgine.Event.MOUSE_CONSTANTS(int) key:
		:return bool:
		"""
		if key in self.MOUSEDOWN: return True
		return False

	def isMouseHit(self, key):
		"""
		Check if the specific key is hit.
		:rgine.Event.MOUSE_CONSTANTS(int) key:
		:return bool:
		"""
		if self.type == pygame.MOUSEBUTTONDOWN and self.dict["button"] == key: return True
		return False

	def isMouseUp(self, key):
		"""
		Check if the specific key is up.
		:rgine.Event.MOUSE_CONSTANTS(int) key:
		:return bool:
		"""
		if self.type == pygame.MOUSEBUTTONUP and self.dict["button"] == key: return True
		return False

def _main():
	pygame.display.set_mode((800, 600))
	evt = Event()

	import time
	t = time.clock()
	fps = 0

	while True:

		evt.update()

		#state/hit type use if->elif
		if evt.type == pygame.QUIT:
			break
		elif evt.isKeyHit("x"):
			print("x hit")

		#down type use if->if
		if evt.isKeyDown("x"):
			print("x down")

		pygame.display.flip()

		#fps checking 1s/print
		fps += 1
		if time.clock()-t >= 1:
			t = time.clock()
			print("fps=%d"%fps)
			fps = 0

	pygame.quit()
	return 0

if __name__ == "__main__": exit(_main())
