#Progressbar.py
import pygame
#====================================================================================================
class Progressbar(object):
    _percentage = 0
    _color = (0,0,0)
    _size = 0
    _surfacesize = (0,0)
    _style = -1
    
    def __init__(self,surfacesize=(0,0),color=(0,0,0),size=0,percentage=0,style=-1):
        self._surfacesize = surfacesize
        self._color = color
        self._size = size
        self._percentage = percentage
        if isinstance(style,int):
            self._style = style
        else:
            try:
                if style.lower() == "unstable":
                    self._style = 1
                elif style.lower() == "stable":
                    self._style = 0
            except Exception:
                self._style = 0

    @staticmethod
    def distpts(pt1,pt2,ret_int = False):
        x1,y1 = pt1
        x2,y2 = pt2
        x=x2-x1
        y=y2-y1
        if not ret_int:
            return (x**2+y**2)**0.5
        else:
            return int((x**2+y**2)**0.5)
        
    def render(self):
        style = self._style
        if style == 0:
            return self._style0()
        elif style == 1:
            return self._style1()
        raise ValueError(self._style)
        
    def get_pos(self):
        return self._percentage
    
    def set_pos(self,percent):
        percent = int(percent)
        if percent<-50:self._percentage = -50
        elif percent>150:self._percentage = 150
        else:self._percentage = percent
    
    def increase(self,percent):
        self._percentage += percent
        if self._percentage > 150: self._percentage=150
    
    def decrease(self,percent):
        self._percentage -= percent
        if self._percentage < -50: self._percentage=-50
    
    def set_color(self,color):
        self._color = color
    
    def set_size(self,length):
        self._size = length
    
    def _style0(self):
        percent = self._percentage 
        color = self._color
        surfacesize = self._surfacesize
        if percent>100:percent=100
        elif percent<0:percent=0
        current = (int((surfacesize[0]/100)*percent),int(surfacesize[1]*0.5))
        cx,cy = (current[0],current[1]*2)
        surface = pygame.Surface((cx,cy),pygame.SRCALPHA)
        surface.fill(color+(100,))
        return surface
    
    def _style1(self):
        percent = self._percentage 
        color = self._color
        size = self._size
        surfacesize = self._surfacesize
        minalpha = 0
        maxalpha = 200
        alpha = minalpha
        surface = pygame.Surface(surfacesize,pygame.SRCALPHA)
        surface.fill((0,0,0,0))
        current = (int((surfacesize[0]/100)*percent),int(surfacesize[1]*0.5))
        c = size
        leftcorner = (int(current[0]-c*0.5),0)
        r = Progressbar.distpts(current,leftcorner,True)
        if len(color)==4:
            color = color[:3]
        pygame.draw.circle(surface,color+(alpha,),current,r+1)
        temp = int(int(c*0.5)/(maxalpha-minalpha))
        if not temp:temp = 1
        for i in range(0,int(c*0.5),temp):
            radi = r-i
            alpha += 1
            pygame.draw.circle(surface,color+(alpha,),current,radi+1)
        return surface
#====================================================================================================

if __name__ == "__main__":
    
    from random import *
    from pygame import *
    #============================
    def distpts(pt1,pt2,ret_int = False):
        x1,y1 = pt1
        x2,y2 = pt2
        x=x2-x1
        y=y2-y1
        if not ret_int:
            return (x**2+y**2)**0.5
        else:
            return int((x**2+y**2)**0.5)
    w_length, w_width = (800,600)
    #============================
    screen = display.set_mode((w_length,w_width))
    screen.fill ((0,0,0))
    running = True


    pgbar = Progressbar((700,50),(0,255,0),250,-50,1)
##    pgbar.set_pos(-50)
##    pgbar.set_color((0,255,0))
##    pgbar.set_size(250)

    clock = time.perf_counter()
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        #=======================
        #entrance
        screen.fill ((0,0,0))
        progressbar = pgbar.render()
        screen.blit(progressbar,(50,400))
        pgbar.increase(1)
        if pgbar.get_pos() >= 125:
            pgbar.set_pos(int("-25"))
##        clock.tick(100)
        clock.tick(0)
        #=======================
        display.flip()
    quit()
    input(clock.get_fps())
    



