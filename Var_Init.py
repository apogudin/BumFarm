import pygame
import os
import sys
from Interface import *
from Objects import *

pygame.init()

map_mode = 'base'
alert = ''
done = False
Worker = Actor()

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

#Объявление всех областей экрана
Pane_Head = Pane(AREA_HEAD, 'head', AREA_HEAD_GRID)
Pane_Head_Menu = Pane(AREA_HEAD, 'main', AREA_HEAD_MENU_GRID)
Pane_Shop = Pane(AREA_SHOP, 'shop', AREA_SHOP_GRID)
Pane_Alert = Pane(AREA_ALERT)
Pane_News = Pane(AREA_NEWS)
Pane_Menu_Main = Pane(AREA_MENU, 'menu:main', AREA_MENU_MAIN_GRID)
Pane_Menu_Shop = Pane(AREA_MENU, 'menu:shop', AREA_MENU_SHOP_GRID)
Pane_Menu_Building = Pane(AREA_MENU, 'menu:building', AREA_MENU_SHOP_GRID)
Pane_Map = Map(AREA_MAP, [20,20])

#Объекты зданий
Station = BusStation()
BLDG2 = BusStation()
BLDG3 = BusStation()
BLDG4 = BusStation()
BLDG5 = BusStation()
BLDG6 = BusStation()
BLDG7 = BusStation()
BLDG8 = BusStation()
BLDG9 = BusStation()
BLDG10 = BusStation()

#Остальные объекты
Budget = Coins()
Bums = Bum()
Farm_RUS = Farm(Worker, Pane_Map) #массив со зданиями

#Шрифты
Font25 = pygame.font.SysFont('Colibri', 20)
Font12 = pygame.font.SysFont('Colibri', 12)
#Время
clock = pygame.time.Clock()
Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2
pygame.time.set_timer(Time1sec, 1000)
#Окно
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(pygame.image.load(os.path.join('images','Bum.png')))

#Объявление всех кнопок
#Переход в главное меню
Button_Menu = Button('Menu', Worker.switch, Bums)
#Главное меню
Button_Quit = Button('EXIT', Worker.EXIT)
Button_Menu_Main2 = Button('MAIN2', Worker.buy)
#Магазин
Button_Shop11 = Button('STATION', Worker.switch, Station)
Button_Shop12 = Button('BLDG2', Worker.switch, BLDG2)
Button_Shop13 = Button('BLDG3', Worker.switch, BLDG3)
Button_Shop14 = Button('BLDG4', Worker.switch, BLDG4)
Button_Shop15 = Button('BLDG5', Worker.switch, BLDG5)
Button_Shop21 = Button('BLDG6', Worker.switch, BLDG6)
Button_Shop22 = Button('BLDG7', Worker.switch, BLDG7)
Button_Shop23 = Button('BLDG8', Worker.switch, BLDG8)
Button_Shop24 = Button('BLDG9', Worker.switch, BLDG9)
Button_Shop25 = Button('BLDG10', Worker.switch, BLDG10)
#Действие с товаром в магазине
Button_Menu_Shop1 = Button('КУПИТЬ', Worker.switch_map)
#Действия с постройкой
Button_BLDG01 = Button('SET', Worker.set)
Button_BLDG02 = Button('LVL', Worker.lvl)
#Ресурсы в шапке
Button_Head1 = Button('', Worker.switch, Bums)
Button_Head2 = Button('', Worker.switch, Bums)
Button_Head3 = Button('', Worker.switch, Bums)

#Записываем кнопки в панели
Pane_Head.Button_Init([Button_Head1, Button_Head2, Button_Head3], [3,1],[100,20])
Pane_Shop.Button_Init([Button_Shop11, Button_Shop12, Button_Shop13, Button_Shop14, Button_Shop15,
                       Button_Shop21, Button_Shop22, Button_Shop23, Button_Shop24, Button_Shop25], [5,2], [125,60])
Pane_Head_Menu.Button_Init([Button_Menu],[1,1],[100,20])
Pane_Menu_Main.Button_Init([Button_Quit, Button_Menu_Main2],[1,3],[150,25])
Pane_Menu_Shop.Button_Init([Button_Menu_Shop1], [1,1],[100,25])
Pane_Menu_Building.Button_Init([Button_BLDG01, Button_BLDG02], [2,1],[80,25])
Pane_Map.Building_Init(Farm_RUS)

#Загружаем изображения и записываем их в объекты
#Фон панелей
Img_Bg1 = Image('Color1.png', [Pane_Head, Pane_Head_Menu, Pane_Alert, Pane_Shop])
Img_Bg2 = Image('Color2.png', [Pane_Menu_Main, Pane_Menu_Shop, Pane_News])
Img_Map1 = Image('map.png', [Pane_Map])
#Кнопки
Img_B_Shop = Image('Button_Shop.png', Pane_Shop.button_list)
Img_B_Menu_Shop = Image('Button_Menu_Shop.png',  Pane_Menu_Shop.button_list)
Img_B_Main = Image('Button_Main.png', Pane_Head_Menu.button_list)
Img_B_Menu_Main = Image('Button_Menu_Main.png', Pane_Menu_Main.button_list)
Img_B_Head = Image('Button_Head.png',Pane_Head.button_list)
Img_B_Menu_BLDG = Image('Button_Menu_Building.png', Pane_Menu_Building.button_list)
#Здания
Img_Station = Image('Build1.png', [Station])
Img_BLDG2 = Image('Build2.png', [BLDG2])
Img_BLDG3 = Image('Build2.png', [BLDG3])
Img_BLDG4 = Image('Build2.png', [BLDG4])
Img_BLDG5 = Image('Build2.png', [BLDG5])
Img_BLDG6 = Image('Build2.png', [BLDG6])
Img_BLDG7 = Image('Build2.png', [BLDG7])
Img_BLDG8 = Image('Build2.png', [BLDG8])
Img_BLDG9 = Image('Build2.png', [BLDG9])
Img_BLDG10 = Image('Build2.png', [BLDG10])
Img_Stone = Image('Stone.png')

#Текст. В работе.
Text01 = Text(Font25, [Button_Head1, Button_Head2, Button_Head3], 'type')
Text02 = Text(Font25, [[850, 100], [850, 150], [850, 200]])

#Списки, определяющие отображаемые группы элементов на экране
CONS_ACTIVE_PANE = [Pane_Head, Pane_Shop, Pane_Head_Menu]
TEMP_ACTIVE_PANE = [Pane_Menu_Main]
PANE_DRAW_LIST = [Pane_Head, Pane_Menu_Main, Pane_Alert, Pane_News, Pane_Shop]

#Записываем во все объекты общие переменные
Pane_Map.screen = screen
Farm_RUS.screen = screen

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
