#Charles-Jianye Chen 2014

import pygame
import rgine

def getImages(img, sizeX, sizeY):
    x, y = img.get_size()
    for sy in range(0, y, sizeY):
        for sx in range(0, x, sizeX):
            yield img.subsurface(pygame.Rect(sx, sy, sizeX, sizeY)).copy()
            
def run(img, width, height):
    global terrain
    terrain = rgine.Terrain("w", 0, 0, width, width)
    j = 0
    for i in getImages(img, width, height):
        terrain.setTexture(i, j)
        j += 1


fname = input("-> Input Filename\n")
width = int(input("-> Input Width\n"))
height = int(input("-> Input Height\n"))
screen = pygame.display.set_mode((width, height))
img = pygame.image.load(fname).convert_alpha()
pygame.display.quit()
run(img, width, height)
print("-> Running ... ")
terrain.writeTextureToFile("%s.texture"%fname)
print(img.get_width()//width, img.get_height()//height)
input("-> Done! Enter To Exit ... ")
