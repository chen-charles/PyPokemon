import pygame

import rgine as rgine

Tsize = 11

t = rgine.Terrain("r")


screen = pygame.display.set_mode((Tsize*32, Tsize*32))
surf = pygame.Surface(screen.get_size())

t.readTerrain("myTerrain.terrain")
t.setTextureFormat(32, 32)      #must call this before reading a texture file
t.readTextureFromFile("myTexture.texture")
t.render(surf)


evt = rgine.Event()

pygame.font.init()
wm = rgine.windows.WindowsManager()
winm = rgine.windows.WindowsMacros()
hButton0 = wm.CreateWindow(winm.WC_BUTTON, ((158, 59), rgine.windows._button, "Button 0",
												  pygame.font.SysFont('Times New Romen', 16),
												  True, (255, 255, 255)), True)
hButton1 = wm.CreateWindow(winm.WC_BUTTON, ((158, 59), rgine.windows._button, "Button 1",
												  pygame.font.SysFont('Times New Romen', 16),
												  True, (255, 255, 255)), True)
wm.MoveWindow(hButton1, 158//2, 59//2)
hButton2 = wm.CreateWindow(winm.WC_BUTTON, ((158, 59), rgine.windows._button, "Button 2",
												  pygame.font.SysFont('Times New Romen', 16),
												  True, (255, 255, 255)), True)
wm.MoveWindow(hButton2, 158, 59)

img = t.getTexture(2)
print(rgine.int2bool(t.getProperty(0, 0)))
while True:
	evt.update()
	if evt.type == pygame.QUIT:
		break
	if evt.isKeyHit(pygame.K_ESCAPE):    # escape
		break
	if evt.isKeyDown("t"):
		t.setTexture(pygame.Surface((32, 32)), 2)
	else:
		t.setTexture(img, 2)
	t.render(surf)
	screen.blit(surf, (0, 0))
	for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
		screen.blit(surface, pos)
		if hWnd == hButton0 and msg == winm.HIT:
			print("Button 0 Hit!")
		elif hWnd == hButton1 and msg == winm.HIT:
			print("Button 1 Hit!")
		elif hWnd == hButton2 and msg == winm.HIT:
			print("Button 2 Hit!")
	pygame.display.flip()

pygame.quit()
