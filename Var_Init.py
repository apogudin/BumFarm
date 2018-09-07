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

Obstacle_Stones = Obstacle('Stone.png')
'''
#Объекты зданий
Station = BusStation(Pane_Menu_Building)
BLDG2 = BusStation(Pane_Menu_Building)
BLDG3 = BusStation(Pane_Menu_Building)
BLDG4 = BusStation(Pane_Menu_Building)
BLDG5 = BusStation(Pane_Menu_Building)
BLDG6 = BusStation(Pane_Menu_Building)
BLDG7 = BusStation(Pane_Menu_Building)
BLDG8 = BusStation(Pane_Menu_Building)
BLDG9 = BusStation(Pane_Menu_Building)
BLDG10 = BusStation(Pane_Menu_Building)
'''
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


#Pane_Map.Building_Init(Farm_RUS)




button_shop_dict = {
    'pane': Pane_Shop,
    'image': 'Button_Shop.png',
    'buttons': [
    {
        'name': 'STATION',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG2',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG3',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG4',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG5',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG6',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG7',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG8',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG9',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    {
        'name': 'BLDG10',
        'action': Worker.switch,
        'item': BusStation(Pane_Menu_Building),
        'item_image': 'Build1.png'
    },
    ]
}

for button in button_shop_dict['buttons']:
    Image(button['item_image'], [button['item']])

button_menu_head_dict = {
    'pane': Pane_Head_Menu,
    'image': 'Button_Head.png',
    'buttons': [
    {
        'name': 'Menu',
        'action': Worker.switch,
        'item': None,
    },
    ]
}

button_menu_main_dict = {
    'pane': Pane_Menu_Main,
    'image': 'Button_Menu_Main.png',
    'buttons': [
    {
        'name': 'EXIT',
        'action': Worker.EXIT,
        'item': None,
    },
    {
        'name': 'MAIN2',
        'action': Worker.buy,
        'item': None,
    },
    ]
}

button_menu_shop_dict = {
    'pane': Pane_Menu_Shop,
    'image': 'Button_Menu_Shop.png',
    'buttons': [
    {
        'name': 'КУПИТЬ',
        'action': Worker.switch_map,
        'item': None,
    },
    ]
}

button_head_dict = {
    'pane': Pane_Head,
    'image': 'Button_Head.png',
    'buttons': [
    {
        'name': '',
        'action': Worker.switch,
        'item': None,
    },
    {
        'name': '',
        'action': Worker.switch,
        'item': None,
    },
    {
        'name': '',
        'action': Worker.switch,
        'item': None,
    },
    ]
}





create_buttons(button_shop_dict, IMAGE_DICT, [5,2], [125,60])
create_buttons(button_head_dict, IMAGE_DICT, [3,1],[100,20])
create_buttons(button_menu_head_dict, IMAGE_DICT, [1,1],[100,20])
create_buttons(button_menu_main_dict, IMAGE_DICT, [1,3],[150,25])
create_buttons(button_menu_shop_dict, IMAGE_DICT, [1,1],[100,25])


#Загружаем изображения и записываем их в объекты
#Фон панелей
Img_Bg1 = Image('Color1.png', [Pane_Head, Pane_Head_Menu, Pane_Alert, Pane_Shop])
Img_Bg2 = Image('Color2.png', [Pane_Menu_Main, Pane_Menu_Shop, Pane_News])
Img_Map1 = Image('map.png', [Pane_Map])
'''
#Img_B_Menu_BLDG = Image('Button_Menu_Building.png', Pane_Menu_Building.button_list)
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
'''

#Текст. В работе.
Text01 = Text(Font25, BUTTON_DICT['head'], 'type')
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
for group in IMAGE_DICT:
    for image in IMAGE_DICT[group]:
        image.screen = screen

for group in BUTTON_DICT:
    for button in BUTTON_DICT[group]:
        button.screen = screen
        button.font = Font12
        button.Worker = Worker
