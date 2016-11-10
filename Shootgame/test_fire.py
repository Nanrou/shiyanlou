#coding:utf8

import pygame
from sys import exit
import random

class Bullet(object):
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False
        
    def move(self):
        if self.active:
            self.y -= 1
        if self.y<0:
            self.active =False
    
    def restart(self): 
        mouseX,mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width()/2
        self.y = mouseY - self.image.get_height()/2
        self.active = True
        
        
class Enemy(object):
    def restart(self):
        self.x = random.randint(80,480)
        self.y = random.randint(-200,-50)
        self.speed =random.random()+0.1
        
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()
    
    def move(self):
        if self.y<800:
            self.y +=self.speed
        else:
            self.restart()
            
def checkHit(e,b):
    if (b.x > e.x and b.x < e.x + e.image.get_width())and(b.y>e.y and b.y<e.y+e.image.get_height()):
        e.restart()           
        b.active = False
        return True
    return False
        
class Plane(object):
    def restart(self):
        self.x = 200
        self.y = 600
    
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()
    
    def move(self):  
        x,y = pygame.mouse.get_pos()
        x -= self.image.get_width()/2
        y -= self.image.get_height()/2
        self.x = x
        self.y = y

def checkCrash(e,p):
    if ((p.x + 0.7*p.image.get_width()>e.x) and (p.x+0.3*p.image.get_width()<e.x+e.image.get_width()))\
        and ((p.y+0.7*p.image.get_height()>e.y)and(p.y+0.3*p.image.get_height()<e.y+e.image.get_height())):
        return True
    return False
    
        
        
pygame.init()
screen = pygame.display.set_mode((516,572),0,32)
pygame.display.set_caption('Hello world!')

a = pygame.image.load('1.png').convert()
#b = pygame.image.load('2.png').convert()
plane = Plane()

bullets =[]
for i in xrange(5):
    bullets.append(Bullet())
    
count_b = len(bullets)
index_b = 0
interval_b = 0

enemies = []
for i in xrange(3):
    enemies.append(Enemy())

font = pygame.font.Font(None,32)
font_g = pygame.font.Font(None,78)
background = a
#flag = True
score = 0
gameover =False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flag:
                background = b
            else:
                background = a
            flag = not(flag)
        '''  
    screen.blit(background,(0,0))
    
    if not gameover:
        
        interval_b -= 1
        if interval_b < 0:
            bullets[index_b].restart()
            interval_b = 330
            index_b = (index_b + 1) % count_b
        
        for b in bullets:
            if b.active:
                for e in enemies:
                    if checkHit(e, b):
                        score +=100
                b.move()
                screen.blit(b.image,(b.x,b.y))
                
        
            for e in enemies:
                if checkCrash(e,plane):
                    gameover = True
                e.move()
                screen.blit(e.image,(e.x,e.y))
    
        plane.move()
        screen.blit(plane.image,(plane.x,plane.y))
        text = font.render('Score:%d' % score,1,(0,0,0))
        screen.blit(text,(0,0))
    
    else :
        textg = font_g.render('Game Over',1,(255,255,255))
        screen.blit(textg,(130,248))
        if event.type == pygame.MOUSEBUTTONDOWN:
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            score = 0
            gameover = False
    
    
    pygame.display.update()