__author__ = 'Charles-Jianye Chen'
import os
import time

import pygame

import wapisp




pygame.init()
import rgine as rgine

_ok = rgine.surface_buffer.read_buffer("ok", 32, 32)
_cross = rgine.surface_buffer.read_buffer("cross", 32, 32)

def getTerrainByPos(terrain, mouseX, mouseY, shiftX, shiftY):
		a, b = terrain.getTerrainByRelativeRect((mouseX-shiftX, mouseY-shiftY, 0, 0))
		return a[0], b[0]

def test(property_byte, digit):
	return rgine.byte2bool(bytes([property_byte]))[digit]

screen = pygame.display.set_mode((16*2*32, 9*2*32))
terrainFilename = "1402018449.terrain"
# textureFilename = "myTexture.texture"
textureSize = 32
terrain = rgine.Terrain("w", 0, 0, textureSize, textureSize)
terrain.readTerrain(terrainFilename)
terrain.readTextureFromSurface(pygame.image.load("1402018449.jpeg").convert_alpha())
##terrain.readTextureFromFile(textureFilename)
textureInfo = \
	{
	"width": terrain.width,
	"height": terrain.height,
	}

evt = rgine.Event()
wm = rgine.windows.WindowsManager()

wmbuttons = {}
wmacro = rgine.windows.WindowsMacros()
buttons = ["Open", "Save", "[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]"]
for i in range(len(buttons)):
	t = wm.CreateWindow(wmacro.WC_BUTTON, ((158//2, 59//2), wmacro.button, buttons[i]))
	wm.MoveWindow(t, 158//2*i, 0)
	wmbuttons[t] = buttons[i]
wm.SetTopmost(-1, False)

##screen = pygame.display.set_mode((16*50, 9*50))
hPygameWindow = pygame.display.get_wm_info()["window"]

world = rgine.TerrainWorld(textureInfo["width"]*textureSize, textureInfo["height"]*textureSize)
world.setTextureFormat(textureSize, textureSize)

wOffset = (0, 32)
world.setProjectionSize(16*2*32-wOffset[0], 9*2*32-wOffset[1])
wRect = pygame.Rect(*(wOffset+world.getSize()))

changed = True
CurrentDigit = 0
while True:
	evt.update()
	if evt.type == pygame.QUIT:
		break

	screen.fill((0, 0, 0))
	world.new()
	rgx, rgy = world.getTerrainRange()
	terrain.render_s(world.getSurface(), world.getShift(), range(*rgx), range(*rgy))
	screen.blit(world.render_s(), wOffset)

	for x in range(*rgx):
		for y in range(*rgy):
			px, py, w, h = terrain.getRelativeClientRect(x, y)
			px += wOffset[0]
			py += wOffset[1]
			px -= world.getShift()[0]
			py -= world.getShift()[1]
			t = terrain.getProperty_s(x, y)
			if t is None: continue
			if test(t, CurrentDigit):
				screen.blit(_ok, (px, py))
			else:
				screen.blit(_cross, (px, py))

	if evt.isMouseHit(evt.MOUSE_LEFT):
		if wRect.collidepoint(evt.getMousePos()):
			wsx, wsy = world.getShift()
			x, y = getTerrainByPos(*[terrain]+[evt.getMousePos()[0]+wsx, evt.getMousePos()[1]+wsy]+list(wOffset))
			t = terrain.getProperty_s(x, y)
			if t is not None:
				li = rgine.int2bool(t)
				li[CurrentDigit] = not li[CurrentDigit]
				terrain.setProperty(x, y, rgine.bool2int(li))



	if evt.isMouseHit(evt.MOUSE_SCROLL_UP) and evt.isKeyDown(pygame.K_LSHIFT):
		if wRect.collidepoint(evt.getMousePos()):
			world.shiftH(-textureSize)

	elif evt.isMouseHit(evt.MOUSE_SCROLL_UP):
		if wRect.collidepoint(evt.getMousePos()):
			world.shiftV(-textureSize)

	if evt.isMouseHit(evt.MOUSE_SCROLL_DOWN) and evt.isKeyDown(pygame.K_LSHIFT):
		if wRect.collidepoint(evt.getMousePos()):
			world.shiftH(textureSize)

	elif evt.isMouseHit(evt.MOUSE_SCROLL_DOWN):
		if wRect.collidepoint(evt.getMousePos()):
			world.shiftV(textureSize)

	for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
		screen.blit(surface, pos)
		if hWnd in wmbuttons and msg == wmacro.HIT:
			wm.SetTopmost(-1, False)
			if wmbuttons[hWnd] == "Open":
				strfilter = ".texture file\x00*.texture\x00.jpeg image file\x00*.jpeg\x00\x00"
				wapisp.MessageBox(hPygameWindow, "Terrain file first, then .texture/.jpeg file, and optional terrainProperty file. ", wmbuttons[hWnd])
				result, fname = wapisp.GetOpenFileName(hPygameWindow)
				if not result:
					continue
				else:
					terrainfname = fname
					
				result, fname = wapisp.GetOpenFileName(hPygameWindow, strfilter)
				if not result:
					continue
				else:
					texturefname = fname

				terrain.readTerrain(terrainfname)

				if fname.split(".")[-1].lower() == "jpeg":
					surf = pygame.image.load(fname)
					surf.convert_alpha()
					terrain.readTextureFromSurface(surf)
				elif fname.split(".")[-1].lower() == "texture":
					terrain.readTextureFromFile(texturefname)
				else:
					raise ValueError(fname)


				result, fname = wapisp.GetOpenFileName(hPygameWindow)
				if not result:
					pass
				else:
					terrain.readTerrainProperty(fname)

					
				terrain.render_check()
				
				world.resize(terrain.width*terrain.textureW, terrain.height*terrain.textureH)
				sx = terrain.width*terrain.textureW
				sy = terrain.height*terrain.textureH
				world.resize(sx, sy)
				if sx > world.getRect()[2]:
					sx = world.getRect()[2]
				if sy > world.getRect()[3]:
					sy = world.getRect()[3]
				world.setProjectionSize(sx, sy)
				terrain.render(world.getSurface())
				wRect = pygame.Rect(*(wOffset+world.getSize()))
				
			elif wmbuttons[hWnd] == "Save":
				fname = terrain.writeTerrainProperty(str(int(time.time()))+".terrainProperty")
				wapisp.MessageBox(hPygameWindow, "Done. Filename is %s"%fname, wmbuttons[hWnd])
				
			elif wmbuttons[hWnd] == "[0]":
				CurrentDigit = 0
			elif wmbuttons[hWnd] == "[1]":
				CurrentDigit = 1
			elif wmbuttons[hWnd] == "[2]":
				CurrentDigit = 2
			elif wmbuttons[hWnd] == "[3]":
				CurrentDigit = 3
			elif wmbuttons[hWnd] == "[4]":
				CurrentDigit = 4
			elif wmbuttons[hWnd] == "[5]":
				CurrentDigit = 5
			elif wmbuttons[hWnd] == "[6]":
				CurrentDigit = 6
			elif wmbuttons[hWnd] == "[7]":
				CurrentDigit = 7

	pygame.display.flip()
pygame.quit()
