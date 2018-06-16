import pygame
import os
import sys
from Interface import *
from Objects import *

pygame.init()

screen_x = win_size[0]
screen_y = win_size[1]
head_h = 25
news_h = 25
alert_h = 100
shop_h = 150
menu_w = 200

#Области самих панелей
AREA_HEAD = [[0,0],[screen_x,head_h]]
AREA_SHOP = [[0,screen_y-shop_h],[screen_x, screen_y]]
AREA_NEWS = [[0,AREA_SHOP[0][1]-news_h],[screen_x,AREA_SHOP[0][1]]]
AREA_ALERT = [[screen_x - menu_w, AREA_NEWS[0][1] - alert_h],[screen_x, AREA_NEWS[0][1]]]
AREA_MENU = [[screen_x-menu_w, head_h],[screen_x, AREA_ALERT[0][1]]]
AREA_MAP = [[0,AREA_HEAD[1][1]],[AREA_ALERT[0][0],AREA_ALERT[1][1]]]

#Область сетки кнопок панелей
AREA_HEAD_GRID = [[0,0],[AREA_MENU[0][0],AREA_MENU[0][1]]]
AREA_HEAD_MENU_GRID = [[screen_x-menu_w, 0],[screen_x, head_h]]
AREA_SHOP_GRID = [[0,screen_y-shop_h],[screen_x, screen_y]]
AREA_MENU_MAIN_GRID = [AREA_MENU[0],AREA_MENU[1]]
AREA_MENU_SHOP_GRID = [[AREA_ALERT[0][0], AREA_ALERT[0][1]-200],[screen_x, AREA_ALERT[1][1]]]
AREA_MENU_BUILD_GRID = [[AREA_ALERT[0][0], AREA_ALERT[0][1]-200],[screen_x, AREA_ALERT[1][1]]]
AREA_MAP_GRID = [[0,head_h],[AREA_ALERT[0][0],AREA_ALERT[1][1]]]


Font25 = pygame.font.SysFont('Colibri', 20)
Font12 = pygame.font.SysFont('Colibri', 12)

Budget = Coins()
Bums = Bum()
Station = BusStation()
BLDG1 = BusStation()
BLDG2 = BusStation()
BLDG3 = BusStation()
BLDG4 = BusStation()

clock = pygame.time.Clock()

Image_Bum = pygame.image.load(os.path.join('images','Bum.png'))
Image_Null1 = pygame.image.load(os.path.join('images', 'Color1.png'))
Image_Null2 = pygame.image.load(os.path.join('images', 'Color2.png'))
Image_Null3 = pygame.image.load(os.path.join('images', 'Color3.png'))
Image_Null5 = pygame.image.load(os.path.join('images', 'Color5.png'))
Image_Null4 = pygame.image.load(os.path.join('images', 'Color4.png'))

screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)

Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2

pygame.time.set_timer(Time1sec, 1000)

map_mode = 'base'

alert = ''
done = False

Worker = Actor()



Pane_Head = Pane(AREA_HEAD, 'head', AREA_HEAD_GRID)
Pane_Head_Menu = Pane(AREA_HEAD, 'main', AREA_HEAD_MENU_GRID)
Pane_Shop = Pane(AREA_SHOP, 'shop', AREA_SHOP_GRID)
Pane_Alert = Pane(AREA_ALERT)
Pane_News = Pane(AREA_NEWS)
Pane_Menu_Main = Pane(AREA_MENU, 'menu:main', AREA_MENU_MAIN_GRID)
Pane_Menu_Shop = Pane(AREA_MENU, 'menu:shop', AREA_MENU_SHOP_GRID)
Pane_Menu_Building = Pane(AREA_MENU, 'menu:building', AREA_MENU_SHOP_GRID)

Pane_Map = Map(AREA_MAP, [20,20])

CONS_ACTIVE_PANE = [Pane_Head, Pane_Shop, Pane_Head_Menu]
TEMP_ACTIVE_PANE = [Pane_Menu_Main]

PANE_DRAW_LIST = [Pane_Head, Pane_Menu_Main, Pane_Alert, Pane_News, Pane_Shop]

Farm = Building(Worker, Pane_Map)

Button_Menu = Button('Menu', Worker.switch, Bums)

Button_Shop11 = Button('BUM', Worker.switch, Bums)
Button_Shop12 = Button('STATION', Worker.switch, Station)
Button_Shop13 = Button('BLDG1', Worker.switch, BLDG1)
Button_Shop14 = Button('BLDG2', Worker.switch, BLDG2)
Button_Shop15 = Button('BLDG3', Worker.switch, BLDG3)
Button_Shop21 = Button('BLDG4', Worker.switch, BLDG4)
Button_Shop22 = Button('SHOP22', Worker.switch, Bums)
Button_Shop23 = Button('SHOP23', Worker.switch, Bums)
Button_Shop24 = Button('SHOP24', Worker.switch, Bums)
Button_Shop25 = Button('SHOP25', Worker.switch, Bums)

Button_BLDG01 = Button('SET', Worker.set)
Button_BLDG02 = Button('LVL', Worker.lvl)

Button_Head1 = Button('', Worker.switch, Bums)
Button_Head2 = Button('', Worker.switch, Bums)
Button_Head3 = Button('', Worker.switch, Bums)

Button_Quit = Button('EXIT', Worker.EXIT)
Button_Menu_Main2 = Button('MAIN2', Worker.buy)

Button_Menu_Shop1 = Button('КУПИТЬ', Worker.switch_map)
#Button_Menu_Shop2 = Button('BUY2', Worker.buy)

Building1 = Button ('yep', Worker.buy)


Pane_Head.Button_Init([Button_Head1, Button_Head2, Button_Head3], [3,1],[100,20])
Pane_Shop.Button_Init([Button_Shop11, Button_Shop12, Button_Shop13, Button_Shop14, Button_Shop15,
                       Button_Shop21, Button_Shop22, Button_Shop23, Button_Shop24, Button_Shop25], [5,2], [125,60])
Pane_Head_Menu.Button_Init([Button_Menu],[1,1],[100,20])
Pane_Menu_Main.Button_Init([Button_Quit, Button_Menu_Main2],[1,3],[150,25])
Pane_Menu_Shop.Button_Init([Button_Menu_Shop1], [1,1],[100,25])
Pane_Menu_Building.Button_Init([Button_BLDG01, Button_BLDG02], [2,1],[80,25])

Pane_Map.Building_Init(Farm)

Img_B_Shop = Image('Button_Shop.png', Pane_Shop.button_list)
Img_B_Menu_Shop = Image('Button_Menu_Shop.png',  Pane_Menu_Shop.button_list)
Img_B_Main = Image('Button_Main.png', Pane_Head_Menu.button_list)
Img_B_Menu_Main = Image('Button_Menu_Main.png', Pane_Menu_Main.button_list)
Img_B_Head = Image('Button_Head.png',Pane_Head.button_list)
Img_B_Menu_BLDG = Image('Button_Menu_Building.png', Pane_Menu_Building.button_list)

Img_Bg1 = Image('Color1.png', [Pane_Head, Pane_Head_Menu, Pane_Alert, Pane_Shop])
Img_Bg2 = Image('Color2.png', [Pane_Menu_Main, Pane_Menu_Shop, Pane_News])
Img_Map1 = Image('map.png', [Pane_Map])

Img_Bldg1 = Image('Build1.png', [BLDG1])
Img_Bldg2 = Image('Build2.png', [BLDG2])


Text01 = Text(Font25, [Button_Head1, Button_Head2, Button_Head3], 'type')
Text02 = Text(Font25, [[850, 100], [850, 150], [850, 200]])

Pane_Map.screen =screen
Building1.font = Font12
Farm.screen = screen

for text in TEXT_LIST:
    text.screen  = screen
for group in PANE_DICT:
    for pane in PANE_DICT[group]:
        pane.screen = screen
for image in IMAGE_LIST:
    image.screen = screen
for group in BUTTON_DICT:
    for button in BUTTON_DICT[group]:
        button.screen = screen
        button.font = Font12
