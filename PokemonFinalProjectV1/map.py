import pygame
from base import *
import Combinedv2 as libpkmon
import os

_scrsize = [0, 0]
_texturesize = 0
EleLand1 = None
GrassLand1 = None
GrassLand2 = None
IceLand = None
LavaLand1 = None
LavaLand2 = None
OpenWater1 = None
RockLand1 = None
RockLand2 = None
RockWater = None

def init(scrsize, texturesize, bBG_path):
	global _scrsize, _texturesize
	global EleLand1, GrassLand1, GrassLand2, IceLand, LavaLand1, LavaLand2, OpenWater1, RockLand1, RockLand2, RockWater
	_scrsize = scrsize[:]
	_texturesize = texturesize
	EleLand1 = pygame.image.load(bBG_path+os.sep+"EleLand1.png").convert_alpha()
	GrassLand1 = pygame.image.load(bBG_path+os.sep+"GrassLand1.png").convert_alpha()
	GrassLand2 = pygame.image.load(bBG_path+os.sep+"GrassLand2.png").convert_alpha()
	IceLand = pygame.image.load(bBG_path+os.sep+"IceLand.png").convert_alpha()
	LavaLand1 = pygame.image.load(bBG_path+os.sep+"LavaLand1.png").convert_alpha()
	LavaLand2 = pygame.image.load(bBG_path+os.sep+"LavaLand2.png").convert_alpha()
	OpenWater1 = pygame.image.load(bBG_path+os.sep+"OpenWater1.png").convert_alpha()
	RockLand1 = pygame.image.load(bBG_path+os.sep+"RockLand1.png").convert_alpha()
	RockLand2 = pygame.image.load(bBG_path+os.sep+"RockLand2.png").convert_alpha()
	RockWater = pygame.image.load(bBG_path+os.sep+"RockWater.png").convert_alpha()

class MapManager(object):
	def __init__(self):
		self.maps = {}
		self._current = None
		self._link = {}

	def add(self, map_inst):
		self.maps[tuple(map_inst.getRect())] = map_inst

	def getMap(self, uPos):
		for i in self.maps:
			if pygame.Rect(*i).collidepoint(*uPos):
				return self.maps[i]
		raise ValueError(uPos)

	def setMap(self, uPos):
		for i in self.maps:
			if pygame.Rect(*i).collidepoint(*uPos):
				self._current = i
				return self.maps[i]
		raise ValueError(uPos)

	def getCurrentMap(self):
		return self.maps[self._current]

	def setLink(self, link):
		self._link = link # uPos: (direction, newPos)

	def addLink(self, uPos, direction, newPos, bothway=True):
		self._link[tuple(uPos)] = [direction, tuple(newPos)]
		if bothway:
			if direction == pygame.K_UP: direction = pygame.K_DOWN
			elif direction == pygame.K_DOWN: direction = pygame.K_UP
			elif direction == pygame.K_LEFT: direction = pygame.K_RIGHT
			else: direction = pygame.K_LEFT
			self._link[tuple(newPos)] = [direction, tuple(uPos)]

	def isSwitchMap(self, uPos, direction):
		if tuple(uPos) in self._link and self._link[tuple(uPos)][0] == direction: return self._link[tuple(uPos)][1]
		return None


MAP_TYPE_NONE = 0
MAP_TYPE_GRASS = 1
MAP_TYPE_GRASSWATER = 2
MAP_TYPE_ICE = 3
MAP_TYPE_ROCK = 4
MAP_TYPE_ROCKWATER = 5
MAP_TYPE_FIRE = 6
MAP_TYPE_GHOST = 7
MAP_TYPE_ELECTRIC = 8

levelBasic = [8,15]
levelAdv = [40,60]
levelLeg = [60,100]


#Map 1-9:
#Grass=Normal grass
#GrassWater= water/sand on map
grassBasic=[10,16,19,21,23,29,32,43,46,48,52,56,69,77,83,84,
			102,108,114,123,127,128,133,143,143,48,102,63,92,96,1]
grassAdv=[1,12,15,18,20,25,24,43,57,70]
grassLeg=[150]

grassWaterBasic=[54,60,72,98,116,118,120,129]
grassWaterAdv=[55,72,7,1,49,64]
grassWaterLeg=[144]

#Map 10-11:
#Ice=Ice

iceBasic=[41,79,86,124]
iceAdv=[42,80,87]
iceLeg=[144]

#Map 12-13
#Roc=Rock
#RocWater = Water on map

rocBasic=[27,41,46,50,66,74,95,104,111,115,132,142,147]
rocAdv=[74,75]
rocLeg=[151]
rocWaterBasic=[72,79,86,90,129,131,138,140]
rockWaterAdv=[139,141]

#Map 14-15
#Fire

fireBasic=[37,58,77,95]
fireAdv=[126,136,4]
fireLeg=[146]

#Map16
#Ghost

ghoBasic=[48,102,63,92,96]
ghoAdv=[49,122,65]
ghoLeg=[150, 151]

#Map Electric
#Ele=Electric

eleBasic=[16,19,21,81,88,100,101,132,137]
eleAdv=[17,22]
eleLeg=[145]

class Map(object):
	def __init__(self, terrain, starting_oft, battle_lv_rli=[5000, 50000], typ=MAP_TYPE_NONE):
		self.sx, self.sy = starting_oft
		self.terrain = terrain
		self.terrain.setShift(*starting_oft)

		self.world = rgine.TerrainWorld(terrain.width*terrain.textureW, terrain.height*terrain.textureH)
		self.world.setProjectionSize(*_scrsize)
		self.world.setTextureFormat(_texturesize, _texturesize)
		self.world.setTerrainShift(*starting_oft)

		self.battle_lv_rli = battle_lv_rli
		self._link = {}

		self._mtyp = typ
		self._restrict_r = None

		if self._mtyp == MAP_TYPE_ROCK or self._mtyp == MAP_TYPE_ROCKWATER:
			self.restrictView(50)

	def getRect(self):
		return pygame.Rect(self.sx, self.sy, self.terrain.width, self.terrain.height)

	def getPos(self):
		return self.sx, self.sy

	def getType(self):
		return self._mtyp

	def setType(self, mtyp):
		self._mtyp = mtyp

	def getBattleBk(self):
		if self._mtyp == MAP_TYPE_NONE:
			return None
		elif self._mtyp == MAP_TYPE_GRASS:
			return GrassLand1
		elif self._mtyp == MAP_TYPE_GRASSWATER:
			return OpenWater1
		elif self._mtyp == MAP_TYPE_ICE:
			return IceLand
		elif self._mtyp == MAP_TYPE_ROCK:
			return RockLand1
		elif self._mtyp == MAP_TYPE_ROCKWATER:
			return RockWater
		elif self._mtyp == MAP_TYPE_FIRE:
			return LavaLand1
		elif self._mtyp == MAP_TYPE_GHOST:
			return None
		elif self._mtyp == MAP_TYPE_ELECTRIC:
			return EleLand1
		else:
			return None

	def getWildPlayer(self):
			x = random.randint(1,1000)
			result = 0
			if self._mtyp == MAP_TYPE_NONE:
					raise ValueError("No Battle Should Present In This Map! ")
			elif self._mtyp == MAP_TYPE_GRASS:
					if x<980: result = random.choice(grassBasic)
					elif x>=980 and x != 1000: result = random.choice(grassAdv)
					elif x == 1000: result = random.choice(grassLeg)
			elif self._mtyp == MAP_TYPE_GRASSWATER:
					if x<980: result = random.choice(grassWaterBasic)
					elif x>=980 and x != 1000: result = random.choice(grassWaterAdv)
					elif x == 1000: result = random.choice(grassWaterLeg)
			elif self._mtyp == MAP_TYPE_ICE:
					if x<980: result = random.choice(iceBasic)
					elif x>=980 and x != 1000: result = random.choice(iceAdv)
					elif x == 1000: result = random.choice(iceLeg)
			elif self._mtyp == MAP_TYPE_ROCK:
					if x<980: result = random.choice(rocBasic)
					elif x>=980 and x != 1000: result = random.choice(rocAdv)
					elif x == 1000: result = random.choice(rocLeg)
			elif self._mtyp == MAP_TYPE_ROCKWATER:
					if x<980: result = random.choice(rocWaterBasic)
					elif x>=980 and x != 1000: result = random.choice(rocWaterAdv)
					elif x == 1000: result = random.choice(rocLeg)
			elif self._mtyp == MAP_TYPE_FIRE:
					if x<980: result = random.choice(fireBasic)
					elif x>=980 and x != 1000: result = random.choice(fireAdv)
					elif x == 1000: result = random.choice(fireLeg)
			elif self._mtyp == MAP_TYPE_GHOST:
					if x<980: result = random.choice(ghoBasic)
					elif x>=980 and x != 1000: result = random.choice(ghoAdv)
					elif x == 1000: result = random.choice(ghoLeg)
			elif self._mtyp == MAP_TYPE_ELECTRIC:
					if x<980: result = random.choice(eleBasic)
					elif x>=980 and x != 1000: result = random.choice(eleAdv)
					elif x == 1000: result = random.choice(eleLeg)
			else:
					result = 1
			lv = 1
			if x < 980: lv = random.randint(*levelBasic)*500
			elif x >= 980 and x != 1000: lv = random.randint(*levelAdv)*500
			elif x == 1000: lv = random.randint(*levelLeg)*500
			t = libpkmon.Pokemon()
			t.load(result, lv)
			return libpkmon.Player([t], [], "name", 0, 0, libpkmon.TYPE_WILD)


	def restrictView(self, r):
		self._restrict_r = r

	def getRestriction(self):
		return self._restrict_r
