import pygame
import os
import sys
from Interface import *
from Objects import *

pygame.init()

map_mode = 'base'
alert = ''
#Quit = False
Worker = Actor()


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


PANE_INIT_DICT = {
    'HEAD': {
        'pane_image': 'Color1.png',
        'order': 0,
        'area': [],
        'pane_type': 'head',
        'alignment' : 'top',
        'height': 25,
        'screen': screen,
        'Worker': Worker,
        'buttons_area': {
            'main':{
                'order': 0,
                'area': [],
                'width': 200,
                'alignment': 'right',
                'font': Font12,
                'button_size': [100,20],
                'button_image': 'Button_Head.png',
                'draw': True,
                'switch': ('MENU', 'menu:main'),
                'button_dict': [
                {
                    'name': 'Menu',
                    'action': Worker.switch,
                    'item': None,
                },
                ]
            },
            'resources':{
                'order': 1,
                'area': [],
                'button_size':[100,20],
                'font': Font12,
                'alignment': 'all',
                'button_image': 'Button_Head.png',
                'draw': True,
                'switch': ('MENU', 'menu:resources'),
                'button_dict': [
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
                }
                ]
            }
        },
    },
    'SHOP': {
        'order': 1,
        'pane_image': 'Color1.png',
        'area': [],
        'alignment' : 'bottom',
        'screen': screen,
        'Worker': Worker,
        'height': 150,
        'pane_type': 'shop',
        'buttons_area': {
            'shop':{
                'order': 0,
                'area': [],
                'alignment': 'all',
                'draw': True,
                'font': Font12,
                'switch': ('MENU', 'menu:shop'),
                'button_row': 2,
                'button_size': [125,60],
                'button_image': 'Button_Shop.png',
                'button_dict': [
                {
                    'name': 'STATION',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG2',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG3',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG4',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG5',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG6',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG7',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG8',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG9',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                },
                {
                    'name': 'BLDG10',
                    'action': Worker.switch,
                    'item_image': 'Build1.png'
                }
                ]
            },
        }
    },
    'NEWS': {
        'order': 2,
        'pane_image': 'Color2.png',
        'area': [],
        'screen': screen,
        'Worker': Worker,
        'pane_type': 'news',
        'alignment' : 'bottom',
        'height': 25,
        'buttons_area': None,
    },
    'MENU': {
        'order': 3,
        'pane_image': 'Color2.png',
        'area': [],
        'pane_type': 'menu',
        'alignment' : 'right',
        'screen': screen,
        'Worker': Worker,
        'width': 200,
        'buttons_area': {
            'menu:main':{
                'order': 0,
                'area': [],
                'alignment': 'all',
                'cut_est': False,
                'static': False,
                'draw': True,
                'font': Font12,
                'button_col': 1,
                'button_size':[100,20],
                'button_image': 'Button_Menu_Main.png',
                'button_dict': [
                {
                    'name': 'EXIT',
                    'action': Worker.end_game,
                    'item': None,
                }
                ]
            },
            'menu:shop':{
                'order': 1,
                'area': [],
                'percent': 33,
                'alignment': 'bottom',
                'font': Font12,
                'draw': False,
                'cut_est': False,
                'static': False,
                'button_image': 'Button_Menu_Shop.png',
                'button_size':[100,20],
                'button_dict': [
                {
                    'name': 'КУПИТЬ',
                    'action': Worker.switch_constructing_mode,
                    'item': None,
                }
                ]
            },
            'menu:building':{
                'order': 2,
                'area': [],#############нужен button_obj_list
                'percent': 33,
                'alignment': 'bottom',
                'draw': False,
                'cut_est': False,
                'static': False,
                'font': Font12,
                'button_obj_list': [],
                'button_size':[100,20],
                'button_image': 'Button_Menu_Shop.png',
                'button_dict': None
            },
        }
    },
    'MAP': {
        'order': 4,
        'area': [],
        'alignment' : 'all',
        'screen': screen,
        'Worker': Worker,
        'pane_type': 'map',
        'buttons_area': None
    },
}


create_areas(PANE_INIT_DICT, [[0,0],[win_size[0], win_size[1]]])
for pane in PANE_INIT_DICT:
    if PANE_INIT_DICT[pane]['buttons_area'] is not None:
        for n in range(len(PANE_INIT_DICT[pane]['buttons_area'])):
            for pane_button_group in PANE_INIT_DICT[pane]['buttons_area']:
                if PANE_INIT_DICT[pane]['buttons_area'][pane_button_group]['order'] == n:
                    create_areas(PANE_INIT_DICT[pane]['buttons_area'], PANE_INIT_DICT[pane]['area'])

create_panes(PANE_INIT_DICT, PANE_DICT, IMAGE_DICT)

for button in PANE_INIT_DICT['SHOP']['buttons_area']['shop']['button_dict']:
    button['item'] = BusStation(button['pane'])
    Image(button['item_image'], [button['item']], screen = screen)

for pane in PANE_INIT_DICT:
    if PANE_INIT_DICT[pane]['buttons_area'] is not None:
        for pane_button_group in PANE_INIT_DICT[pane]['buttons_area']:
            if PANE_INIT_DICT[pane]['buttons_area'][pane_button_group]['button_dict'] is not None:
                create_buttons(PANE_INIT_DICT[pane]['buttons_area'], pane_button_group, IMAGE_DICT, BUTTON_DICT, BUTTON_DRAW_GROUPS)

Worker.PANE_INIT_DICT = PANE_INIT_DICT


'''for pane in PANE_INIT_DICT:
    print (pane, '\n', sep = '')
    for key in PANE_INIT_DICT[pane].keys():
        print(key,'  ',PANE_INIT_DICT[pane][key], '\n',sep = '')

    print( '=======', '\n')'''






#create_buttons(button_shop_dict, IMAGE_DICT, [5,2], [125,60])
#create_buttons(button_head_dict, IMAGE_DICT, [3,1],[100,20])
#create_buttons(button_menu_head_dict, IMAGE_DICT, [1,1],[100,20])
#create_buttons(button_menu_main_dict, IMAGE_DICT, [1,3],[150,25])
#create_buttons(button_menu_shop_dict, IMAGE_DICT, [1,1],[100,25])


#create_panes1(PANE_INIT_DICT, PANE_DICT)

#Объявление всех областей экрана
#Pane_Head = Pane(PANE_INIT_DICT['HEAD']['area'], 'head', PANE_INIT_DICT['HEAD']['buttons_area']['GRID_HEAD']['area'])
#Pane_Head_Menu = Pane(PANE_INIT_DICT['HEAD']['area'], 'main', PANE_INIT_DICT['HEAD']['buttons_area']['GRID_HEAD_MENU']['area'])
#Pane_Shop = Pane(PANE_INIT_DICT['SHOP']['area'], 'shop', PANE_INIT_DICT['SHOP']['buttons_area']['GRID_SHOP']['area'])
#Pane_Alert = Pane(AREA_ALERT)
#Pane_News = Pane(PANE_INIT_DICT['NEWS']['area'])
#Pane_Menu_Main = Pane(PANE_INIT_DICT['MENU']['area'], 'menu:main', PANE_INIT_DICT['MENU']['buttons_area']['GRID_MENU_MAIN']['area'])
#Pane_Menu_Shop = Pane(PANE_INIT_DICT['MENU']['area'], 'menu:shop', PANE_INIT_DICT['MENU']['buttons_area']['GRID_MENU_SHOP']['area'])
#Pane_Menu_Building = Pane(PANE_INIT_DICT['MENU']['area'], 'menu:building', PANE_INIT_DICT['MENU']['buttons_area']['GRID_MENU_BUILD']['area'])


Pane_Map = Map(PANE_INIT_DICT['MAP']['area'], [20,20])

Obstacle_Stones = Obstacle('Stone.png', screen)

#Остальные объекты
Budget = Coins()
Bums = Bum()
Farm_RUS = Farm(Worker, Pane_Map) #массив со зданиями



#Pane_Map.Building_Init(Farm_RUS)


#Загружаем изображения и записываем их в объекты
#Фон панелей
#Pane_Alert

Img_Map1 = Image('map.png', [Pane_Map], screen = screen)

#Текст. В работе.
Text01 = Text(Font25, PANE_INIT_DICT['HEAD']['buttons_area']['resources']['button_obj_list'], 'type')
Text02 = Text(Font25, [[850, 100], [850, 150], [850, 200]])

#Списки, определяющие отображаемые группы элементов на экранеPane_Alert
#CONS_ACTIVE_PANE = [Pane_Head, Pane_Shop, Pane_Head_Menu]
#TEMP_ACTIVE_PANE = [Pane_Menu_Main]
#PANE_DRAW_LIST = [Pane_Head, Pane_Menu_Main, Pane_News, Pane_Shop]

#Записываем во все объекты общие переменные
Pane_Map.screen = screen
Farm_RUS.screen = screen

for text in TEXT_LIST:
    text.screen  = screen

#for group in PANE_DICT:
#    PANE_DICT[group] = screen

#for group in IMAGE_DICT:
#    for image in IMAGE_DICT[group]:
#        image.screen = screen

#for group in BUTTON_DICT:
#    for button in BUTTON_DICT[group]:
        #button.screen = screen
        #button.font = Font12
#        button.Worker = Worker

#print (BUTTON_DICT)
#print (BUTTON_DRAW_GROUPS)
