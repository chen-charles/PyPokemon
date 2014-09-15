from basics import *
from resources_loader import *

__author__ = 'Charles-Jianye Chen'

import sys
path = sys.path[0]
if not path: path = sys.path[1]
_battle_bk = rgine.surface_buffer.read_buffer(path+"/resources/bBG", 640, 436)

ATK = 1
DEF = 2

TYPE_PLAYER = 0
TYPE_NPC = 1
TYPE_WILD = 2

class choice1(object):
	# windowBase: RegisterClass
	# Battle First Choice Window
	def init(self, hWnd):
		self.wmacros = rgine.windows.WindowsMacros()
		self._handle = hWnd
		self._umsg = 0
		self._hasresult = False
		x, y, w, h = self.getRect()
		self._bk_ = pygame.Surface((w, h), pygame.SRCALPHA)
		self._buttons = {0: "ATTACK", 1: "BAG", 2:"POKEMON", 3:"RUN"}
		self._hWnds = {}

		x, y = self._wm.screensize

		# Outline Buttons
		button_size = self.wmacros.button_size[0]*2//3, self.wmacros.button_size[1]*2//3
		button_surf = pygame.transform.scale(self.wmacros.button.copy(), button_size)
		pygame.draw.rect(button_surf, (0, 0, 0), button_surf.get_rect(), 1)

		# Create Buttons
		t_handles = []
		k = list(self._buttons.keys())
		k.sort()
		for i in k:
			h = self._wm.CreateWindow(self.wmacros.WC_BUTTON,
								(button_size, button_surf, "%s"%self._buttons[i],
												pygame.font.SysFont('Times New Romen', 16),
												True, (255, 255, 255)), True)
			t_handles.append(h)
			self._hWnds[h] = i

		# Set Pos
		tx, ty = ((x//2)-button_size[0])//2, ((y//2)-button_size[1])//2
		self._wm.MoveWindowToPos(t_handles[0], tx, ty)
		self._wm.MoveWindowToPos(t_handles[1], tx+x//2, ty)
		self._wm.MoveWindowToPos(t_handles[2], tx, ty+y//2)
		self._wm.MoveWindowToPos(t_handles[3], tx+x//2, ty+y//2)
		self._wm.SetTopmost(t_handles[0], False)

		return True

	def cb(self, event, uMsg):
		self._bk_.fill((255, 255, 255, 255//2))
		for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
			self._bk_.blit(surface, pos)
			if msg == self.wmacros.HIT and hWnd in self._hWnds:
				self._umsg = self._hWnds[hWnd]
				self._hasresult = True  # this ensures the caller will be able to get the msg once
		return True

	def rd(self):
		return self._bk_

	def getMsg(self):
		"""
		:return (bHasResult, msg):
		"""
		if self._hasresult:
			self._hasresult = False # after caller gets the msg, return False instead
			return True, self._umsg
		return False, self._umsg

	def rel(self):
		self._wm.Release()


class choice2(choice1):
	def init(self, hWnd):
		self.wmacros = rgine.windows.WindowsMacros()
		self._handle = hWnd
		self._umsg = 0
		self._hasresult = False
		x, y, w, h = self.getRect()
		self._bk_ = pygame.Surface((w, h), pygame.SRCALPHA)
		self._buttons = self._args[0]
		self._hWnds = {}

		x, y = self._wm.screensize

		# Outline Buttons
		button_size = self.wmacros.button_size[0]*2//3, self.wmacros.button_size[1]*2//3
		button_surf = pygame.transform.scale(self.wmacros.button.copy(), button_size)
		pygame.draw.rect(button_surf, (0, 0, 0), button_surf.get_rect(), 1)

		t_handles = []
		# Create Buttons
		for i in range(len(self._buttons)):
			h = self._wm.CreateWindow(self.wmacros.WC_BUTTON,
								(button_size, button_surf, "%s"%self._buttons[i],
												pygame.font.SysFont('Times New Romen', 16),
												True, (255, 255, 255)), True)
			t_handles.append(h)
			self._hWnds[h] = i

		# Set Pos
		tx, ty = ((x//2)-button_size[0])//2, ((y//2)-button_size[1])//2
		self._wm.MoveWindowToPos(t_handles[0], tx, ty)
		self._wm.MoveWindowToPos(t_handles[1], tx+x//2, ty)
		self._wm.MoveWindowToPos(t_handles[2], tx, ty+y//2)
		self._wm.MoveWindowToPos(t_handles[3], tx+x//2, ty+y//2)
		self._wm.SetTopmost(t_handles[0], False)
		return True

	def cb(self, event, uMsg):
		self._bk_.fill((255, 255, 255, 255//2))

		# If K_ESCAPE, return to the prev one
		if event.isKeyHit(pygame.K_ESCAPE):
			self._umsg = -1
			self._hasresult = True
			return True

		for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
			self._bk_.blit(surface, pos)
			if msg == self.wmacros.HIT and hWnd in self._hWnds:
				self._umsg = self._hWnds[hWnd]
				self._hasresult = True
		return True


class uiStatus(choice1):
	def init(self, hWnd):
		self.wmacros = rgine.windows.WindowsMacros()
		self._handle = hWnd
		self._umsg = 0
		self._hasresult = False
		x, y, w, h = self.getRect()
		self._bk_ = pygame.Surface((w, h), pygame.SRCALPHA)
		self._owner = self._args[0]
		self._hWnds = {}

		# Create UI
		x, y = self._wm.screensize
		px, py = 100, 25
		self._pgbar_hp = rgine.Progressbar((px, py), (255, 0, 0), 5, 0, 0)
		self._render_pgbar_hp = lambda pgbar: (pgbar.render(), ((x-px)//2, (y-py)*5//10))
		px, py = 100, 10
		self._pgbar_exp = rgine.Progressbar((px, py), (0, 255, 0), 5, 0, 0)
		self._render_pgbar_exp = lambda pgbar: (pgbar.render(), ((x-px)//2, (y-py)*9//10))
		self._ft = pygame.font.SysFont('Times New Romen', 16)
		return True

	def cb(self, event, uMsg):
		return True

	def rd(self):
		# Refresh UI every single frame, instead of refresh at topmost
		self._bk_.fill((255, 255, 255, 255//2))
		self._pgbar_hp.set_pos(self._owner.get_hp_percentage())
		self._pgbar_exp.set_pos(self._owner.get_exp_percentage())

		self._bk_.blit(*self._render_pgbar_hp(self._pgbar_hp))
		self._bk_.blit(*self._render_pgbar_exp(self._pgbar_exp))
		self._bk_.blit(
			self._ft.render(self._owner.getName()+"  Lv. %d"%self._owner.get_level(), True, (255, 255, 255)),
			(0, 0),
		)
		return self._bk_


class _BattleMain(rgine.windows.windowBase):
	def _create_cpokemon(self):
		# Refresh Pokemon Info (after current pokemon changed)

		winsize = 16*10, 9*10
		self._hWnds["uistatus_atk"] = self._wm.CreateWindow(
			self._wm.RegisterClass(False, uiStatus.init, uiStatus.cb, uiStatus.rd, uiStatus.getMsg, uiStatus.rel),
			(winsize, None, self._atk.getCurrentPokemon()), False,
			)

		# x, y = self._wm.screensize
		self._wm.MoveWindow(self._hWnds["uistatus_atk"], 0, 0)

		winsize = 16*10, 9*10
		self._hWnds["uistatus_def"] = self._wm.CreateWindow(
			self._wm.RegisterClass(False, uiStatus.init, uiStatus.cb, uiStatus.rd, uiStatus.getMsg, uiStatus.rel),
			(winsize, None, self._def.getCurrentPokemon()), False,
			)

		x, y = self._wm.screensize
		self._wm.MoveWindow(self._hWnds["uistatus_def"], x-winsize[0], 0)

		def c_choice1(self):
			winsize = self._wm.screensize[0], 16*8
			self._hWnds["choice1"] = self._wm.CreateWindow(
				self._wm.RegisterClass(False, choice1.init, choice1.cb, choice1.rd, choice1.getMsg, choice1.rel),
				(winsize, None), False,
				)
			x, y = self._wm.screensize
			self._wm.MoveWindow(self._hWnds["choice1"], (x-winsize[0])*9.5//10, (y-winsize[1])*9.5//10)

		self._init_choice1 = c_choice1
		def c_choice2(self):
			winsize = self._wm.screensize[0], 16*8
			self._hWnds["choice2"] = self._wm.CreateWindow(
				self._wm.RegisterClass(False, choice2.init, choice2.cb, choice2.rd, choice2.getMsg, choice2.rel),
				(winsize, None, self._atk.getCurrentPokemon().getSkills()), False,
				)

			x, y = self._wm.screensize
			self._wm.MoveWindow(self._hWnds["choice2"], (x-winsize[0])*1//10, (y-winsize[1])*9.5//10)

		self._init_choice2 = c_choice2

	def _update_cpokemon(self):
		if self._wm.isWindowPresent(self._hWnds["uistatus_atk"]): self._wm.DestroyWindow(self._hWnds["uistatus_atk"])
		if self._wm.isWindowPresent(self._hWnds["uistatus_def"]): self._wm.DestroyWindow(self._hWnds["uistatus_def"])
		self._create_cpokemon()

	def set_args(self, atk, defense, backpack, wm):
		# Set all needed args

		self._atk = atk
		self._def = defense
		self._backpack = backpack
		self._backpack_mode = 0
		self._g_wm = wm

	def init(self, hWnd):
		self.wmacros = rgine.windows.WindowsMacros()
		self._handle = hWnd
		self._umsg = 0
		w, h = self._size
		self._bk_ = pygame.Surface((w, h), pygame.SRCALPHA)
		self._hWnds = {}

		self.set_args(*self._args[:5])

		self._create_cpokemon()

		self._hWnds["choice1"] = 0
		self._hWnds["choice2"] = 0

		self._init_choice1(self)
		self._wm.SetTopmost(self._hWnds["choice1"], True)
		self._uiRunning = True  # check if all ui are closed
		self._dbox = 0
		self._text = []
		self._lastFrom = 0  # check who should attack next
		self._selecting_nxt = False
		self._result = 0
		return True


	def callback(self, event, uMsg):
		if uMsg == self.wmacros.WM_KILLFOCUS:
			return True
		self._bk_ = self._bk.copy()
		x, y = self._wm.screensize

		# render pokemon image
		self._bk_.blit(self._atk.getCurrentPokemon().render(False),
		               (60, y-self._atk.getCurrentPokemon().get_size()[1]-y+(y-16*8)*9.5//10+40))
		self._bk_.blit(self._def.getCurrentPokemon().render(True),
		               (x-100-self._def.getCurrentPokemon().get_size()[0], 60))

		if self._backpack_mode:
			msg = self._backpack.getMsg()
			if msg is None: # Backpack Destroyed
				self._backpack_mode = 0
				self._wm.DestroyWindow(self._hWnds["choice1"])
				self._wm.DestroyWindow(self._hWnds["choice2"])
				self._uiRunning = False
			elif msg == 1:  # Backpack Pokeball Used
				self._result = ATK
				self._backpack_mode = 0
				self._wm.DestroyWindow(self._hWnds["choice1"])
				self._wm.DestroyWindow(self._hWnds["choice2"])
				self._create_dbox(["Caught %s !"%self._def.getCurrentPokemon().name,
							"You WON The Battle! ",
							 "Gained %d EXP\nGained %d Gold"%(0, 0)
						])
				return True
			elif msg == -1: # Backpack Return Hit
				self._backpack_mode = 0
				if self._selecting_nxt:
					# if user cancelled selection, just select the next one in the pocket
					nxt = self._atk.getNextAlivePokemon()
					self._atk.setCurrentPokemon(nxt.id)
				self._update_cpokemon()
				self._wm.DestroyWindow(self._hWnds["choice1"])
				self._wm.DestroyWindow(self._hWnds["choice2"])
				self._hWnds["choice1"] = 0
				self._hWnds["choice2"] = 0

				self._init_choice1(self)
				self._wm.SetTopmost(self._hWnds["choice1"], True)
				self._uiRunning = True
				self._lastFrom = ATK

		if not self._uiRunning: # if all ui are closed, def will attack atk, then create new ui again
			import random
			ski = random.randint(0, 3)
			result = -1

			# Check attack PP
			if not self._def.getCurrentPokemon().getSkillPP(ski):
				for i in range(4):
					if self._def.getCurrentPokemon().getSkillPP(i):
						result = i
						break
				if result == -1:
					result = 0  # attack with 0 pp: damage will be zero, in cdv2.Pokemon.attack
			else:
				result = ski

			self._def.getCurrentPokemon().attack(self._atk.getCurrentPokemon(), result)

			# Create dbox
			self._text.append(self._def.getCurrentPokemon().get_str()+
							"\nSkill: %s\nSkill PP Left: %d"
					        %(self._def.getCurrentPokemon().getSkill(result) ,self._def.getCurrentPokemon().getSkillPP(result)))
			x, y = self._wm.screensize
			dboxsize = x, y*3//10
			self._dbox = self._wm.CreateWindow(
					self._wm.RegisterCompleteClass(ConversationBox),
					(dboxsize, None, "%s"%self._def.getCurrentPokemon().name,
                    pygame.font.SysFont('Times New Romen', 16),
					True, (255, 255, 255), self._text))
			self._text = []
			self._wm.MoveWindow(self._dbox, 0, (y-self._wm.getInstance(self._dbox).getRect()[3]))
			self._wm.getInstance(self._dbox).setFrameMovable(False)
			self._lastFrom = DEF

			self._wm.SetTopmost(self._dbox, True)
			self._uiRunning = True

		for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
			self._bk_.blit(surface, pos)
			if hWnd  == self._hWnds["choice1"]:
				r, msg = msg
				if not r: continue  # if not new msg, continue
				if msg == 0:    # Attack
					self._wm.DestroyWindow(self._hWnds["choice1"])
					self._init_choice2(self)
					self._wm.SetTopmost(self._hWnds["choice2"], True)
					self._uiRunning = True
				elif msg == 1:  # Backpack
					if not self._backpack.isRunning():
						self._backpack.setPlayer(self._atk)
						self._backpack.setOther(self._def)
						self._backpack.setDefaultTab(2)
						self._backpack.setStatic(True)  # User cannot change the tab is it is static
						self._backpack.init(event, self._g_wm)
						self._backpack_mode = 2
				elif msg == 2:  # Pokemon
					if not self._backpack.isRunning():
						self._backpack.setPlayer(self._atk)
						self._backpack.setOther(self._def)
						self._backpack.setDefaultTab(1)
						self._backpack.setStatic(True)
						self._backpack.init(event, self._g_wm)
						self._backpack_mode = 1
				elif msg == 3:  # Escape
					if self._def.getType() == TYPE_WILD:
						import random
						if random.randint(0, 1):
							self._result = ATK
							self._create_dbox(["Escaped! "], DEF)
						else:
							self._create_dbox(["Failed To Escape! "], ATK)
					else:
						self._create_dbox(["Could not RUN this time! "], DEF)


			if hWnd == self._hWnds["choice2"]:
				r, msg = msg
				if not r: continue
				if msg == -1:   # return to choice 1 menu
					self._wm.DestroyWindow(self._hWnds["choice1"])
					self._wm.DestroyWindow(self._hWnds["choice2"])
					self._init_choice1(self)
					self._wm.SetTopmost(self._hWnds["choice1"], True)
					self._uiRunning = True
				else:
					if not self._atk.getCurrentPokemon().getSkillPP(msg): continue  # if not enough pp, disable skill
					self._atk.getCurrentPokemon().attack(self._def.getCurrentPokemon(), msg)

					# Create dbox
					self._text.append(self._atk.getCurrentPokemon().get_str()+
					                  "\nSkill: %s\nSkill PP Left: %d"
					                  %(self._atk.getCurrentPokemon().getSkill(msg) ,self._atk.getCurrentPokemon().getSkillPP(msg)))
					self._wm.DestroyWindow(self._hWnds["choice1"])
					self._wm.DestroyWindow(self._hWnds["choice2"])
					self._uiRunning = False

					x, y = self._wm.screensize
					dboxsize = x, y*3//10
					self._dbox = self._wm.CreateWindow(
							self._wm.RegisterCompleteClass(ConversationBox),
							(dboxsize, None, "%s"%self._atk.getCurrentPokemon().name,
                            pygame.font.SysFont('Times New Romen', 16),
							True, (255, 255, 255), self._text))
					self._text = []
					self._wm.MoveWindow(self._dbox, 0, (y-self._wm.getInstance(self._dbox).getRect()[3]))
					self._wm.getInstance(self._dbox).setFrameMovable(False)
					self._lastFrom = ATK

					self._wm.SetTopmost(self._dbox, True)
					self._uiRunning = True

			if hWnd == self._dbox and (msg[0] == msg[1]):
				if self._result:    # if battle ended, after last dbox is finished, battle should exit
					self._umsg = self._result
					return True
				self._wm.DestroyWindow(self._dbox)
				self._dbox = 0
				self._uiRunning = False
				if self._lastFrom == ATK and not self._def.getCurrentPokemon().getHP(): # if def currentPokemon dead
					nxt = self._def.getNextAlivePokemon()
					if nxt is None:
						self._result = ATK  # if result, exit after last msgbox

						# Check Awards
						exp = 0
						gold = 0
						import random
						for i in self._def.pokemon:
							level = i.level
							if level <= 20:
								gold += level*10 + random.randint(10, 100)
							elif level > 20:
								gold += level*15
							exp += level*4
						self._create_dbox(
							["You WON The Battle! ",
							 "Gained %d EXP\nGained %d Gold"%(exp, gold)]
						)
						self._atk.money += gold
						self._atk.getCurrentPokemon().add_exp(exp)
						self._update_cpokemon()
					else:   # auto select the next pokemon
						self._def.setCurrentPokemon(nxt.id)
						self._lastFrom = DEF    # end turn
				if self._lastFrom == DEF and not self._atk.getCurrentPokemon().getHP(): # if atk currentPokemon dead
					nxt = self._atk.getNextAlivePokemon()
					if nxt is None:
						# if no more alive ones, just return
						self._result = DEF
						self._create_dbox(["You LOST The Battle! "])
					else:
						# launch ui_backpack select next
						self._selecting_nxt = True
						if not self._backpack.isRunning():
							self._backpack.setPlayer(self._atk)
							self._backpack.setDefaultTab(1)
							self._backpack.setStatic(True)
							self._backpack.init(event, self._g_wm)
							self._backpack_mode = 1
							self._uiRunning = True

				if self._lastFrom == DEF and not self._uiRunning:   # create ui
					self._update_cpokemon()
					self._hWnds["choice1"] = 0
					self._hWnds["choice2"] = 0

					self._init_choice1(self)
					self._wm.SetTopmost(self._hWnds["choice1"], True)
					self._uiRunning = True

		return True

	def _create_dbox(self, texts=[], lastfrom=None):
		# Destroy Current UI
		self._wm.DestroyWindow(self._hWnds["choice1"])
		self._wm.DestroyWindow(self._hWnds["choice2"])
		self._uiRunning = False

		self._text += texts

		# Create dbox
		x, y = self._wm.screensize
		dboxsize = x, y*3//10
		self._dbox = self._wm.CreateWindow(
				self._wm.RegisterCompleteClass(ConversationBox),
				(dboxsize, None, "%s"%self._atk.getCurrentPokemon().name,
	            pygame.font.SysFont('Times New Romen', 16),
				True, (255, 255, 255), self._text))
		self._text = []
		self._wm.MoveWindow(self._dbox, 0, (y-self._wm.getInstance(self._dbox).getRect()[3]))
		self._wm.getInstance(self._dbox).setFrameMovable(False)

		if lastfrom is not None: self._lastFrom = lastfrom

		self._wm.SetTopmost(self._dbox, True)
		self._uiRunning = True

	def render(self):
		return self._bk_

	def getMsg(self):
		return self._umsg

	def release(self):
		self._wm.Release()


class Battle(pEvent):
	# taking player objects
	def __init__(self, backpack, wm):
		super(Battle, self).__init__()
		self._scene = -1
		self._activated = False
		self._hWnds = {}
		self._atk = None
		self._def = None
		self._init_choice1 = lambda x: x
		self._init_choice2 = lambda x: x
		self._backpack = backpack
		self._g_wm = wm
		self._uiRunning = False
		self.scenebk = None
		self.lastwinner = ATK

	def setFightingObjects(self, atk, defense):
		# player objects
		if atk is not None: self._atk = atk
		if defense is not None: self._def = defense

	def setBackground(self, surface):
		self.scenebk = surface.copy()

	def init(self, evt, wm):
		if not self._activated:
			atk, defense = self._atk, self._def
			backpack = self._backpack
			wm = self._g_wm
			#if atk is None or defense is None: raise ValueError((atk, defense))
			self._activated = True

			winsize = wm.screensize
			if self.scenebk is None: self.scenebk = pygame.transform.scale(_battle_bk, winsize).convert_alpha()
			self._scene = wm.CreateWindow(
				wm.RegisterCompleteClass(_BattleMain),
				(winsize, self.scenebk, atk, defense, backpack, wm)
				)
			x, y = wm.screensize
			wm.MoveWindow(self._scene, (x-winsize[0])//2, (y-winsize[1])//2)

			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			if wm.getInstance(self._scene) is None: # if scene is done
				self.release(wm)
			else:
				umsg = wm.getMsg(self._scene)
				if umsg == ATK or umsg == DEF: self.lastwinner = umsg
				return None, umsg
		return None, None

	def release(self, wm):
		wm.DestroyWindow(self._scene)
		self._scene = -1
		self._activated = False
