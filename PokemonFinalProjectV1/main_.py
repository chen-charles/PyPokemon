import cProfile

import pygame

p = cProfile.Profile()

import rgine as rgine

p.enable()


Tsize = 11

t = rgine.Terrain("w")
t.init(Tsize, Tsize, 32, 32)
surf = pygame.Surface((32, 32))

surf.fill((255, 255, 255))
t.setTexture(surf.copy(), 0)

surf.fill((0, 0, 0))
t.setTexture(surf.copy(), 1)

t.setTexture(surf, 2)

for x, y in zip(range(0, Tsize), range(0, Tsize)):
	t.modify(x, y, 1)
	t.modify(x, Tsize-1-y, 1)
	t.modify(Tsize//2, y, 2)
	t.modify(x, Tsize//2, 2)

screen = pygame.display.set_mode((Tsize*32, Tsize*32))

img = pygame.image.load("try.png").convert_alpha()
t.setTexture(img, 0)

surf = pygame.Surface(screen.get_size(), pygame.HWSURFACE)
##t.render(surf)


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
prpty = [True, True, True, False, True, True, True, True]
print(prpty)
t.setProperty(0, 0, rgine.bool2int(prpty))

running = True
while running:
	evt.update()
	if evt.type == pygame.QUIT:
		running = False
	if evt.isKeyHit(pygame.K_ESCAPE):    # escape
		running = False
	if evt.isKeyDown(pygame.K_t):
		t.setTexture(pygame.Surface((32, 32)), 2)
	else:
		t.setTexture(img, 2)
	t.render(surf, (0, 0), range(0, 5), range(5, 10))
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

print(t.getTerrainByRelativeRect((32, 32, 32, 33)))
print(t.getRelativeClientRect(3, 3))
print(t.getTerrainByRelativeRect(t.getRelativeClientRect(3, 3)))

t.writeTerrain("myTerrain.terrain")
t.writeTextureToFile("myTexture.texture")

pygame.quit()
p.disable()
p.print_stats(sort='tottime')
