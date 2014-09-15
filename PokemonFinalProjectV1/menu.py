from basics import *
from resources_loader import *
import time
__author__ = 'Charles-Jianye Chen'

class _MenuMain(NPC_Skeleton):
	# buttons->dict() id:text
	def __init__(self, buttons):
		super(_MenuMain, self).__init__((-1, -1), None)
		self._buttons = buttons

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			_button_size = self.wmacros.button_size[:]
			_button_size = list(map((lambda x: x//2), _button_size))
			buttons = self._buttons
			def init(self, hWnd):
				nonlocal buttons, _button_size
				self.wmacros = rgine.windows.WindowsMacros()
				self._handle = hWnd
				self._umsg = 0
				self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
				self._hWnds = dict()
				self._buttons = buttons

				cy = 0
				t = list(self._buttons.keys())
				t.sort()
				for i in t:
					self._hWnds[i] = self._wm.CreateWindow(self.wmacros.WC_BUTTON,
										(_button_size, self.wmacros.button, "%s"%self._buttons[i],
														pygame.font.SysFont('Times New Romen', 16),
														True, (255, 255, 255)), True)
					self._wm.MoveWindowToPos(self._hWnds[i], 0, cy)
					cy += _button_size[1]
				# self._wm.SetTopmost(-1, True)
				self._wm.SetTopmost(-1, False)

			def cb(self, event, uMsg):
				x, y, w, h = self.getRect()
				self._bk_ = pygame.Surface((w, h), pygame.SRCALPHA)
				self._bk_.fill((150, 150, 150, 255//2))
				for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
					self._bk_.blit(surface, pos)
					if msg == self.wmacros.HIT:
						for i in self._buttons:
							if hWnd == self._hWnds[i]:
								self._umsg = i
								break
				return True

			def rd(self):
				return self._bk_

			def getMsg(self):
				return self._umsg

			def rel(self):
				self._wm.Release()

			winsize = _button_size[0], _button_size[1]*len(self._buttons)
			self._hWnds["menu"] = wm.CreateWindow(
				wm.RegisterClass(False, init, cb, rd, getMsg, rel), (winsize, None))
			x, y = wm.screensize
			wm.MoveWindow(self._hWnds["menu"], x-_button_size[0], 0)
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			for i in self._hWnds:
				umsg = wm.getMsg(self._hWnds[i])
				if umsg != 0:
					self.release(wm)
					return umsg

		return False

class MenuManager(object):
	def __init__(self, buttons):
		if 0 in buttons: raise Warning("(int) 0 should not be found in buttons.keys()")
		self._mMain = _MenuMain(buttons)
		self._pEvents = {}
		self._runningEvt = None

	def register(self, bid, pEvent_inst):
		self._pEvents[bid] = pEvent_inst

	def register_dict(self, d_pEvent_inst):
		for i in d_pEvent_inst:
			self.register(i, d_pEvent_inst[i])

	def update(self, evt, wm, key=pygame.K_SPACE):
		if self._runningEvt is None:
			if evt.isKeyHit(key):
				if not self._mMain.isRunning(): self._mMain.init(evt, wm)
				else: self._mMain.release(wm)

			result = self._mMain.render(evt, wm)
			if result:
				r = self._pEvents[result].init(evt, wm)
				if r:
					self._runningEvt = result
					self.update(evt, wm, key)
			return None, None
		else:
			surf, pos = self._pEvents[self._runningEvt].render(evt, wm)
			if not surf:
				self._pEvents[self._runningEvt].release(wm)
				self._runningEvt = None
			return surf, pos

	def release(self, wm):
		if self._runningEvt is not None:
			self._pEvents[self._runningEvt].release(wm)
			self._runningEvt = None

	def isRunning(self):
		return self._mMain.isRunning()


import os
_img_uMe = None
Boulder_Badge = None
Cascade_Badge = None
Earth_Badge = None
Marsh_Badge = None
Rainbow_Badge = None
Soul_Badge = None
Thunder_Badge = None
Volcano_Badge = None
Boulder_Badge_Blank = None
Cascade_Badge_Blank = None
Earth_Badge_Blank = None
Marsh_Badge_Blank = None
Rainbow_Badge_Blank = None
Soul_Badge_Blank = None
Thunder_Badge_Blank= None
Volcano_Badge_Blank = None
_accp = ["Boulder_Badge", "Cascade_Badge", "Earth_Badge", "Marsh_Badge", "Rainbow_Badge", "Soul_Badge",
	 "Thunder_Badge", "Volcano_Badge"]

Ele= None
Fai=None
Wat=None
Psy=None
Poi=None
Fly=None
Gho=None
Gra=None
Dra=None
Dar=None
Bug=None
Fig=None
Nor=None
Fir=None
Ste=None
Roc=None
Gro=None
Ice=None

Caught=None
NotCaught=None
Template=None

def init_menu(d_buttons, d_pEvents):
		global _img_uMe
		global Boulder_Badge, Cascade_Badge, Earth_Badge, Marsh_Badge, Rainbow_Badge, Soul_Badge, Thunder_Badge, Volcano_Badge
		global Boulder_Badge_Blank, Cascade_Badge_Blank, Earth_Badge_Blank, Marsh_Badge_Blank, Rainbow_Badge_Blank, Soul_Badge_Blank, Thunder_Badge_Blank, Volcano_Badge_Blank
		global Ele, Fai, Wat, Psy, Poi, Fly, Gho, Gra, Dra, Dar, Bug, Fig, Nor, Fir, Ste, Gro, Ice, Roc
		global Template, Caught, NotCaught
		global SpriteBack
		r = MenuManager(d_buttons)
		r.register_dict(d_pEvents)
		_img_uMe = pygame.image.load(os.path.join("resources", "uMe.jpg")).convert_alpha()
		Boulder_Badge = pygame.image.load(os.path.join("resources", "badges", "Boulder_Badge.png")).convert_alpha()
		Cascade_Badge = pygame.image.load(os.path.join("resources", "badges", "Cascade_Badge.png")).convert_alpha()
		Earth_Badge = pygame.image.load(os.path.join("resources", "badges", "Earth_Badge.png")).convert_alpha()
		Marsh_Badge = pygame.image.load(os.path.join("resources", "badges", "Marsh_Badge.png")).convert_alpha()
		Rainbow_Badge = pygame.image.load(os.path.join("resources", "badges", "Rainbow_Badge.png")).convert_alpha()
		Soul_Badge = pygame.image.load(os.path.join("resources", "badges", "Soul_Badge.png")).convert_alpha()
		Thunder_Badge = pygame.image.load(os.path.join("resources", "badges", "Thunder_Badge.png")).convert_alpha()
		Volcano_Badge = pygame.image.load(os.path.join("resources", "badges", "Volcano_Badge.png")).convert_alpha()

		Boulder_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Boulder_Badge_Blank.png")).convert_alpha()
		Cascade_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Cascade_Badge_Blank.png")).convert_alpha()
		Earth_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Earth_Badge_Blank.png")).convert_alpha()
		Marsh_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Marsh_Badge_Blank.png")).convert_alpha()
		Rainbow_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Rainbow_Badge_Blank.png")).convert_alpha()
		Soul_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Soul_Badge_Blank.png")).convert_alpha()
		Thunder_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Thunder_Badge_Blank.png")).convert_alpha()
		Volcano_Badge_Blank = pygame.image.load(os.path.join("resources", "badges", "Volcano_Badge_Blank.png")).convert_alpha()

		Ele = pygame.image.load(os.path.join("resources", "PokedexPics", "Ele.png")).convert_alpha()
		Fai = pygame.image.load(os.path.join("resources", "PokedexPics", "Fai.png")).convert_alpha()
		Wat = pygame.image.load(os.path.join("resources", "PokedexPics", "Wat.png")).convert_alpha()
		Psy = pygame.image.load(os.path.join("resources", "PokedexPics", "Psy.png")).convert_alpha()
		Poi = pygame.image.load(os.path.join("resources", "PokedexPics", "Poi.png")).convert_alpha()
		Fly = pygame.image.load(os.path.join("resources", "PokedexPics", "Fly.png")).convert_alpha()
		Gho = pygame.image.load(os.path.join("resources", "PokedexPics", "Gho.png")).convert_alpha()
		Gra = pygame.image.load(os.path.join("resources", "PokedexPics", "Gra.png")).convert_alpha()
		Dra = pygame.image.load(os.path.join("resources", "PokedexPics", "Dra.png")).convert_alpha()
		Dar = pygame.image.load(os.path.join("resources", "PokedexPics", "Dar.png")).convert_alpha()
		Bug = pygame.image.load(os.path.join("resources", "PokedexPics", "Bug.png")).convert_alpha()
		Fig = pygame.image.load(os.path.join("resources", "PokedexPics", "Fig.png")).convert_alpha()
		Nor = pygame.image.load(os.path.join("resources", "PokedexPics", "Nor.png")).convert_alpha()
		Fir = pygame.image.load(os.path.join("resources", "PokedexPics", "Fir.png")).convert_alpha()
		Ste = pygame.image.load(os.path.join("resources", "PokedexPics", "Ste.png")).convert_alpha()
		Gro = pygame.image.load(os.path.join("resources", "PokedexPics", "Gro.png")).convert_alpha()
		Ice = pygame.image.load(os.path.join("resources", "PokedexPics", "Ice.png")).convert_alpha()
		Roc = pygame.image.load(os.path.join("resources", "PokedexPics", "Roc.png")).convert_alpha()

		Caught = pygame.image.load(os.path.join("resources", "PokedexPics", "Caught.png")).convert_alpha()
		NotCaught = pygame.image.load(os.path.join("resources", "PokedexPics", "NotCaught.png")).convert_alpha()
		SpriteBack = pygame.image.load(os.path.join("resources", "PokedexPics", "SpriteBack.png")).convert_alpha()

		return r


import time
from backpack import uiBackpack_scroll
class _window_uMe(rgine.windows.windowBase):
	def __init__(self, wsize, winbk=None, *args):
		super(_window_uMe, self).__init__(wsize, winbk)
		self.setRenderArgs(*args)

		self.player = self._args[0]

		self._handle = 0
		self._surface = pygame.Surface(wsize, pygame.SRCALPHA)
		self._surface.blit(self._bk, (0, 0))

		self._surf = None
		self._state = 0
		self._button_return = 0
		self.wmacros = rgine.windows.WindowsMacros()
		self._record = 0
		self._acc = 0
		self._static = []
		self.hClass = self._wm.RegisterCompleteClass(uiBackpack_scroll)

	def init(self, hWnd):
		self._handle = hWnd
		self._state = 0
		self._askbox_item = 0
		self._button_return = self._wm.CreateWindow(self.wmacros.WC_BUTTON, ((100, 20), None, "Return"))
		self._wm.MoveWindow(self._button_return, 100, 400)



		t = self.player.info["accomplishment"]
		self._static = []
		cx = 300
		cy = 25
		surf = pygame.Surface((400, 40), pygame.SRCALPHA)
		surf.fill((255, 255, 255, 128))
		self._static.append((surf, (300, 25)))
		for i in _accp:
			if i in t:
				self._static.append((eval(i), (cx, cy)))
			else:
				self._static.append((eval(i+"_Blank"), (cx, cy)))
			cx += 50


		surf = pygame.Surface((400, 300), pygame.SRCALPHA)
		surf.fill((111, 111, 111, 20))

		info = []
		t = self.player.info["catch_record"]
		import Combinedv2 as cdv2
		for i in t:
			info.append(("ID: %d, Name: %s, Count: %d, LastTime: %s"
					 %(i, cdv2.PokeStat[i][0][0], t[i][0], time.ctime(t[i][1])), -1))
		if not info: info.append(("No catch records yet :(", -1))
		p = 25*len(info)
		if p < 300: p = 300
		self._record = self._wm.CreateWindow(
				self.hClass,
				(
				(400, 300), surf, (400, p),
				info,
				)
						  )
		self._wm.MoveWindow(self._record, 300, 125)
		return True

	def callback(self, evt, uMsg):
		self._surf = self._surface.copy()
		for i in self._static:
			self._surf.blit(*i)

		for hWnd, msg, surface, pos in self._wm.DispatchMessage(evt):
			self._surf.blit(surface, pos)
			if hWnd == self._button_return and msg == self.wmacros.HIT:
				return False

		return True

	def render(self):
		return self._surf

	def release(self):
		self._wm.Release()

	def getMsg(self):
		return self._state

from Combinedv2 import getPokeLore, PokeStat
class _window_Pokedex(rgine.windows.windowBase):
	def __init__(self, wsize, winbk=None, *args):
		super(_window_Pokedex, self).__init__(wsize, winbk)
		self.setRenderArgs(*args)

		self.player = self._args[0]

		self._handle = 0
		self._surface = pygame.Surface(wsize, pygame.SRCALPHA)
		self._surface.fill((0, 0, 0))
		# self._surface.blit(self._bk, (0, 0))

		self._surf = None
		self._state = 0
		self._button_return = 0
		self.wmacros = rgine.windows.WindowsMacros()
		self.hClass = self._wm.RegisterCompleteClass(uiBackpack_scroll)
		self._lipkmon = 0
		self._lastcall = time.time()
		self._eevee_id = 134

	def init(self, hWnd):
		self._handle = hWnd
		self._state = 0
		self._button_return = self._wm.CreateWindow(self.wmacros.WC_BUTTON, ((100, 20), None, "Return"))
		self._wm.MoveWindow(self._button_return, 100, 400)
		# self._wm.SetTopmost(self._button_return, True)
		# self.player.pokemon: [Pokemon_inst]
		self._state = self.player.getCurrentPokemon().tID
##		self._state = 133
		#This gets type and image

		surf = pygame.Surface((200, 400-25), pygame.SRCALPHA)
		surf.fill((111, 111, 111, 20))

		info = []
		import Combinedv2 as cdv2

		def f(x): return (3-len(str(x)))*"0"+str(x)
		for i in range(1, 152):
			info.append((f(i), i))
		p = 25*len(info)
		if p < 400-25: p = 400-25
		self._lipkmon = self._wm.CreateWindow(
				self.hClass,
				(
				(200, 400-25), surf, (200, p),
				info,
				)
						  )
		self._wm.MoveWindow(self._lipkmon, 0, 25)
		self._present = {}
		for i in range(152):
			self._present[i] = False
		for i in self.player.pokemon+self.player.pokemon_save:
			self._present[i.tID] = True
		return True

	def callback(self, evt, uMsg):
		self._surf = self._surface.copy()

		for hWnd, msg, surface, pos in self._wm.DispatchMessage(evt):
			self._surf.blit(surface, pos)
			if hWnd == self._button_return and msg == self.wmacros.HIT:
				return False
			elif hWnd == self._lipkmon and msg != 0:
				self._state = msg
		self._surf.blit(self.render_info(self._present[self._state]), (310, 25))
		return True

	def render_info(self, isPresent):
		surf = pygame.Surface((400, 375), pygame.SRCALPHA)
##                        surf.blit(SpriteBack,(0,50))
		pokeLore=getPokeLore(self._state)
		pokeName=PokeStat[self._state][0][0]
		pygame.draw.circle(surf,(205,201,201),(170,155),45)
		pygame.draw.circle(surf,(139,137,137),(170,155),43)
		pygame.draw.circle(surf,(255,255,255),(170,155),40)
		Name_text = rgine.windows.render_text\
						(
														[400, 375],
												pokeName,
												pygame.font.SysFont('Times New Romen', 30),
												True, (255, 255, 255))
		ID_text = rgine.windows.render_text\
						(
														[400, 375],
												str(self._state),
												pygame.font.SysFont('Times New Romen', 30),
												True, (255, 255, 255))
		lore_text = rgine.windows.render_text\
						(
														[400, 375],
												pokeLore,
												pygame.font.SysFont('Times New Romen', 26),
												True, (255, 255, 255))

		if isPresent: surf.blit(Caught,(130,44))
		
		surf.blit(Name_text,(164,50))
		surf.blit(lore_text,(0,230))
		evolID=self._state+1

		lastcall = time.time()
		if PokeStat[self._state][-1][0]!="Final Stage of Evolution":
                        if pokeName != "Eevee":
                                EvolPic=pokepic=pygame.image.load(os.path.join("pokedex-media","pokemon", "main-sprites","platinum", str(evolID)+".png")).convert_alpha()
                                surf.blit(EvolPic,(131,114))
                        else:
                                if self._lastcall <= lastcall - 1:
                                        self._eevee_id += 1
                                        self._lastcall = lastcall
                                        if self._eevee_id == 137: self._eevee_id = 134
                                EvolPic=pokepic=pygame.image.load(os.path.join("pokedex-media","pokemon", "main-sprites","platinum", str(self._eevee_id)+".png")).convert_alpha()
                                surf.blit(EvolPic,(131,114))
                                
			

		type1=PokeStat[self._state][1][0]

		type2=PokeStat[self._state][1][-1]
		if type1!=type2:
			surf.blit(eval(type1),(129,80))
			surf.blit(eval(type2),(224,80))
		if type1==type2:
			surf.blit(eval(type1),(129,80))

		pokepicture=pygame.transform.scale(pygame.image.load((os.path.join("pokedex-media","pokemon", "sugimori", str(self._state)+".png"))), (130, 120)).convert_alpha()

		surf.blit(pokepicture,(-7,50))
		return surf

	def render(self):
		return self._surf

	def release(self):
		self._wm.Release()

	def getMsg(self):
		return self._state
						
						
MENU_EXIT = None
MENU_SAVE = 1
MENU_LOAD = 2

import base

class Menu_Me(base.pEvent):
	def __init__(self):
		super(Menu_Me, self).__init__()
		self.ui = 0
		self.hClass = 0
		self.player = None

	def setPlayer(self, player):
		self.player = player

	def init(self, evt, wm):
		if not self.hClass: self.hClass = wm.RegisterCompleteClass(_window_uMe)
		if wm.isWindowPresent(self.ui): return False
		self.ui = wm.CreateWindow(self.hClass, (wm.screensize, _img_uMe,
												self.player))
		return False


class Menu_Pokedex(base.pEvent):
	def __init__(self):
		super(Menu_Pokedex, self).__init__()
		self.ui = 0
		self.hClass = 0
		self.player = None

	def setPlayer(self, player):
		self.player = player

	def init(self, evt, wm):
		if not self.hClass: self.hClass = wm.RegisterCompleteClass(_window_Pokedex)
		if wm.isWindowPresent(self.ui): return False
		self.ui = wm.CreateWindow(self.hClass, (wm.screensize, Template, self.player))
		return False


class Menu_Help(base.pEvent):
	def __init__(self):
		super(Menu_Help, self).__init__()
		self._count = 0

	def init(self, evt, wm):
		self._count = 0
		print("Help Button Init ... ")
		return True

	def render(self, evt, wm):
		print("Help Button Procedure ... %d"%self._count)
		if self._count == 10:
			return None, (0, 0)
		self._count += 1
		return True, (0, 0)

	def release(self, wm):
		print("Help Button Release ... ")


class Menu_Exit(base.pEvent):
	def render(self, evt, wm):
		return True, MENU_EXIT


class Menu_Backpack(base.pEvent):
	def __init__(self):
		super(Menu_Backpack, self).__init__()
		self.uBackpack = None

	def setBackpack(self, uBackpack):
		self.uBackpack = uBackpack

	def init(self, evt, wm):
		if not self.uBackpack.isRunning(): self.uBackpack.init(evt, wm)
		return False


class Menu_Save(base.pEvent):
	def __init__(self):
		super(Menu_Save, self).__init__()

	def init(self, evt, wm):
		return True

	def render(self, evt, wm):
		return True, MENU_SAVE

	def release(self, wm):
		pass

class Menu_Load(base.pEvent):
	def __init__(self):
		super(Menu_Load, self).__init__()

	def init(self, evt, wm):
		return True

	def render(self, evt, wm):
		return True, MENU_LOAD

	def release(self, wm):
		pass

buttons = {1:"me", 2:"backpack", 3:"Save", 4:"Load", 5:"Pokedex", 99:"exit"}
inst = {1: Menu_Me(), 2: Menu_Backpack(), 3: Menu_Save(), 4: Menu_Load(), 5: Menu_Pokedex(), 99: Menu_Exit()}
