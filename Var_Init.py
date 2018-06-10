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

screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)

Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2

pygame.time.set_timer(Time1sec, 1000)

alert = ''
font = pygame.font.SysFont('Colibri', 25)
done = False

Button_Buy_Bum = Button('Купить бомжа','shop',[0,0],Image_Null3,Image_Null2, Bums.buy)
Button_Buy_Station = Button('ОСТАНОВКА','shop',[1,0],Image_Null3,Image_Null2, Station.buy)
TEST_BUTTON20 = Button('TEST20','shop',[2,0],Image_Null3,Image_Null2, Bums.buy)
Button_Bum_Station = Button('Поселить бомжа','shop',[0,1],Image_Null3,Image_Null2, Station.setBum)
Button_Menu = Button('Menu','menu',[0,0],Image_Null3,Image_Null2, Bums.buy)
Button_Quit = Button('ВЫЙТИ','shop',[2,1],Image_Null3,Image_Null2, Bums.buy)

Panes = Interface_Pane()

menu_type = 1
