import pygame
import os
import sys
from Interface import *
from Objects import *

pygame.init()

Budget = Coins()
Bums = Bum()
Station = BusStation()

clock = pygame.time.Clock()

Image_Bum = pygame.image.load(os.path.join('images','Bum.png'))
Image_Null1 = pygame.image.load(os.path.join('images', 'Color1.png'))
Image_Null2 = pygame.image.load(os.path.join('images', 'Color2.png'))
Image_Null3 = pygame.image.load(os.path.join('images', 'Color3.png'))
Image_Null4 = pygame.image.load(os.path.join('images', 'Color4.png'))
Image_Null5 = pygame.image.load(os.path.join('images', 'Color5.png'))

screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)

Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2

pygame.time.set_timer(Time1sec, 1000)

alert = ''
font = pygame.font.SysFont('Colibri', 25)
done = False


#Button_Menu = Button('Menu','to_menu_main',[0,0],Image_Null5,Image_Null4, Interface_Pane.set_menu)

#Button_Shop11 = Button('SHOP11','shop',[0,0],Image_Null5,Image_Null4, Interface_Pane.set_menu)
Button_Shop12 = Button('SHOP12','shop',[1,0],Image_Null5,Image_Null4, Bums.buy)
Button_Shop13 = Button('SHOP13','shop',[2,0],Image_Null5,Image_Null4, Bums.buy)
Button_Shop14 = Button('SHOP14','shop',[3,0],Image_Null5,Image_Null4, Bums.buy)
Button_Shop15 = Button('SHOP15','shop',[4,0],Image_Null5,Image_Null4, Bums.buy)
Button_Shop21 = Button('SHOP21','shop',[0,1],Image_Null5,Image_Null4, Bums.buy)
Button_Shop22 = Button('SHOP22','shop',[1,1],Image_Null5,Image_Null4, Bums.buy)
Button_Shop23 = Button('SHOP23','shop',[2,1],Image_Null5,Image_Null4, Bums.buy)
Button_Shop24 = Button('SHOP24','shop',[3,1],Image_Null5,Image_Null4, Bums.buy)
Button_Quit = Button('ВЫХОД','shop',[4,1],Image_Null5,Image_Null4, Bums.buy)

Button_Head1 = Button('h1', 'head',[0,0], Image_Null5, Image_Null4, Bums.buy)
Button_Head2 = Button('h2', 'head',[1,0], Image_Null5, Image_Null4, Bums.buy)
Button_Head3 = Button('h3', 'head',[2,0], Image_Null5, Image_Null4, Bums.buy)

Button_Menu_Main1 = Button('main1', 'menu_main',[0,0], Image_Null5, Image_Null4, Bums.buy)
Button_Menu_Main2 = Button('main2', 'menu_main',[0,1], Image_Null5, Image_Null4, Bums.buy)

Button_Menu_Shop1 = Button('menu_shop1', 'menu_shop',[0,0], Image_Null5, Image_Null4, Bums.buy)


Panes = Interface_Pane()

menu_type = 1
