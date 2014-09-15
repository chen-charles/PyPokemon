import os
import inspect
import pickle
import pygame
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
f = open(path+os.sep+"__DEBUG__", "rb")
__DEBUG__ = f.read(1)[0]
f.close()

if __DEBUG__:
		from common import *
		import exception
		import buildinfo
		from surface_buffer import *
else:
		from rgine.common import *
		import rgine.exception as exception
		import rgine.buildinfo as buildinfo
		from rgine.surface_buffer import *


##if __name__ == "__main__": _version_ = buildinfo.bump("terrain", 1)
##else: _version_ = buildinfo.get("terrain")
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
_version_ = buildinfo.get(path+"/terrain")


'''
Exp. File Format Details

Terrain->Storage
byte0~7		: terrain loader version info ->unsigned int 64
byte8~16	: terrain size x ->unsigned int 64
byte16~24	: terrain size y ->unsigned int 64
byte24~   	:
			byte0:  	terrain properties	->8 bits
			byte1~3:	terrain resource identifier	->unsigned int 16

Texture->Storage    (pygame.Surface)    ->  must init the video mode first
(TextureID follows x)
--------    ->  0 1 2 3 4 5 6 7
--------    ->  8 9 10 11 12 13 14 15

Texture->Storage    (fname)   ->  could be load before the video mode is set
byte0~7		: texture loader version info ->unsigned int 64
byte8~16	: texture size x ->unsigned int 64
byte16~24	: texture size y ->unsigned int 64
byte24~     :
			byte0~4:    RGBA
(TextureID follows x)
--------    ->  0 1 2 3 4 5 6 7
--------    ->  8 9 10 11 12 13 14 15
'''

def Terrain(mode="r", *init_args):
	"""
	Returns terrain instance.
	if len(init_args) is 2: implicitly call setTextureFormat() for mode "r" only.
	if len(init_args) is 4: implicitly call init() for mode "w" only.
	:str mode:
	:*args init_args:
	:return specific type of terrain instance:
	:raise ValueError if mode is neither "r" nor "w":
	"""
	if mode == "r": return _terrainR(*init_args)
	elif mode == "w": return _terrainW(*init_args)
	else: raise ValueError("mode should be either 'r' or 'w'")

class _terrainBase(object):
	# Base Object for both R/W
	def __init__(self):
		"""
		Initializes all variables.
		"""
		self._data = []
		self._texture = {}
		self._texture_prpty = {}
		self.width = 0
		self.height = 0
		self.textureW = 0
		self.textureH = 0
		self.sx = 0
		self.sy = 0

	def setShift(self, sx, sy):
		self.sx = sx
		self.sy = sy

	def writeTextureProperty(self, fname):
		with open(fname, "wb") as f:
			f.write(pickle.dumps(self._texture_prpty))
		return fname

	def readTextureProperty(self, fname):
		with open(fname, "rb") as f:
			self._texture_prpty = pickle.loads(f.read())
		return fname

	def setTextureProperty(self, identifier, prpty):
		self._texture_prpty[identifier] = prpty

	def getTextureProperty(self, identifier):
		if identifier in self._texture_prpty: return self._texture_prpty[identifier]
		return None

	def generateTextureProperty(self):
		data = self._data
		for x in range(len(data)):
			for y in range(len(data[x])):
				tid, prpty = data[x][y]
				self._texture_prpty[tid] = prpty

	def applyTextureProperty(self):
		data = self._data
		for x in range(len(data)):
			for y in range(len(data[x])):
				tid, prpty = data[x][y]
				if tid in self._texture_prpty:
					data[x][y][1] = self._texture_prpty[tid]

	def writeTerrainProperty(self, fname):
		f = open(fname, "wb")
		li = []
		for y in range(self.height):
			for x in range(self.width):
				li.append(bytes([self.getProperty_s(x, y)]))
		f.write(b''.join(li))
		return fname

	def readTerrainProperty(self, fname):
		f = open(fname, "rb")
		s = f.read()
		f.close()
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				self.setProperty_s(x, y, s[i])
				i += 1
		return i
	
	def setTextureFormat(self, textureWidth, textureHeight):
		"""
		Must be called before reading and rendering.  Could be called implicitly by giving args to Terrain() or init().
		:int textureWidth:
		:int textureHeight:
		"""
		self.textureW = textureWidth
		self.textureH = textureHeight

	def render_check(self):
		s = pygame.Surface((self.textureW, self.textureH))
		for x in range(self.width):
			for y in range(self.height):
				if self._data[x][y][0] not in self._texture:
					self._texture[self._data[x][y][0]] = s

	def render_s(self, Surface, startpt=[0, 0], range_w=None, range_h=None):
		if range_w is None: range_w = range(self.sx, self.width+self.sx)
		if range_h is None: range_h = range(self.sy, self.height+self.sy)
		startpt = list(startpt)
		sx, sy = startpt
		s = pygame.Surface((self.textureW, self.textureH))
		for y in range_h:
			for x in range_w:
				try:
					Surface.blit(self._texture[self._data[x-self.sx][y-self.sy][0]], startpt)
				except:
					Surface.blit(s, startpt)
				startpt[0] += self.textureW
			startpt[0] = sx
			startpt[1] += self.textureH
			
	def render(self, Surface, startpt=[0, 0], range_w=None, range_h=None):
		"""
		Renders on the specific surface from startpt, w/h is for terrain coords.
		:pygame.Surface Surface:
		:tuple/list startpt:
		:range range_w:
		:range range_h:
		"""
		if range_w is None: range_w = range(self.sx, self.width+self.sx)
		if range_h is None: range_h = range(self.sy, self.height+self.sy)
		startpt = list(startpt)
		sx, sy = startpt
		for y in range_h:
			for x in range_w:
				Surface.blit(self._texture[self._data[x-self.sx][y-self.sy][0]], startpt)
				startpt[0] += self.textureW
			startpt[0] = sx
			startpt[1] += self.textureH

	def getProperty(self, x, y):
		"""
		Returns the property of the specific terrain.
		:int x:
		:int y:
		:return int:
		"""
		return self._data[x-self.sx][y-self.sy][1]

	def setProperty(self, x, y, prpty_int):
		"""
		Sets the property of the specific terrain.
		:int x:
		:int y:
		:int prpty_int:
		"""
		self._data[x-self.sx][y-self.sy][1] = prpty_int

	def getIdentifier(self, x, y):
		"""
		Returns the identifier of the texture on the specific terrain.
		:int x:
		:int y:
		:return int:
		"""
		return self._data[x-self.sx][y-self.sy][0]

	def setIdentifier(self, x, y, identifier):
		"""
		Sets the identifier of the texture on the specific terrain.
		:int x:
		:int y:
		:int identifier:
		"""
		self._data[x-self.sx][y-self.sy][0] = identifier
		
	def getProperty_s(self, x, y):
		"""
		Returns the property of the specific terrain.
		:int x:
		:int y:
		:return int:
		"""
		if self.sx <= x < self.width+self.sx and self.sy <= y < self.height+self.sy:
			return self._data[x-self.sx][y-self.sy][1]
		else:
			return None

	def setProperty_s(self, x, y, prpty_int):
		"""
		Sets the property of the specific terrain.
		:int x:
		:int y:
		:int prpty_int:
		"""
		if self.sx <= x < self.width+self.sx and self.sy <= y < self.height+self.sy:
			self._data[x-self.sx][y-self.sy][1] = prpty_int
			return True
		return False

	def getIdentifier_s(self, x, y):
		"""
		Returns the identifier of the texture on the specific terrain.
		:int x:
		:int y:
		:return int:
		"""
		if self.sx <= x < self.width+self.sx and self.sy <= y < self.height+self.sy:
			return self._data[x-self.sx][y-self.sy][0]
		else:
			return None

	def setIdentifier_s(self, x, y, identifier):
		"""
		Sets the identifier of the texture on the specific terrain.
		:int x:
		:int y:
		:int identifier:
		"""
		if self.sx <= x < self.width+self.sx and self.sy <= y < self.height+self.sy:
			self._data[x-self.sx][y-self.sy][0] = identifier
			return True
		return False
		
	def getTexture(self, identifier):
		"""
		Gets the texture by the given identifier.
		:int identifier:
		:return pygame.Surface:
		"""
		return self._texture[identifier]

	def setTexture(self, Surface, identifier):
		"""
		Sets the specific texture to the given identifier(for rendering and exporting).
		:pygame.Surface Surface:
		:int identifier:
		"""
		self._texture[identifier] = Surface

	def getRelativeClientRect(self, x, y):
		"""
		Gets the relative rect for specific (range) of terrain.
		Note that x & y could only be either both integer, or both range_type list ([start, end])
		:int/list x:
		:int/list y:
		:return pygame.Rect:
		"""
		if (isinstance(x, list) and isinstance(y, list)) or (isinstance(x, tuple) and isinstance(y, tuple)):
			x1, x2 = x
			x1 -= self.sx
			x2 -= self.sx
			y1, y2 = y
			y1 -= self.sy
			y2 -= self.sy
			return pygame.Rect(x1*self.textureW, y1*self.textureH,
							   self.textureW*abs(x2-x1), self.textureH*abs(y2-y1))
		else:
			return pygame.Rect(x*self.textureW, y*self.textureH, self.textureW, self.textureH)

	def getAbsoluteClientRect(self, x, y, shiftX, shiftY):
		"""
		Gets the absolute rect for specific (range) of terrain.
		Note that x & y could only be either both integer, or both range_type list ([start, end])
		:int/list x:
		:int/list y:
		:int shiftX:
		:int shiftY:
		:return pygame.Rect:
		"""
		x, y, w, h = self.getRelativeClientRect(x, y)
		return pygame.Rect(x+shiftX, y+shiftY, w, h)

	def getTerrainByRelativeRect(self, rect):
		"""
		Gets the range of terrain x & y by relative rect.
		:pygame.Rect/tuple/list rect:
		:return [x_start, x_end], [y_start, y_end]:
		"""
		x, y, w, h = rect
		x //= self.textureW
		y //= self.textureH
		if w%self.textureW:
			w = ((w+self.textureW)//self.textureW)
		else:
			w //= self.textureW

		if h%self.textureH:
			h = ((h+self.textureH)//self.textureH)
		else:
			h //= self.textureH

		return [x+self.sx, x+w+self.sx], [y+self.sy, y+h+self.sy]


class _terrainR(_terrainBase):
	def __init__(self, *init_args):
		super(_terrainR, self).__init__()
		if len(init_args) == 2:
			self.setTextureFormat(*init_args)
		self._img_texture = pygame.Surface((0, 0), pygame.SRCALPHA)

	def readTerrain(self, fname):
		"""
		Reads the terrain file generated by _terrainW.writeTerrain()
		:str fname:
		:raise exception.error if terrain file version/size mismatched (which means the given file has an error):
		"""
		hFile = open(fname, "rb")
		info = hFile.read(8*3)
		ver, tx, ty = [info[n:n+8] for n in range(0,24,8)]
		if raw2struct(ver, uint64).uint != raw2struct(_version_, uint64).uint:
			hFile.close()
			raise exception.error("Terrain File Version Mismatched.  ", ValueError)
		self._data = []
		tx, ty = raw2struct(tx, uint64).uint, raw2struct(ty, uint64).uint
		for x in range(tx):
			self._data.append([])
			for y in range(ty):
				d = hFile.read(3)
				if not d:
					self._data = []
					hFile.close()
					raise exception.error("Terrain File Size Mismatched.  ", ValueError)
				self._data[-1].append([raw2struct(d[1:], uint).uint, d[0]])
		hFile.close()
		self.width = tx
		self.height= ty

	def readTextureFromSurface(self, surface):
		"""
		Reads the textures from the given surface.  The textures will be ordered by x change -> y change.
		:pygame.Surface surface:
		"""
		self._texture = {}
		i = 0
		for y in range(0, surface.get_height(), self.textureH):
			for x in range(0, surface.get_width(), self.textureW):
				self._texture[i] = surface.subsurface((x, y, self.textureW, self.textureH))
				i += 1

	def readTextureFromFile(self, fname):
		"""
		Reads the texture file generated by _terrainW.writeTextureToFile()
		:str fname:
		:return: :raise exception.error if terrain file version mismatched:
		"""
		hFile = open(fname, "rb")
		info = hFile.read(8*3)
		ver, tx, ty = [info[n:n+8] for n in range(0,24,8)]
		if raw2struct(ver, uint64).uint != raw2struct(_version_, uint64).uint:
			hFile.close()
			raise exception.error("Texture File Version Mismatched.  ", ValueError)
		tx, ty = raw2struct(tx, uint64).uint, raw2struct(ty, uint64).uint
		self._img_texture = pygame.image.frombuffer(hFile.read(), (tx, ty), "RGBA")
		return self.readTextureFromSurface(self._img_texture)

	def convert_alpha(self):
		self._img_texture.convert_alpha()

class _terrainW(_terrainR):
	def __init__(self, *init_args):
		super(_terrainW, self).__init__()
		if len(init_args) == 4: self.init(*init_args)

	def init(self, width, height, textureWidth, textureHeight):
		"""
		Must be called before any operations.  Could be called implicitly by giving args to Terrain().
		:int width:
		:int height:
		:int textureWidth:
		:int textureHeight:
		"""
		self.width = width
		self.height= height
		self._data = [[[0,0]for i in range(height)] for i in range(width)]
		self.setTextureFormat(textureWidth, textureHeight)

	def modify(self, x, y, identifier=-1, Property=-1):
		"""
		Modifys the terrain by x, y.
		:int x:
		:int y:
		:int (texture) identifier:
		:int (terrain) Property:
		:return:
		"""
		if identifier == -1 and Property == -1: return
		elif identifier == -1: self._data[x][y][1] = Property
		elif Property == -1: self._data[x][y][0] = identifier
		else: self._data[x][y] = [identifier, Property]

	def writeTerrain(self, fname):
		"""
		Writes the terrain to the specific file.
		:str fname:
		"""
		hFile = open(fname, "wb")

		hFile.write(_version_)
		hFile.write(struct2raw(uint64(self.width)))
		hFile.write(struct2raw(uint64(self.height)))

		for x in self._data:
			for y in x:
				hFile.write(
					struct2raw(byte(y[1]))
					+
					struct2raw(uint16(y[0]))
					)

		hFile.close()

	def writeTextureToSurface(self):
		"""
		Writes textures to a pygame.Surface(SRCALPHA).
		:return pygame.Surface:
		"""
		m = int(((max(self._texture.keys()))**0.5))+1
		surface = pygame.Surface((m*self.textureW, m*self.textureH), pygame.SRCALPHA)
		s = pygame.Surface((self.textureW, self.textureH))
		x = 0
		y = 0
		j = 0
		while y < m*self.textureH:
			if j in self._texture:
				surface.blit(self._texture[j], (x*self.textureW, y))
			else:
				surface.blit(s, (x*self.textureW, y))
			if x >= m-1:
				x = 0
				y += self.textureH
			else:
				x += 1
			j += 1
		return surface

	def writeTextureToFile(self, fname):
		"""
		Writes the textures to the specific file.
		:str fname:
		"""
		surface = self.writeTextureToSurface()
		save_buffer(fname+".temp", surface)
		
		hFile = open(fname, "wb")
		hFile.write(_version_)
		hFile.write(struct2raw(uint64(surface.get_width())))
		hFile.write(struct2raw(uint64(surface.get_height())))
		
		tempfile = open(fname+".temp", "rb")
		hFile.write(tempfile.read())
		tempfile.close()
		os.remove(fname+".temp")
		hFile.close()

	def semi_finalize(self, surface):
		"""
		Semi-Finalizes the working terrain, generates new texturefile to avoid ppa issues.
		YOU CAN LOAD IT WITH THE TEXTURE FILES WHICH HAVE LESS TEXTURES THEN THE CURRENT TEXTURE.
		Note that the orders of textures are changed.
		Returns the newly created _terrainW object.
		:pygame.Surface surface:
		:str fname:
		:str texturefname:
		:return _terrainW object:
		"""

		t = Terrain("w", self.width, self.height, self.textureW, self.textureH)
		i = len(self._texture)+1
		for y in range(self.height):
			for x in range(self.width):
				t.setProperty_s(x, y, self.getProperty_s(x, y))
				t.setIdentifier(x, y, i)
				i += 1

		def getImages(img, sizeX, sizeY):
			x, y = img.get_size()
			for sy in range(0, y, sizeY):
				for sx in range(0, x, sizeX):
					yield img.subsurface(pygame.Rect(sx, sy, sizeX, sizeY)).copy()

		k = list(self._texture.keys())
		k.sort()
		for i in k:
			t.setTexture(self._texture[i], i)

		j = len(self._texture)+1
		for i in getImages(surface, self.textureW, self.textureH):
			t.setTexture(i, j)
			j += 1

		return t

	def finalize(self, surface):
		"""
		Finalizes the working terrain, generates new texturefile to avoid ppa issues.
		Note that the orders of textures are changed.
		Returns the newly created _terrainW object.
		:pygame.Surface surface:
		:str fname:
		:str texturefname:
		:return _terrainW object:
		"""

		t = Terrain("w", self.width, self.height, self.textureW, self.textureH)
		i = 0
		for y in range(self.height):
			for x in range(self.width):
				t.setProperty_s(x, y, self.getProperty_s(x, y))
				t.setIdentifier(x, y, i)
				i += 1
				
		def getImages(img, sizeX, sizeY):
			x, y = img.get_size()
			for sy in range(0, y, sizeY):
				for sx in range(0, x, sizeX):
					yield img.subsurface(pygame.Rect(sx, sy, sizeX, sizeY)).copy()

		j = 0
		for i in getImages(surface, self.textureW, self.textureH):
			t.setTexture(i, j)
			j += 1

		return t


# class AnimatedTerrain():
# 	pass

def _main(): return 0
if __name__ == "__main__": exit(_main())
