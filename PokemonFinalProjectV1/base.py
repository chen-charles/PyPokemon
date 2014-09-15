from basics import *
from resources_loader import *
__author__ = 'Charles-Jianye Chen', "Raymond Li"
#Added Stones
#Cost fixed
#Removed Gym Leader Safegaurd

ATK = 1
DEF = 2

class TestNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk):
		super(TestNPC, self).__init__(pos, res_walk)

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			_button_size = self.wmacros.button_size[:]
			# _button_size = list(map((lambda x: x//2), _button_size))
			msgbox = wm.CreateWindow(self.wmacros.WC_MSGBOX,
									 ((400, 200), None, "MessageBox!", None, None, None,
									  "Good Morning! How Are You? ",
									  self.wmacros.MB_ICONWARNING | self.wmacros.MB_CANCELTRYCONTINUE
									  , [_button_size[0]//2, _button_size[1]//2]))
			self._hWnds["msgbox"] = msgbox
			wm.SetTopmost(self._hWnds["msgbox"], True)
			wm.getInstance(self._hWnds["msgbox"]).center(*wm.screensize)
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			umsg = wm.getMsg(self._hWnds["msgbox"])
			if umsg is None: self.release(wm) # is terminated
			else:
				if umsg != self.wmacros.IDNORESULT:
					self.release(wm)

		return self.render_scene()


class ConversationNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk, sentences, title="ConversationNPC"):
		if not len(sentences): raise ValueError(len(sentences))
		super(ConversationNPC, self).__init__(pos, res_walk)
		self._sentences = sentences
		# for i in range(len(self._sentences)):
		# 		self._sentences[i] = "    "+self._sentences[i]
		self._dir = DOWN
		self._title = title
		self.dbox = 0

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True

			x, y = wm.screensize
			dboxsize = x, y*3//10
			self.dbox = wm.CreateWindow(
					wm.RegisterCompleteClass(ConversationBox), (dboxsize, None, str(self._title),
																pygame.font.SysFont('Times New Romen', 16),
																True, (255, 255, 255), self._sentences))

			wm.MoveWindow(self.dbox, 0, (y-wm.getInstance(self.dbox).getRect()[3]))
			wm.getInstance(self.dbox).setFrameMovable(False)
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			umsg = wm.getMsg(self.dbox)
			if umsg[0] == umsg[1]:
				self.release(wm)

		return self.render_scene()

	def release(self, wm):
		super(ConversationNPC, self).release(wm)
		wm.DestroyWindow(self.dbox)
		self.dbox = 0


class TaskNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk, taskid, taskprev, taskname="Task"):
		super(TaskNPC, self).__init__(pos, res_walk)
		self.player = None
		self.taskid = taskid
		self.task = None
		self.taskprev = taskprev
		self.taskname = taskname

	def setPlayer(self, player):
		self.player = player

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			isNewCreated, self.task = self.player.open_task(self.taskid, self.taskprev, self.taskname)
			if not self.player.check_prev_task(self.task.prev): self.task.stage = 0
			if self.task.stage == 0:
				_button_size = self.wmacros.button_size[:]
				self._hWnds["msgbox"] =  wm.CreateWindow(self.wmacros.WC_MSGBOX,
				 ((400, 200), None, self.task.name, None, None, None,
				  "Kiddo, you are not ready for this :( \n"
				  "Please complete the preparation(s) first!\n"
				  "See you later :) ",
				  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_OK
				  , [_button_size[0]//2, _button_size[1]//2]))
				wm.SetTopmost(self._hWnds["msgbox"], True)
				wm.getInstance(self._hWnds["msgbox"]).center(*wm.screensize)
				return True
			else:
				return self.init_(evt, wm)
		return False

	def render(self, evt, wm):
		if self._activated and self.task.stage == 0:
			if wm.getMsg(self._hWnds["msgbox"]) == self.wmacros.IDOK:
				wm.SetTopmost(-1, False)
				self.release(wm)
				# return None, (0, 0)
		elif self._activated:
			return self.render_(evt, wm)
		return self.render_scene()

	def init_(self, evt, wm):
		return True

	def render_(self, evt, wm):
		return self.render_scene()


class ShopNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk, items={}):
		super(ShopNPC, self).__init__(pos, res_walk)
		self._items_sell = items
		self._items = dict()
		self.player = None

	def setPlayer(self, player):
		self.player = player

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			_button_size = [100, 30]
			for i in self._items_sell:
				self._items[i] = self.player.addItem(self._items_sell[i])[1]

			def init(self, hWnd):   #init
				nonlocal _button_size
				self.macros = rgine.windows.WindowsMacros()
				self.button_id = -1

				cx = cy = tx = ty = 0
				self._askbox = 0
				x, y = self._size
				self._hWnds = {}
				self._stable = []
				buttons = self._args[4]
				t = list(buttons.keys())
				t.sort()
				self.framewidth = 20
				self._diff = (self.getRect()[2] - 2 * self.framewidth - 5 * (_button_size[0])) // 4
				for i in t:
					self._button0 = self._wm.CreateWindow(self.macros.WC_BUTTON, (_button_size, self.macros.button, "%s"%i,
					pygame.font.SysFont('Times New Roman', 16),
					True, (255, 255, 255)), True)
					Times_New_Roman = pygame.font.SysFont('Times New Roman', 16)
					self._text0 = Times_New_Roman.render("%s"%str(buttons[i].buy_price), True, (0, 0, 0))

					self._wm.MoveWindow(self._button0, cx + self.framewidth, cy + self.framewidth)
					tx = _button_size[0]/2 - self._text0.get_width()/2 + cx + self.framewidth
					ty = _button_size[1] + cy + self.framewidth
					cx += _button_size[0] + self._diff

					self._stable.append((self._text0, (tx, ty)))



					if cx +  _button_size[0] > self.getRect()[2]:
						cx = 0
						cy += (2 * _button_size[1]+1)
					if tx + 20 > self.getRect()[2]:
						tx = 0
						ty += (2 * _button_size[1]+1)
					self._hWnds[i] = self._button0
				self._exit_button =  self._wm.CreateWindow(self.macros.WC_BUTTON, (_button_size, self.macros.button, "Exit",
												   pygame.font.SysFont('Times New Romen', 16),
												   True, (255, 255, 255)), True)
				x,y = self.getClientSize()
				self._wm.MoveWindow(self._exit_button, x-_button_size[0]-20, y-_button_size[1]-20)
				self._hWnds[exit] = self._exit_button
				self._hWnds["msgbox"] = 0
				self._handle = hWnd
				self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
				self.msgbox = 0
				return True


			def cb(self, event, uMsg):  #callback
				nonlocal _button_size
				self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
				for i in self._stable:
					self._bk_.blit(*i)
				for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
					self._bk_.blit(surface, pos)

					if msg == self.macros.HIT and hWnd == self._hWnds[exit]:
						return False
					for x in self._hWnds:
						self.umsg = msg
						if msg == self.macros.HIT and hWnd == self._hWnds[x] and not self._askbox:
							self._askbox = self._wm.CreateWindow(self._wm.RegisterCompleteClass(amtbox),
												 ((100, 50), None, "Amount"))
							self._wm.MoveWindow(self._askbox, 0, 0)
							self._wm.SetTopmost(self._askbox, True)
							self._wm.getInstance(self._askbox).center(*self._wm.screensize)
							self._current_item = x

					if hWnd == self._askbox and msg:
						amt = int(msg)
						self._wm.DestroyWindow(self._askbox)
						self._askbox = 0
						self._wm.SetTopmost(-1, False)
						if amt == -1:
							self._current_item = 0
							continue
						d = self._args[4]
						item = d[self._current_item]
						if amt > item.getMaxBuy(): amt = item.getMaxBuy()
						item.buy(amt)
						_button_size = self.wmacros.button_size[:]
						self._hWnds["msgbox"] =  self._wm.CreateWindow(self.wmacros.WC_MSGBOX,
						 ((400, 200), None, "Buy", None, None, None,
						  "Bought %d %s! "%(amt, item.name),
						  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_OK
						  , [_button_size[0]//2, _button_size[1]//2]))
						self._wm.SetTopmost(self._hWnds["msgbox"], True)
						self._wm.getInstance(self._hWnds["msgbox"]).center(*self._wm.screensize)
						self._current_item = 0
				return True

			def rd(self):   #render
				return self._bk_

			def getMsg(self):
				return self.button_id

			def rel(self):  #release
				self._wm.Release()
				if self._args[4]: list(self._args[4].values())[0].owner.check_backpack()


			background = pygame.image.load("Pokemon Shop.jpg")
			dboxsize = wm.screensize[0]*3//4, wm.screensize[1]*3//4
			background = pygame.transform.scale(background, dboxsize).convert()
			background.set_alpha(200)

			self._hWnds["shop"] = wm.CreateWindow(wm.RegisterClass(True, init, cb, rd, getMsg, rel), (dboxsize, background , "Shop",
														  pygame.font.SysFont('Times New Romen', 16),
														  True, (255, 255, 255), self._items))

			wm.MoveWindow(self._hWnds["shop"], wm.screensize[0]/2-dboxsize[0]/2, wm.screensize[1]/2-dboxsize[1]/2)
			wm.SetTopmost(self._hWnds["shop"])
			return True
		return False

	def render(self, evt, wm):
			if not self._activated: return self.render_scene()
			for i in self._hWnds:
				umsg = wm.getMsg(self._hWnds[i])
				if umsg is None: self.release(wm)
			return self.render_scene()

class SellNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk):
		super(SellNPC, self).__init__(pos, res_walk)
		self._items = {}
		self.player = None

	def setPlayer(self, player):
		self.player = player
		self._items = self.player.backpack

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			_button_size = [100, 30]

			def init(self, hWnd):   #init
				nonlocal _button_size
				self.macros = rgine.windows.WindowsMacros()
				self.button_id = -1

				cx = cy = tx = ty = 0
				self._askbox = 0
				x, y = self._size
				self._hWnds = {}
				self._stable = []
				buttons = self._args[4]
				t = list(buttons.keys())
				t.sort()
				self.framewidth = 20
				self._diff = (self.getRect()[2] - 2 * self.framewidth - 5 * (_button_size[0])) // 4
				for i in t:
					self._button0 = self._wm.CreateWindow(self.macros.WC_BUTTON, (_button_size, self.macros.button,
					                                                              "%s"%buttons[i].name,
																				pygame.font.SysFont('Times New Roman', 16),
																				True, (255, 255, 255)), True)
					Times_New_Roman = pygame.font.SysFont('Times New Roman', 16)
					self._text0 = Times_New_Roman.render("%s"%str(buttons[i].sell_price), True, (0, 0, 0))

					self._wm.MoveWindow(self._button0, cx + self.framewidth, cy + self.framewidth)
					tx = _button_size[0]/2 - self._text0.get_width()/2 + cx + self.framewidth
					ty = _button_size[1] + cy + self.framewidth
					cx += _button_size[0] + self._diff

					self._stable.append((self._text0, (tx, ty)))



					if cx +  _button_size[0] > self.getRect()[2]:
						cx = 0
						cy += (2 * _button_size[1]+1)
					if tx + 20 > self.getRect()[2]:
						tx = 0
						ty += (2 * _button_size[1]+1)
					self._hWnds[i] = self._button0
				self._exit_button =  self._wm.CreateWindow(self.macros.WC_BUTTON, (_button_size, self.macros.button, "Exit",
												   pygame.font.SysFont('Times New Romen', 16),
												   True, (255, 255, 255)), True)
				x,y = self.getClientSize()
				self._wm.MoveWindow(self._exit_button, x-_button_size[0]-20, y-_button_size[1]-20)
				self._hWnds[exit] = self._exit_button
				self._handle = hWnd
				self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
				self.msgbox = 0
				return True


			def cb(self, event, uMsg):  #callback
				nonlocal _button_size
				self._bk_ = pygame.Surface(self.getClientSize(), pygame.SRCALPHA)
				for i in self._stable:
					self._bk_.blit(*i)
				for hWnd, msg, surface, pos in self._wm.DispatchMessage(event):
					self._bk_.blit(surface, pos)

					if msg == self.macros.HIT and hWnd == self._hWnds[exit]:
						return False
					for x in self._hWnds:
						self.umsg = msg
						if msg == self.macros.HIT and hWnd == self._hWnds[x] and not self._askbox:
							self._askbox = self._wm.CreateWindow(self._wm.RegisterCompleteClass(amtbox),
												 ((100, 50), None, "Amount"))
							self._wm.MoveWindow(self._askbox, 0, 0)
							self._wm.SetTopmost(self._askbox, True)
							self._wm.getInstance(self._askbox).center(*self._wm.screensize)
							self._current_item = x

					if hWnd == self._askbox and msg:
						amt = int(msg)
						self._wm.DestroyWindow(self._askbox)
						self._askbox = 0
						self._wm.SetTopmost(-1, False)
						if amt == -1:
							self._current_item = 0
							continue
						d = self._args[4]
						item = d[self._current_item]
						if amt > item.getMaxSell(): amt = item.getMaxSell()
						item.sell(amt)
						self._current_item = 0
						if item.count == 0:
							self._wm.DestroyWindow(self._hWnds[item.id])
						_button_size = self.wmacros.button_size[:]
						self._hWnds["msgbox"] =  self._wm.CreateWindow(self.wmacros.WC_MSGBOX,
						 ((400, 200), None, "Sell", None, None, None,
						  "Sold %d %s! "%(amt, item.name),
						  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_OK
						  , [_button_size[0]//2, _button_size[1]//2]))
						self._wm.SetTopmost(self._hWnds["msgbox"], True)
						self._wm.getInstance(self._hWnds["msgbox"]).center(*self._wm.screensize)

				return True

			def rd(self):   #render
				return self._bk_

			def getMsg(self):
				return self.button_id

			def rel(self):  #release
				self._wm.Release()
				if self._args[4]: list(self._args[4].values())[0].owner.check_backpack()


			background = pygame.image.load("Pokemon Shop.jpg")
			dboxsize = wm.screensize[0]*3//4, wm.screensize[1]*3//4
			background = pygame.transform.scale(background, dboxsize).convert()
			background.set_alpha(200)

			self._hWnds["shop"] = wm.CreateWindow(wm.RegisterClass(True, init, cb, rd, getMsg, rel), (dboxsize, background , "Sell",
														  pygame.font.SysFont('Times New Romen', 16),
														  True, (255, 255, 255), self._items))

			wm.MoveWindow(self._hWnds["shop"], wm.screensize[0]/2-dboxsize[0]/2, wm.screensize[1]/2-dboxsize[1]/2)
			wm.SetTopmost(self._hWnds["shop"])
			return True
		return False

	def render(self, evt, wm):
			if not self._activated: return self.render_scene()
			for i in self._hWnds:
				umsg = wm.getMsg(self._hWnds[i])
				if umsg is None: self.release(wm)
			return self.render_scene()


class BattleNPC(NPC_Skeleton):
		def __init__(self, pos, res_walk, sentences, title="ConversationNPC", fightwhat=None):
				if not len(sentences): raise ValueError(len(sentences))
				super(BattleNPC, self).__init__(pos, res_walk)
				self._s_start = sentences[0]
				self._s_end = sentences[1]
				# for i in range(len(self._sentences)):
				#               self._sentences[i] = "    "+self._sentences[i]
				self._dir = DOWN
				self._title = title
				self.dbox = 0
				self.nbox = 0
				self.player = None
				self.uBattle = None
				self._bBattle = False
				self.fightwhat = fightwhat

		def setPlayer(self, player):
				self.player = player

		def setBattle(self, uBattle):
				self.uBattle = uBattle

		def init(self, evt, wm):
				if not self._activated:
						self._activated = True

						x, y = wm.screensize
						dboxsize = x, y*3//10
						self.dbox = wm.CreateWindow(
										wm.RegisterCompleteClass(ConversationBox), (dboxsize, None, str(self._title),
																					pygame.font.SysFont('Times New Romen', 16),
																					True, (255, 255, 255), self._s_start))

						wm.MoveWindow(self.dbox, 0, (y-wm.getInstance(self.dbox).getRect()[3]))
						wm.getInstance(self.dbox).setFrameMovable(False)


						return True
				return False

		def render(self, evt, wm):
						if not self._activated: return self.render_scene()
						umsg = wm.getMsg(self.dbox)
						if umsg is not None and umsg[0] == umsg[1]:
								wm.DestroyWindow(self.dbox)
								if self.uBattle.isRunning(): self.release(wm)
								else:
										if self.fightwhat is None: return None, (0, 0)
										self.uBattle.setFightingObjects(self.player, self.fightwhat)
										self.uBattle.init(evt, wm)
										self._bBattle = True
						if self._bBattle and not self.uBattle.isRunning():
								self._bBattle = False
								x, y = wm.screensize
								dboxsize = x, y*3//10
								self.nbox = wm.CreateWindow(
										wm.RegisterCompleteClass(ConversationBox), (dboxsize, None, str(self._title),
																					pygame.font.SysFont('Times New Romen', 16),
																					True, (255, 255, 255), self._s_end))
								wm.MoveWindow(self.nbox, 0, (y-wm.getInstance(self.nbox).getRect()[3]))
								wm.getInstance(self.nbox).setFrameMovable(False)
						umsg = wm.getMsg(self.nbox)
						if umsg is not None and umsg[0] == umsg[1]:
								wm.DestroyWindow(self.nbox)
								self.release(wm)

						return self.render_scene()

		def release(self, wm):
				super(BattleNPC, self).release(wm)
				wm.DestroyWindow(self.dbox)
				self.dbox = 0
				self._bBattle = False


class GymLeaderNPC(BattleNPC):
	def __init__(self, pos, res_walk, taskid, taskprev, sentences, taskname="Task", accomplishment="GymLeaderNPC",
	             fightwhat=None):
		super(GymLeaderNPC, self).__init__(pos, res_walk, sentences, taskname, fightwhat)
		self.taskid = taskid
		self.task = None
		self.taskprev = taskprev
		self.taskname = taskname
		self.acc = accomplishment

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			isNewCreated, self.task = self.player.open_task(self.taskid, self.taskprev, self.taskname)
			if not self.player.check_prev_task(self.task.prev):
				self.task.stage = 0

				_button_size = self.wmacros.button_size[:]
				self._hWnds["msgbox"] =  wm.CreateWindow(self.wmacros.WC_MSGBOX,
				 ((400, 200), None, self.task.name, None, None, None,
				  "Kiddo, you are not ready for this :( \n"
				  "Please complete the preparation(s) first!\n"
				  "See you later :) ",
				  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_OK
				  , [_button_size[0]//2, _button_size[1]//2]))
				wm.SetTopmost(self._hWnds["msgbox"], True)
				wm.getInstance(self._hWnds["msgbox"]).center(*wm.screensize)
				return True
			else:
				if not self.task.stage: self.task.stage = 1
				return self.init_(evt, wm)
		return False

	def init_(self, evt, wm):
		if self.task.stage == 1:
			self._activated = False
			return super(GymLeaderNPC, self).init(evt, wm)
		elif self.task.stage == 2:
			_button_size = self.wmacros.button_size[:]
			self._hWnds["msgbox"] =  wm.CreateWindow(self.wmacros.WC_MSGBOX,
			 ((400, 200), None, self.task.name, None, None, None,
			  "You ve already fought with me.  ",
			  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_OK
			  , [_button_size[0]//2, _button_size[1]//2]))
			wm.SetTopmost(self._hWnds["msgbox"], True)
			wm.getInstance(self._hWnds["msgbox"]).center(*wm.screensize)
			return True
		return True

	def render(self, evt, wm):
		if self._activated and self.task.stage == 1:
			t = super(GymLeaderNPC, self).render(evt, wm)
			if not self.dbox:
				self.task.stage = 2
				self.task.done = True
				self.player.info["accomplishment"].append(self.acc)
			return t
		elif self._activated:
			return self.render_(evt, wm)
		return self.render_scene()

	def render_(self, evt, wm):
		if self.task.stage == 0:
			if wm.getMsg(self._hWnds["msgbox"]) == self.wmacros.IDOK:
				wm.SetTopmost(-1, False)
				self.release(wm)
		elif self.task.stage == 2:
			try:
				if wm.getMsg(self._hWnds["msgbox"]) == self.wmacros.IDOK:
					wm.SetTopmost(-1, False)
					self.release(wm)
			except:
				pass
		return self.render_scene()

	def release(self, wm):
		if self.task.stage == 1 and self.uBattle.lastwinner == DEF:
			# Lost Battle, Reset Task
			self.task.stage = 0
			self.task.done = False
		return super(GymLeaderNPC, self).release(wm)

class ServiceNPC(NPC_Skeleton):
	def __init__(self, pos, res_walk, text, title="ServiceNPC"):
		super(ServiceNPC, self).__init__(pos, res_walk)
		self.player = None
		self.text = text
		self.title = title

	def setPlayer(self, player):
		self.player = player

	def init(self, evt, wm):
		if not self._activated:
			self._activated = True
			_button_size = self.wmacros.button_size[:]
			self._hWnds["msgbox"] =  wm.CreateWindow(self.wmacros.WC_MSGBOX,
			 ((400, 200), None, self.title, None, None, None,
			  self.text,
			  self.wmacros.MB_ICONINFORMATION | self.wmacros.MB_YESNO
			  , [_button_size[0]//2, _button_size[1]//2]))
			wm.SetTopmost(self._hWnds["msgbox"], True)
			wm.getInstance(self._hWnds["msgbox"]).center(*wm.screensize)
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			if wm.getMsg(self._hWnds["msgbox"]) == self.wmacros.IDYES:
				self.apply(self.player, True)
				wm.SetTopmost(-1, False)
				self.release(wm)
			elif wm.getMsg(self._hWnds["msgbox"]) == self.wmacros.IDNO:
				self.apply(self.player, False)
				wm.SetTopmost(-1, False)
				self.release(wm)
		return self.render_scene()

	def apply(self, player, bResult):
		if bResult:
			pass
		else:
			pass


class TransmissionNPC(ServiceNPC):
	def __init__(self, pos, res_walk, text, title="To Somewhere", newPos=(0, 0), cost=0):
		text += "\nThis will cost you %d gold.  "%int(cost)
		super(TransmissionNPC, self).__init__(pos, res_walk, text, title)
		self.cost = int(cost)
		self.newPos = newPos

	def apply(self, player, bResult):
		global direction
		if bResult:
			if player.money >= self.cost:
				player.money -= self.cost
				player.setPos(*self.newPos)
				self.LoadMap(player.getPos())
				direction = []
		else:
			pass


class RecoveryNPC(ServiceNPC):
	def __init__(self, pos, res_walk, text, title="Recovery"):
		super(RecoveryNPC, self).__init__(pos, res_walk, text, title)
		self.cost = 0
		self.text_sav = self.text[:]

	def init(self, evt, wm):
		self.cost = 100
		for i in self.player.pokemon:
			if i.level >= 50: self.cost += (i.maxhp-i.hp)*i.level
		if self.cost == 100: self.cost = 0
		self.text = self.text_sav + "\nThis will cost you %d gold.  "%self.cost
		return super(RecoveryNPC, self).init(evt, wm)

	def apply(self, player, bResult):
		if bResult:
			if player.money >= self.cost:
				player.money -= self.cost
				for i in self.player.pokemon:
					i.load(i.tID, i.exp, i.name, changeid=i.id)
		else:
			pass


class ComputerNPC(NPC_Skeleton):    # save/load pokemons
	def __init__(self, pos, res_walk):
		super(NPC_Skeleton, self).__init__(pos, res_walk)
		self._hWnds = {"in backpack": 0, "in computer": 0}
		self.hClass = 0

	def _create_in_backpack(self, wm, surf):
		if wm.isWindowPresent(self._hWnds["in backpack"]): wm.DestroyWindow(self._hWnds["in backpack"])
		info = []
		for i in self.player.pokemon:
			info.append((i.name+" Lv. %d"%i.level, i.id))
		p = 25*len(info)
		if p < 300: p = 300
		self._hWnds["in backpack"] = wm.CreateWindow(
				self.hClass,
				(
				(wm.screensize[0]//2, 300), surf, (wm.screensize[0]//2, p),
				info,
				)
						  )
		wm.MoveWindow(self._hWnds["in backpack"], 0, 25)

	def _create_in_computer(self, wm, surf):
		if wm.isWindowPresent(self._hWnds["in computer"]): wm.DestroyWindow(self._hWnds["in computer"])
		info = []
		for i in self.player.pokemon_save:
			info.append((i.name+" Lv. %d"%i.level, i.id))
		p = 25*len(info)
		if p < 300: p = 300
		self._hWnds["in computer"] = wm.CreateWindow(
				self.hClass,
				(
				(wm.screensize[0]//2, 300), surf, (wm.screensize[0]//2, p),
				info,
				)
						  )
		wm.MoveWindow(self._hWnds["in computer"], wm.screensize[0]//2, 25)

	def init(self, evt, wm):
		if not self._activated:
			import backpack
			if not self.hClass: self.hClass = wm.RegisterCompleteClass(backpack.uiBackpack_scroll)
			self._activated = True

			self._hWnds["return"] = wm.CreateWindow(self.wmacros.WC_BUTTON, ((100, 20), None, "Return"))
			wm.MoveWindow(self._hWnds["return"], 100, 400)

			self._hWnds["text_in_backpack"] = wm.CreateWindow(self.wmacros.WC_TEXT,
				((wm.screensize[0]//2, 25), None, "In Backpack",
				pygame.font.SysFont('Times New Romen', 16),
				True, (255, 255, 255)), True)
			wm.MoveWindow(self._hWnds["text_in_backpack"], 0, 0)

			self._hWnds["text_in_computer"] = wm.CreateWindow(self.wmacros.WC_TEXT,
				((wm.screensize[0]//2, 25), None, "In Computer",
				pygame.font.SysFont('Times New Romen', 16),
				True, (255, 255, 255)), True)
			wm.MoveWindow(self._hWnds["text_in_computer"], wm.screensize[0]//2, 0)

			surf = pygame.Surface((400, 300), pygame.SRCALPHA)
			surf.fill((0, 0, 0, 255//2))

			self._create_in_backpack(wm, surf)
			self._create_in_computer(wm, surf)
			return True
		return False

	def render(self, evt, wm):
		if self._activated:
			for i in self._hWnds:
				umsg = wm.getMsg(self._hWnds[i])
				if i == "return" and umsg == self.wmacros.HIT:
					self.release(wm)
					break
				elif i == "in backpack" and umsg != 0:
					self.player.savePokemon(umsg)
					surf = pygame.Surface((400, 300), pygame.SRCALPHA)
					surf.fill((0, 0, 0, 255//2))
					self._create_in_backpack(wm, surf)
					self._create_in_computer(wm, surf)
				elif i == "in computer" and umsg != 0:
					self.player.loadPokemon(umsg)
					surf = pygame.Surface((400, 300), pygame.SRCALPHA)
					surf.fill((0, 0, 0, 255//2))
					self._create_in_backpack(wm, surf)
					self._create_in_computer(wm, surf)
		return self.render_scene()

	def release(self, wm):
		for i in self._hWnds:
			wm.DestroyWindow(self._hWnds[i])
		self._hWnds = {"in backpack": 0, "in computer": 0}
		self._activated = False


# pos(terrain)->tuple: pEvent/inh. class, init_args
playerEvent = {}
# load these npcs before game starts # (x, y): npc_object
npcs = {}
# load these maps before game starts # (terrain, starting_offset) # remember to call init first
maps = []

import os

Blaine = rgine.read_buffer(os.path.join('resources','sprites','Blaine'), 96, 128)
Brock = rgine.read_buffer(os.path.join('resources','sprites','Brock'), 96, 128)
Erika = rgine.read_buffer(os.path.join('resources','sprites','Erika'), 96, 128)
Giovanni = rgine.read_buffer(os.path.join('resources','sprites','Giovanni'), 96, 128)
Koga = rgine.read_buffer(os.path.join('resources','sprites','Koga'), 96, 128)
Lt_Surge = rgine.read_buffer(os.path.join('resources','sprites','Lt Surge'), 96, 128)
Misty = rgine.read_buffer(os.path.join('resources','sprites','Misty'), 96, 128)
Sabrina = rgine.read_buffer(os.path.join('resources','sprites','Sabrina'), 96, 128)
StoreOwner=rgine.read_buffer(os.path.join('resources','sprites','StoreOwner'), 96, 128)

surf = rgine.read_buffer("pic1", 96, 128)
pos = (9, 9)


npcs[(-5, -5)] = ConversationNPC(pos, res_walk(surf, 3, 4, 0)[0],
								  [
										  "Everyone has a dream that fills their heart, \n"
										  "A journey they must take, \n"
										  "A destiny to fulfill. \n"
										  "As close as your imagination exists a wonderful place where wondrous "
										  "creatures with incredible powers help make dreams come true. \n"
										  "It's the world of Pokemon. \n",

										  "Welcome to the world of Pokemon! \n"
										  "A new Pokemon is now in your backpack! Get Ready! ",
								  ],
								  "Opening Statement",
)
npcs[(-6, -6)] = ConversationNPC(pos, res_walk(surf, 3, 4, 0)[0],
								  [
										  "You were killed. ",
										  "Your body was thrown in the field. ",
								          "Months later ...\n"
								          "Nobody would ever remember ...\n",
								          "Because ...\n",
								          "There are just too many of 'you' ...\n",
								          "With a dream, but failed ...\n",
								          "Game Over ... \n...\n...\nEnd of file is reached. ",
								  ],
								  "EOF",
)

import Combinedv2 as cdv2
pos = (9, 10)
it = cdv2.Item("Pokeball",0, 200, 0)
it2 = cdv2.Item("Great Ball",0, 600, 0)
it3 = cdv2.Item("Ultra Ball",0, 1200, 0)
it4 = cdv2.Item("Master Ball",0,10000,0)
it5 = cdv2.Item("Potion",0, 300, 100)
it6 = cdv2.Item("Super Potion",0, 700, 100)
it7 = cdv2.Item("Hyper Potion",0, 1200, 100)
it8 = cdv2.Item("Max Potion",0, 2500, 100)
it9 = cdv2.Item("Fire Stone", 0, 1200, 0)
it10 = cdv2.Item("Thunder Stone", 0, 1200, 0)
it11 = cdv2.Item("Water Stone", 0, 1200, 0)
it12 = cdv2.Item("Leaf Stone", 0, 1200, 0)
it13 = cdv2.Item("Moon Stone", 0, 1200, 0)
selling = {it.getInfo()[0]:it, it2.getInfo()[0]:it2,
                                                                   it3.getInfo()[0]:it3, it4.getInfo()[0]:it4,
                                                                   it5.getInfo()[0]:it5, it6.getInfo()[0]:it6, it7.getInfo()[0]:it7,
                                                                   it8.getInfo()[0]:it8, it9.getInfo()[0]:it9,
                                                                   it10.getInfo()[0]:it10, it11.getInfo()[0]:it11,
                                                                   it12.getInfo()[0]:it12}

pos = (10, 10)

t = cdv2.Pokemon()
t.load(1, 500)

npcs[(8, 25)] = GymLeaderNPC(pos, res_walk(Brock, 3, 4, 0)[0], 1, [],
                               [["I'm Brock! I'm Pewter's Gym Leader! I believe in rock hard defense and "
                                 "determination! That's why my Pokémon are all the Rock-type!","Do you still want to "
                                 "challenge me? Fine then! Show me your best!"], ["I took you for granted. As proof of your victory, here's the Boulder Badge!"]],
                         cdv2.gLeader[1][0][0], cdv2.gLeader[1][2][0],
                         cdv2.Player(cdv2.gLeader[1][1], [], "name", 0, 0))

npcs[(221, 223)] = GymLeaderNPC(pos, res_walk(Misty, 3, 4, 0)[0], 2, [],
                               [["Hi, you're a new face! Trainers who want to turn pro have to "
                                 "have a policy about Pokémon! What's your policy on Pokémon? "
                                 "What is your approach? My policy is an all-out offensive with water-type Pokémon! "
                                 "Misty, the world-famous beauty, is your host! Are you ready, sweetie?"], ["Wow! You're too much! All right! You can have the Cascade Badge to show you beat me!"
]],
                         cdv2.gLeader[2][0][0], cdv2.gLeader[2][2][0],
                         cdv2.Player(cdv2.gLeader[2][1], [], "name", 0, 0))

npcs[(107,19)] = GymLeaderNPC(pos, res_walk(Erika, 3, 4, 0)[0], 3, [],
                               [["Hello. Lovely weather isn't it? It's so pleasant. ...Oh dear... I must have dozed off. "
                                 "Welcome. My name is Erika. I am the Leader of Celadon Gym. I teach the art of flower arranging. "
                                 "My Pokémon are of the grass-type. Oh, I'm sorry, I had no idea that you wished to challenge me. "
                                 "Very well, but I shall not lose."], ["Oh! I concede defeat. You are remarkably strong. I must confer you the Rainbow Badge." ]],
                         cdv2.gLeader[3][0][0], cdv2.gLeader[3][2][0],
                         cdv2.Player(cdv2.gLeader[3][1], [], "name", 0, 0))

npcs[(214, 502)] = GymLeaderNPC(pos, res_walk(Lt_Surge, 3, 4, 0)[0], 4, [],
                               [["Hey, kid! What do you think you're doing here? You won't live long in combat! "
                                 "That's for sure! I tell you kid, electric Pokémon saved me during the war! "
                                 "They zapped my enemies into paralysis! The same as I'll do to you!"], ["Whoa! You're the real deal, kid! Fine then, take the Thunder Badge!"]],
                         cdv2.gLeader[4][0][0], cdv2.gLeader[4][2][0],
                         cdv2.Player(cdv2.gLeader[4][1], [], "name", 0, 0))

npcs[(214, 20)] = GymLeaderNPC(pos, res_walk(Koga, 3, 4, 0)[0], 6, [],
                               [["Fwahahaha! A mere child like you dares to challenge me? Very well, I shall show you true terror as a ninja master! "
                                 "You shall feel the despair of poison and sleep techniques!" ], ["Humph! You have proven your worth! Here! take the Soul Badge!" ]],
                         cdv2.gLeader[6][0][0], cdv2.gLeader[6][2][0],
                         cdv2.Player(cdv2.gLeader[6][1], [], "name", 0, 0))

npcs[(4, 3)] = GymLeaderNPC(pos, res_walk(Sabrina, 3, 4, 0)[0], 5, [],
                               [[ "I had a vision of your arrival! I have had psychic powers since I was a little child. "
                                  "I first learned to bend spoons with my mind. I dislike fighting, but if you wish, I will show you my powers!" ], ["I'm shocked! But a loss is a loss. I admit I didn't work hard enough to win! You earned the Marsh Badge!" ]],
                         cdv2.gLeader[5][0][0], cdv2.gLeader[5][2][0],
                         cdv2.Player(cdv2.gLeader[5][1], [], "name", 0, 0))

npcs[(210, 415)] = GymLeaderNPC(pos, res_walk(Blaine, 3, 4, 0)[0], 7, [],
                               [["Hah! I'm Blaine! I am the Leader of Cinnabar Gym! My fiery Pokémon will incinerate all challengers!"
                                 "Hah! You better have Burn Heal!" ], ["I've burnt out! You have earned the Volcano Badge!" ]],
                         cdv2.gLeader[7][0][0], cdv2.gLeader[7][2][0],
                         cdv2.Player(cdv2.gLeader[7][1], [], "name", 0, 0))

npcs[(24, 426)] = GymLeaderNPC(pos, res_walk(Giovanni, 3, 4, 0)[0], 8, [],
                               [["So! I must say, I am impressed you got here!"
                                 "You shall face Giovanni, the greatest trainer!"], ["Ha! That was a truly intense fight! You have won! As proof, here is the Earth Badge!" ]],
                         cdv2.gLeader[8][0][0], cdv2.gLeader[8][2][0],
                         cdv2.Player(cdv2.gLeader[8][1], [], "name", 0, 0))


npcs[(6, 3)] = TransmissionNPC(pos, res_walk(StoreOwner, 3, 4, 0)[0],
                               "You want to goto Ice place? ", "Guide", (1, 301), 100)
npcs[(1, 300)] = TransmissionNPC(pos, res_walk(StoreOwner, 3, 4, 0)[0],
                                 "Do You Want To Transfer? ", "To Downtown", (5, 3), 100)

npcs[(7, 503)] = NPC(pos, res_walk(StoreOwner, 3, 4, 0)[0])
npcs[(7, 504)] = RecoveryNPC(pos, char_walk(0), "Do You Want To Recover All Your Pokemons? ")
npcs[(10, 502)] = ComputerNPC(pos, char_walk(0))
npcs[(101, 503)] = NPC(pos, res_walk(StoreOwner, 3, 4, 0)[0])
npcs[(101, 503)].chgDir(RIGHT)
npcs[(101, 503)].setStaticDir(True)
npcs[(102, 503)] = ShopNPC(pos, char_walk(0), selling)


npcs[(107, 603)] = NPC(pos, res_walk(StoreOwner, 3, 4, 0)[0])
npcs[(107, 604)] = RecoveryNPC(pos, char_walk(0), "Do You Want To Recover All Your Pokemons? ")
npcs[(110, 602)] = ComputerNPC(pos, char_walk(0))
npcs[(201, 603)] = NPC(pos, res_walk(StoreOwner, 3, 4, 0)[0])
npcs[(201, 603)].chgDir(RIGHT)
npcs[(201, 603)].setStaticDir(True)
npcs[(202, 603)] = ShopNPC(pos, char_walk(0), selling)
