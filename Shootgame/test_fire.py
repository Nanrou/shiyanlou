#coding:utf8

import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((295,413),0,32)
pygame.display.set_caption('Hello world!')

a = pygame.image.load('1.jpg').convert()
b = pygame.image.load('2.jpg').convert()

background = a
flag = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if flag:
                background = b
            else:
                background = a
            flag = not(flag)
            
    screen.blit(background,(0,0))
    pygame.display.update()