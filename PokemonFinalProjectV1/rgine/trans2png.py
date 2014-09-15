#Create Surface Buffer
#Pygame, Python 3.2.5
#Designed by Charles-Jianye Chen 2014

import os
import pygame


def save_buffer(filename, surface):
	t = open(filename,"wb")
	buf = surface.get_buffer()
	print(buf.length)
	t.write(buf.raw)
	del buf
	return surface.get_size()


def read_buffer(filename, width, height, fmt="RGBA"):
	t = open(filename, "rb")
	p = t.read()
	print(len(p))
	img = pygame.image.frombuffer(p, (width, height), fmt)
	t.close()
	return img


def _main():
	print("You Need To Have A Dot Before File Format.  Make Sure The Specific File Exists.  ")
	try:
		uin = input("->fname? ")
		screen = pygame.display.set_mode((640, 360))
		surf = pygame.image.load(uin)
		pygame.image.save(surf, "".join(uin.split(".")[:-1])+".tga")
	finally:
		pygame.display.quit()
	return 0

if __name__ == "__main__": exit(_main())
