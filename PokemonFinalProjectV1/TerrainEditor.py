__author__ = 'Charles-Jianye Chen'
import pygame
import ctypes
import wapisp

MB_ICONQUESTION = 0x00000020
MB_ICONINFORMATION = 0x00000040
import time
pygame.init()
import rgine as rgine


def getTerrainByPos(terrain, mouseX, mouseY, shiftX, shiftY):
		a, b = terrain.getTerrainByRelativeRect((mouseX-shiftX, mouseY-shiftY, 0, 0))
		return a[0], b[0]

textureSize = 32
TsizeW, TsizeH = 15, 15
textureFileName = "outside.png.texture"
textureInfo = \
	{
	"width": 8,
	"height": 469,
	}

terrainFileName = "8x469_ordered"


tRead = rgine.Terrain("r", textureSize, textureSize)
tWrite = rgine.Terrain("w", TsizeW, TsizeH, textureSize, textureSize)

tRead.readTextureFromFile(textureFileName)
tRead.readTerrain(terrainFileName)
wRead = rgine.TerrainWorld(textureInfo["width"]*textureSize, textureInfo["height"]*textureSize)
wRead.setTextureFormat(textureSize, textureSize)
wRead.setProjectionSize(8*textureSize, 20*textureSize)
tRead.render(wRead.getSurface())


tWrite.readTextureFromFile(textureFileName)
wWrite = rgine.TerrainWorld(TsizeW*textureSize, TsizeH*textureSize)
wWrite.setTextureFormat(textureSize, textureSize)
wWrite.setProjectionSize(12*textureSize, 12*textureSize)
tWrite.render(wWrite.getSurface())

screen = pygame.display.set_mode((16*50, 9*50))
hPygameWindow = pygame.display.get_wm_info()["window"]

evt = rgine.Event()
wm = rgine.windows.WindowsManager()
wmacro = rgine.windows.WindowsMacros()
wmbuttons = dict()

buttons = ["New", "Open - Read", "Open - Write", "Semi-Finalize", "Finalize", "About", "Quit"]
for i in range(len(buttons)):
	t = wm.CreateWindow(wmacro.WC_BUTTON, ((158//2, 59//2), rgine.windows._button,buttons[i]))
	wm.MoveWindow(t, 158//2*i+10*i, 0)
	wmbuttons[t] = buttons[i]
wm.SetTopmost(-1, False)

wReadOffset = (0, 30)
wWriteOffset = (400, 30)
wReadRect = pygame.Rect(*(wReadOffset+wRead.getSize()))
wWriteRect = pygame.Rect(*(wWriteOffset+wWrite.getSize()))
CurrentIdentifier = []
running = True

selectedR = [(0, 0), (0, 0)]
# selectedW = [(0, 0), (0, 0)]
while running:
	evt.update()
	if evt.type == pygame.QUIT:
		uret = wapisp.MessageBox(hPygameWindow, "Are you sure? ", "Quit",
				  wapisp.MB_YESNO | MB_ICONQUESTION)
		if uret == wapisp.IDYES:
			running = False
	screen.fill((0, 0, 0))

	rgx, rgy = wRead.getTerrainRange()
	pygame.draw.rect(wRead.getSurface(), (0, 0, 0), wRead.getRect(), 0)
	tRead.render_s(wRead.getSurface(), wRead.getShift(), range(*rgx), range(*rgy))
	screen.blit(wRead.render_s(), wReadOffset)

	rgx, rgy = wWrite.getTerrainRange()
	# pygame.draw.rect(wWrite.getSurface(), (0, 0, 0), wWrite.getRect(), 0)
	tWrite.render_s(wWrite.getSurface(), wWrite.getShift(), range(*rgx), range(*rgy))
	screen.blit(wWrite.render_s(), wWriteOffset)


	mx, my = evt.getMousePos()
	# getRelativeClientRect
	# pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(), 1)
	if wReadRect.collidepoint(evt.getMousePos()):
		sx, sy = wReadOffset
		wsx, wsy = wRead.getShift()
		tpos = getTerrainByPos(tRead, mx+wsx, my+wsy, sx, sy)
		x, y, w, h = wRead.transform(tRead.getRelativeClientRect(*tpos))
		pygame.draw.rect(screen, (255, 0, 0), (x+wReadOffset[0], y+wReadOffset[1], w, h), 1)
		a, b = selectedR
		x, y, w, h = wRead.transform(tRead.getRelativeClientRect((a[0], b[0]+1), (a[1], b[1]+1)))
		t = tRead.getRelativeClientRect(*selectedR)
		if selectedR != [(0, 0), (0, 0)]:
			pygame.draw.rect(screen, (0, 0, 255), (x+wReadOffset[0], y+wReadOffset[1], w, h), 1)
		if evt.isMouseHit(evt.MOUSE_LEFT):
			selectedR = [tpos, tpos]
		elif evt.isMouseDown(evt.MOUSE_LEFT):
			selectedR[1] = tpos
		elif evt.isMouseUp(evt.MOUSE_LEFT):
			selectedR[1] = tpos
			xrange = selectedR[0][0], selectedR[1][0]+1
			yrange = selectedR[0][1], selectedR[1][1]+1
			CurrentIdentifier = []
			selectedR = [(0, 0), (0, 0)]
			for x in range(*xrange):
				CurrentIdentifier.append([])
				for y in range(*yrange):
					CurrentIdentifier[-1].append(tRead.getIdentifier(x, y))

	elif wWriteRect.collidepoint(evt.getMousePos()):
		selectedR = [(0, 0), (0, 0)]

		sx, sy = wWriteOffset
		wsx, wsy = wWrite.getShift()
		tpos = getTerrainByPos(tWrite, mx+wsx, my+wsy, sx, sy)
		x, y, w, h = wWrite.transform(tWrite.getRelativeClientRect(*tpos))
		pygame.draw.rect(screen, (255, 0, 0), (x+wWriteOffset[0], y+wWriteOffset[1], w, h), 1)

		if evt.isMouseDown(evt.MOUSE_LEFT):
			x, y = tpos
			for tx in range(len(CurrentIdentifier)):
				for ty in range(len(CurrentIdentifier[tx])):
					tWrite.setIdentifier_s(x+tx, y+ty, CurrentIdentifier[tx][ty])
	else:
		selectedR = [(0, 0), (0, 0)]


	if evt.isMouseHit(evt.MOUSE_SCROLL_UP) and evt.isKeyDown(pygame.K_LSHIFT):
		if wReadRect.collidepoint(evt.getMousePos()):
			wRead.shiftH(-textureSize)
		elif wWriteRect.collidepoint(evt.getMousePos()):
			wWrite.shiftH(-textureSize)

	elif evt.isMouseHit(evt.MOUSE_SCROLL_UP):
		if wReadRect.collidepoint(evt.getMousePos()):
			wRead.shiftV(-textureSize)
		elif wWriteRect.collidepoint(evt.getMousePos()):
			wWrite.shiftV(-textureSize)

	if evt.isMouseHit(evt.MOUSE_SCROLL_DOWN) and evt.isKeyDown(pygame.K_LSHIFT):
		if wReadRect.collidepoint(evt.getMousePos()):
			wRead.shiftH(textureSize)
		elif wWriteRect.collidepoint(evt.getMousePos()):
			wWrite.shiftH(textureSize)

	elif evt.isMouseHit(evt.MOUSE_SCROLL_DOWN):
		if wReadRect.collidepoint(evt.getMousePos()):
			wRead.shiftV(textureSize)
		elif wWriteRect.collidepoint(evt.getMousePos()):
			wWrite.shiftV(textureSize)

	for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
		screen.blit(surface, pos)
		if hWnd in wmbuttons and msg == wmacro.HIT:
			wm.SetTopmost(-1, False)

			if wmbuttons[hWnd] == "New":
				tWrite.init(TsizeW, TsizeH, textureSize, textureSize)
				wWrite.new()
				tWrite.render(wWrite.getSurface(), [0, 0])

			elif wmbuttons[hWnd] == "Open - Read":
				strfilter = ".texture file\x00*.texture\x00.jpeg image file\x00*.jpeg\x00\x00"
				wapisp.MessageBox(hPygameWindow, "Terrain file first, then .texture/.jpeg file.  ", wmbuttons[hWnd])
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

				tRead.readTerrain(terrainfname)

				if fname.split(".")[-1].lower() == "jpeg":
					surf = pygame.image.load(fname)
					surf.convert_alpha()
					tRead.readTextureFromSurface(surf)
				elif fname.split(".")[-1].lower() == "texture":
					tRead.readTextureFromFile(texturefname)
				else:
					raise ValueError(fname)
				tRead.render_check()
				wRead.resize(tRead.width*tRead.textureW, tRead.height*tRead.textureH)
				sx = tRead.width*tRead.textureW
				sy = tRead.height*tRead.textureH
				wRead.resize(sx, sy)
				if sx > wRead.getRect()[2]:
					sx = wRead.getRect()[2]
				if sy > wRead.getRect()[3]:
					sy = wRead.getRect()[3]
				wRead.setProjectionSize(sx, sy)
				tRead.render(wRead.getSurface())
				wReadRect = pygame.Rect(*(wReadOffset+wRead.getSize()))

			elif wmbuttons[hWnd] == "Open - Write":
				strfilter = ".texture file\x00*.texture\x00.jpeg image file\x00*.jpeg\x00\x00"
				wapisp.MessageBox(hPygameWindow, "Terrain file first, then .texture/.jpeg file.  ", wmbuttons[hWnd])
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

				tWrite.readTerrain(terrainfname)

				if fname.split(".")[-1].lower() == "jpeg":
					surf = pygame.image.load(fname)
					surf.convert_alpha()
					tWrite.readTextureFromSurface(surf)
				elif fname.split(".")[-1].lower() == "texture":
					tWrite.readTextureFromFile(texturefname)
				else:
					raise ValueError(fname)

				tWrite.render_check()
				sx = tWrite.width*tWrite.textureW
				sy = tWrite.height*tWrite.textureH
				wWrite.resize(sx, sy)
				if sx > wWrite.getRect()[2]:
					sx = wWrite.getRect()[2]
				if sy > wWrite.getRect()[3]:
					sy = wWrite.getRect()[3]
				wWrite.setProjectionSize(sx, sy)
				tWrite.render(wWrite.getSurface())
				wWriteRect = pygame.Rect(*(wWriteOffset+wWrite.getSize()))
			elif wmbuttons[hWnd] == "Semi-Finalize":
				temp = wapisp.MessageBox(hPygameWindow, "This could take a while, "
								 "depends on the terrain size. \n"
								 "You will receive another msgbox for notification. \n\n"
								 "Confirm to start. \n\n"
								 "Note that Semi-Finalization could only use .texture format. ", wmbuttons[hWnd],
						  wapisp.MB_OKCANCEL| MB_ICONINFORMATION)
				if temp == wapisp.IDCANCEL: continue

				wapisp.MessageBox(hPygameWindow, "Optional Texture Property File", wmbuttons[hWnd], wapisp.MB_OK)
				result, fname = wapisp.GetOpenFileName(hPygameWindow)
				if not result:
					pass
				else:
					tWrite.readTextureProperty(fname)
					tWrite.applyTextureProperty()

				ct = int(time.time())
				temp = tWrite.semi_finalize(wWrite.getSurface())
				temp.writeTerrain("%d.terrain"%ct)
				temp.writeTextureToFile("%d.texture"%ct)

				wapisp.MessageBox(hPygameWindow, "Done! ", wmbuttons[hWnd])
			elif wmbuttons[hWnd] == "Finalize":
				uret = wapisp.MessageBox(hPygameWindow, "Do you want to save it as a jpeg file?\n"
								 "Note that it will be extremely fast and small-sized "
								 "to save textures as a jpeg file, "
								 "but you won't be able to load it by readTextureFromFile().\n"
								 "Instead, you will have to load it by pygame.image first, "
								 "then call readTextureFromSurface() to initialize.  ", wmbuttons[hWnd],
						  wapisp.MB_YESNO | MB_ICONQUESTION)
				if uret != wapisp.IDYES and uret != wapisp.IDNO: continue

				wapisp.MessageBox(hPygameWindow, "Optional Texture Property File", wmbuttons[hWnd], wapisp.MB_OK)
				result, fname = wapisp.GetOpenFileName(hPygameWindow)
				if not result:
					pass
				else:
					tWrite.readTextureProperty(fname)
					tWrite.applyTextureProperty()
					print(tWrite.getProperty(0, 0))

				temp = wapisp.MessageBox(hPygameWindow, "This could take a while, "
								 "depends on the terrain size. \n"
								 "You will receive another msgbox for notification. \n\n"
								 "Confirm to start. ", wmbuttons[hWnd],
						  wapisp.MB_OKCANCEL| MB_ICONINFORMATION)
				if temp == wapisp.IDCANCEL: continue

				ct = int(time.time())
				temp = tWrite.finalize(wWrite.getSurface())
				temp.writeTerrain("%d.terrain"%ct)

				if uret == wapisp.IDYES:
					pygame.image.save(temp.writeTextureToSurface(), "%d.jpeg"%ct)
				else:
					temp.writeTextureToFile("%d.texture"%ct)

				wapisp.MessageBox(hPygameWindow, "Done! ", wmbuttons[hWnd])

			elif wmbuttons[hWnd] == "About":
				wapisp.MessageBox(hPygameWindow, "Terrain Editor 1.0 RC2\n"
								 "Powered by Python, Pygame\n"
								 "Tested on Windows 7 (x64) with Python (x86) 3.2.5, Pygame 1.9.2a0\n"
                                                                 "Thanks to Raymond-Jeffery Li\n"
								 "By Charles-Jianye Chen 2014", wmbuttons[hWnd], MB_ICONINFORMATION)

			elif wmbuttons[hWnd] == "Quit":
				uret = wapisp.MessageBox(hPygameWindow, "Are you sure? ", wmbuttons[hWnd],
						  wapisp.MB_YESNO | MB_ICONQUESTION)
				if uret == wapisp.IDYES:
					running = False
	pygame.draw.rect(screen, (0, 255, 0), wReadRect, 1)
	pygame.draw.rect(screen, (0, 255, 0), wWriteRect, 1)
	pygame.display.flip()
pygame.quit()
