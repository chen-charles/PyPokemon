import pygame

import rgine as rgine


#globals

def init_terrain(terrain_name, texture_name, is_display_mode_set=True):
	terrain = rgine.Terrain("r", 32, 32)
	terrain.readTerrain(terrain_name)
	terrain.readTextureFromFile(texture_name)
	if is_display_mode_set:
		terrain.convert_alpha()
	return terrain

def test(property_byte, digit):
	return rgine.byte2bool(bytes([property_byte]))[digit]

screen = pygame.display.set_mode((16*50, 9*50))
terrain = init_terrain("myTerrain.terrain", "myTexture.texture", True)
evt = rgine.Event()

print(test(terrain.getProperty(0, 0), 0))
wm = rgine.windows.WindowsManager()
_button_size = [158, 59]
msgbox = wm.CreateWindow(rgine.windows.WindowsMacros.WC_MSGBOX,
			 ((400, 200), None, "Welcome!", None, None, None,
			  "Hello! Welcome to the world of Pokemon!",
			  # rgine.windows.WindowsMacros.MB_ICONWARNING | rgine.windows.WindowsMacros.MB_CANCELTRYCONTINUE
              rgine.windows.WindowsMacros.MB_OK
			  , [_button_size[0]//2, _button_size[1]//2]))
wm.MoveWindow(msgbox, 200, 200)
while True:
	evt.update()
	if evt.type == pygame.QUIT: break
	screen.fill((0, 0, 0))
	terrain.render(screen)
	for hWnd, msg, surface, pos in wm.DispatchMessage(evt):
		screen.blit(surface, pos)
		if hWnd == msgbox:
			if msg != rgine.windows.WindowsMacros.IDNORESULT:
				print("Messagebox %d !"%msg)
	pygame.display.flip()
pygame.quit()
