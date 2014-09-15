#Create Surface Buffer
#Pygame, Python 3.2.5
#Designed by Charles-Jianye Chen 2014

import os
import inspect

import pygame

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def save_buffer(filename, surface):
	t = open(filename, "wb")
	buf = surface.get_buffer()
	t.write(buf.raw)
	del buf
	os.system("\""+path+"\\rgine_bgra2rgba.exe\" %s"%filename)
	return surface.get_size()

def read_buffer(filename, width, height, fmt="RGBA"):
	t = open(filename, "rb")
	p = t.read()
	img = pygame.image.frombuffer(p, (width, height), fmt)
	t.close()
	return img


def _main():
	print("You Need To Have A Dot Before File Format.  Make Sure The Specific File Exists.  ")
	try:
		uin = input("->fname? ")
		ref = pygame.image.load("x.png")
		screen = pygame.display.set_mode((640, 360))
		screen.fill((255, 255, 255))
		surf = pygame.image.load(uin).convert_alpha()
		screen.blit(surf, (0, 0))
		while True:
			if pygame.event.poll().type == pygame.QUIT: break
			pygame.display.flip()
		print(save_buffer("".join(uin.split(".")[:-1]), surf))
		screen.fill((255, 255, 255))
		t = read_buffer("".join(uin.split(".")[:-1]), surf.get_width(), surf.get_height(), "RGBA")
		screen.blit(t, (0, 0))
		while True:
			if pygame.event.poll().type == pygame.QUIT: break
			pygame.display.flip()
	finally:
		pygame.display.quit()
	return 0

if __name__ == "__main__": exit(_main())
