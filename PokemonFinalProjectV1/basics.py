import random
import string
import pygame

import rgine as rgine

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

def init_terrain(terrain_name, texture_name, is_display_mode_set=True, textureSize=32):
	terrain = rgine.Terrain("r", textureSize, textureSize)
	terrain.readTerrain(terrain_name)
	terrain.readTextureFromFile(texture_name)
	if is_display_mode_set: terrain.convert_alpha()
	return terrain

def test(property_byte, digit): # test terrain property byte
	return rgine.byte2bool(bytes([property_byte]))[digit]

def renderInitScene(screensize, pgbar):
	x, y = screensize
	screen = pygame.Surface(screensize, pygame.SRCALPHA)
	running = True
	while running:
		for evt in pygame.event.get():
			if evt.type == pygame.QUIT:
				running = False
		screen.fill ((0,0,0))
		progressbar = pgbar.render()
		sx, sy = progressbar.get_size()
		screen.blit(progressbar,((x-sx)//2,(y-sy)//3*2))
		pgbar.increase(1)
		if pgbar.get_pos() >= 125:
			pgbar.set_pos(int("-25"))
		yield screen

def approx(a, b):
	c = a-b
	if 0.99 <= c <= 1: return True
	if -1 <= c <= -0.99: return True
	return False


class pEvent(object):
	def __init__(self, *args):
		self._activated = False

	def init(self, evt, wm):
		"""
		Will be called right after this event is activated.
		Return False will remove the event, but the release method will NOT be called.
		:rgine.Event evt:
		:rgine.windows.WindowsManager wm:
		:return bool:
		"""
		return True

	def render(self, evt, wm):
		"""
		Render the scene, if surf is None, the event will be released.
		:rgine.Event evt:
		:rgine.windows.WindowsManager wm:
		:return pygame.Surface, tuple/list(pos):
		"""
		return None, (0, 0)

	def release(self, wm):
		"""
		Release all resources.
		Note that you are responsible for relasing created windows in WindowsManager
		:rgine.windows.WindowsManager wm:
		"""
		pass
	
	def isRunning(self):
		return self._activated

class NPC(pEvent):
	# npcs are events
	# using terrain pos ALL THE TIME
	# wm could render to screen directly
	def __init__(self, pos, res_walk):
		super(NPC, self).__init__()
		self._pos = pos
		self._res = res_walk
		self._dir = DOWN
		self._static_dir = False
		self.player = None

	def init(self, evt, wm):
		"""
		Prepare for the activation of this event, create windows objects.
		:rgine.Event evt:
		:rgine.windows.WindowsManager wm:
		:return bool:
		"""
		return True

	def render(self, evt, wm):
		"""
		Render the scene.
		Note that this function will be called anyways, you are responsible to figure out if the event is activated.
		:rgine.Event evt:
		:rgine.windows.WindowsManager wm:
		:return pygame.Surface, tuple/list(pos)(terrain pos):
		"""
		return self.render_scene()

	def release(self, wm):
		"""
		Prepare for the next activation of this event, cleanup.
		Note that you are responsible for destroying windows in WindowsManager
		:rgine.windows.WindowsManager wm:
		"""
		pass

	def setPlayer(self, player):
		self.player = player

	def hasEvent(self, x, y):
		if (x, y) == tuple(self._pos):
			return True
		return False

	def getPos(self):
		return self._pos

	def setPos(self, pos):
		self._pos = pos

	def setStaticDir(self, bStatic):
		self._static_dir = bool(bStatic)

	def chgDir(self, dir_val):
		if not self._static_dir: self._dir = dir_val

	def getDir(self):
		return self._dir

	def render_scene(self):
		if self._dir == DOWN:
			return self._res.front[1], self._pos
		elif self._dir == UP:
			return self._res.back[1], self._pos
		elif self._dir == LEFT:
			return self._res.left[1], self._pos
		elif self._dir == RIGHT:
			return self._res.right[1], self._pos
		raise ValueError(self._dir)
		

class NPC_Skeleton(NPC):
	wmacros = rgine.windows.WindowsMacros()

	def __init__(self, pos, res_walk):
		super(NPC_Skeleton, self).__init__(pos, res_walk)
		self._hWnds = {}

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			for i in self._hWnds:
				umsg = wm.getMsg(self._hWnds[i])
		return self.render_scene()

	def release(self, wm):
		for i in self._hWnds:
			wm.DestroyWindow(self._hWnds[i])
		self._hWnds = {}
		self._activated = False


class PlayerManager(object):
		def __init__(self, player, terrain, playerEvent, npcManager):
				self._player = player
				self._terrain = terrain
				self.playerEvent = playerEvent
				self.npcManager = npcManager
				self._evt = None
				self._wm = None
				self._battle_s = 0
				self._battle_rg = [0, 0]
				self._battle_nxt = 9999

		def testTerrain(self, x, y, digit):
				prpty = self._terrain.getProperty_s(x, y)
				if prpty is None: return False
				r = test(prpty, digit)
				if r:
						return True
				else:
						return False

		def isTerrainReachable(self, x, y):
				return self.testTerrain(x, y, 0)

		def isPlayerEvent(self, x, y):
				# r = self.testTerrain(x, y, 1)
				if (x, y) in self.playerEvent:
					return self.playerEvent[(x, y)]
				else:
					return False

		def isNpcEvent(self, x, y):
				if self.npcManager.isPresent((x, y)):
					return True
				else:
					return False

		def updateEvent(self, evt, wm):
				self._evt = evt
				self._wm = wm

		def update(self, x, y):
				# change direction
				self._player.chgDir_pos(x, y)
				self._player.normalize_pos()
				tx, ty = self._player.getPos()
				tx += x
				ty += y
				# tx, ty: if actually move, where do the player settle

				# Return: surface, pEvent, if walk

				if tx<0 or ty<0 or (not self.isTerrainReachable(int(tx), int(ty))):
					return self._player.render(self._evt), -1, False

				r = self.isNpcEvent(int(tx), int(ty))
				if r: return self._player.render(self._evt), -1, False

				r = self.isPlayerEvent(int(tx), int(ty))
				if r: return self._player.render(self._evt), r, False

				r = self._player.move(x, y)
				if r and self.testTerrain(int(tx), int(ty), 2): self._battle_s += 1
				return self._player.render(self._evt), -1, not r

		def getPlayer(self):
			return self._player

		def release(self):
			return self._player.release()

		def setTerrain(self, terrain):
			self._terrain = terrain

		def setBattleStepCount(self, li_range):
			self._battle_rg = li_range
			self._battle_nxt = random.randint(*self._battle_rg)

		def isBattleNeeded(self):
			if self._battle_s >= self._battle_nxt:
				self._battle_s = 0
				self._battle_nxt = random.randint(*self._battle_rg)
				return True
			else: return False


class NPCManager(object):
	# using terrain offsets
		def __init__(self):
			self.npcs = {}

		def new(self, x, y, obj):
			obj.setPos((x, y))
			self.npcs[obj.getPos()] = obj

		def update(self, terrainRect, uPos):
			for i in self.npcs:
				if terrainRect.collidepoint(*self.npcs[i].getPos()):
					if self.npcs[i].hasEvent(*uPos): yield self.npcs[i], True
					else: yield self.npcs[i], False

		def delete(self, obj):
			if obj.getPos() in self.npcs:
				del self.npcs[obj.getPos()]
				return True
			return False

		def isPresent(self, pos):
			if tuple(pos) in self.npcs: return True
			return False


class ConversationBox(rgine.windows.windowFramed):
	def init(self, hWnd):
		_button_size = self.wmacros.button_size[:]
		_button_size = list(map((lambda x: x//2), _button_size))
		self._text = self._args[4]
		self._text = list(map(str, self._text))
		self._text_indx = 0
		self.wmacros = rgine.windows.WindowsMacros()
		self._handle = hWnd
		self._state = [self._text_indx, len(self._text)]    # current_indx, total_indx
		self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
		x, y = self._size

		# Button and Text
		self._button0 = self._wm.CreateWindow(self.wmacros.WC_BUTTON,
											(_button_size, self.wmacros.button, "OK",
																				pygame.font.SysFont('Times New Romen', 16),
																				True, (255, 255, 255)), True)
		self._text0 = self._wm.CreateWindow(self.wmacros.WC_TEXT,
											((x-(x*2//10), y*6//10), None, self._text[self._text_indx],
																				pygame.font.SysFont('Times New Romen', 16),
																				True, (255, 255, 255)), True)

		self._wm.MoveWindow(self._button0, (x-_button_size[0])*9//10, (y-_button_size[1])*8//10)
		self._wm.MoveWindow(self._text0, x*1//10, y*1//10)
		# self._wm.SetTopmost(self._button0, True)
		self._wm.SetTopmost(self._button0, True)

	def callback_(self, event, uMsg):
		self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
		self._bk_.fill((150, 150, 150, 255//2))
		for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
			self._bk_.blit(surface, pos)
			if hWnd == self._button0:
				if msg == self.wmacros.HIT:
					self._text_indx += 1
					if self._text_indx == len(self._text):
						self._text_indx -= 1
						self._state = [self._text_indx+1, len(self._text)]
					else:
						self._state = [self._text_indx, len(self._text)]
					self._wm.DestroyWindow(self._text0)
					x, y = self._size
					self._text0 = self._wm.CreateWindow(self.wmacros.WC_TEXT,
								((x-(x*2//10), y*6//10), None, self._text[self._text_indx],
																			pygame.font.SysFont('Times New Romen', 16),
																			True, (255, 255, 255)), True)
					self._wm.MoveWindowToPos(self._text0, x*1//10, y*1//10)
					self._wm.SetTopmost(self._button0, True)

		return True

	def render_(self):
		return self._bk_

	def getMsg(self):
		return self._state

	def release(self):
		self._wm.Release()


class amtbox(rgine.windows.windowFramed):
	def __init__(self, *args):
		super(amtbox, self).__init__(*args)
		self._state = 0
		self._bk_ = None
		self.macros = rgine.windows.WindowsMacros()
		self._handle = 0
		self._editbox = 0

	def init(self, hWnd):
		self._state = 0
		self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
		self._handle = hWnd
		self._editbox = self._wm.CreateWindow(self.macros.WC_EDITBOX, ((100,50), None))
		self._wm.SetTopmost(self._editbox, True)

	def callback_(self, RgineEvent, uMsg):
		self._bk_.fill((0, 0, 0))
		for hWnd, uMsg, surface, pos in self._wm.DispatchMessage(RgineEvent):
			if hWnd == self._editbox and uMsg:
				lidel = []
				if uMsg[-1] == "\n":
					for i in range(len(uMsg)):
						if uMsg[i] not in string.digits:
							lidel.append(uMsg[i])
					for i in lidel:
						uMsg.remove(i)
					if not uMsg: uMsg = ["-1"]
					t = int("".join(uMsg))
					if t == 0: t = -1
					self._state = t
				elif uMsg[-1] == "\x1b":
					uMsg = ["-1"]
					t = int("".join(uMsg))
					if t == 0: t = -1
					self._state = t

				lidel = []
				for i in range(len(uMsg)):
					if uMsg[i] not in string.digits:
						lidel.append(uMsg[i])
				for i in lidel:
					uMsg.remove(i)

				surface = self._wm.getInstance(hWnd).refresh()  # re-render surface
			self._bk_.blit(surface, pos)
		return True

	def render_(self):
		return self._bk_

	def getMsg(self):
		return self._state


# playerEvent = {}    # pos(terrain)->tuple: pEvent/inh. class, init_args
# npcs = {}   # load these npcs before game starts
# 			# (x, y): npc_object
