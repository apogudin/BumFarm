import pygame
import os
import sys
from Interface import *
from Objects import *
a = 'test'
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

Worker = Actor()

Pane_Head = Panes('head')
Pane_Shop = Panes('shop')
Pane_News = Panes('news')
Pane_Alert = Panes('alert')
Pane_To_Menu = Panes('main')
Pane_Menu_Main = Panes('menu:main')
Pane_Menu_Shop = Panes('menu:shop')

Button_Menu = Button('Menu', Image_Null5,Image_Null4, Worker.switch, Bums)

Button_Shop11 = Button('BUM', Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop12 = Button('STATION', Image_Null5,Image_Null4, Worker.switch, Station)
Button_Shop13 = Button('SHOP13', Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop14 = Button('SHOP14', Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop15 = Button('SHOP15',Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop21 = Button('SHOP21',Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop22 = Button('SHOP22',Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop23 = Button('SHOP23',Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop24 = Button('SHOP24',Image_Null5,Image_Null4, Worker.switch, Bums)
Button_Shop25 = Button('SHOP25',Image_Null5,Image_Null4, Worker.switch, Bums)

Button_Head1 = Button('h1', Image_Null5, Image_Null4, Worker.switch, Bums)
Button_Head2 = Button('h2', Image_Null5, Image_Null4, Worker.switch, Bums)
Button_Head3 = Button('h3', Image_Null5, Image_Null4, Worker.switch, Bums)

Button_Quit = Button('EXIT', Image_Null5, Image_Null4, Worker.nothing)
Button_Menu_Main2 = Button('MAIN2', Image_Null5, Image_Null4, Worker.buy)

Button_Menu_Shop1 = Button('BUY1', Image_Null5, Image_Null4, Worker.buy)
Button_Menu_Shop2 = Button('BUY2', Image_Null5, Image_Null4, Worker.buy)

Pane_Head.Button_Init([Button_Head1, Button_Head2, Button_Head3])
Pane_Shop.Button_Init([Button_Shop11, Button_Shop12, Button_Shop13, Button_Shop14, Button_Shop15,
                       Button_Shop21, Button_Shop22, Button_Shop23, Button_Shop24, Button_Shop25, ])
Pane_To_Menu.Button_Init([Button_Menu])
Pane_Menu_Main.Button_Init([Button_Quit, Button_Menu_Main2])
Pane_Menu_Shop.Button_Init([Button_Menu_Shop1, Button_Menu_Shop2])
