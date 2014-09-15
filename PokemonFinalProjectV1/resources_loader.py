import pygame

FRONT_LEFT_RIGHT_BACK = 0
LLLBBBBRRRRFFFFL = 1
RET_RAW = 0xff

class char_walk():
	def __init__( self, typ, *init_FLRB ):
		if typ == FRONT_LEFT_RIGHT_BACK:
			if not init_FLRB:
				t = pygame.Surface((0, 0))
				self.back = self.right = self.front = self.left = [t, t, t]
				return
			self.front = init_FLRB[0]
			self.left = init_FLRB[1]
			self.right= init_FLRB[2]
			self.back = init_FLRB[3]
		elif typ == LLLBBBBRRRRFFFFL:
			if not init_FLRB:
				t = pygame.Surface((0, 0))
				self.Lfront = self.Rfront = self.Rback = self.Lback = self.back = self.right = self.front = self.left = [t, t, t]
				return
			self.left = init_FLRB[0]
			self.Lback= init_FLRB[1]
			self.back = init_FLRB[2]
			self.Rback= init_FLRB[3]
			self.right= init_FLRB[4]
			self.Rfront=init_FLRB[5]
			self.front= init_FLRB[6]
			self.Lfront=init_FLRB[7]
		else:
			raise ValueError()

def res_walk( img, wObj = 3, hObj = 4, arrg =  RET_RAW ):
	dx = img.get_width()//wObj
	dy = img.get_height()//hObj

	if arrg == RET_RAW:
		imgs = []
		for y in range(hObj):
			for x in range(wObj):
				imgs.append(img.subsurface(pygame.Rect(x*dx, y*dy, dx, dy)).copy())
	else:
		imgs = [[]for i in range (hObj)]
		for y in range(hObj):
			for x in range(wObj):
				imgs[y].append(img.subsurface(pygame.Rect(x*dx, y*dy, dx, dy)).copy())
		imgs = char_walk(arrg, *imgs)
	return imgs, (dx, dy)


if __name__ == "__main__":
	import time
	screen = pygame.display.set_mode((1,1))
	t=res_walk("CH20287.png",8,8,LLLBBBBRRRRFFFFL)
	screen = pygame.display.set_mode(t[1])
	tlen=8
	i=0
	while True:
		time.sleep(0.1)
		if pygame.event.poll().type == pygame.QUIT:break
		screen.fill((255,255,255))
		screen.blit(t[0].front[i], (0,0))
		i+=1
		if i == tlen: i=0
		pygame.display.flip()

	pygame.quit()
