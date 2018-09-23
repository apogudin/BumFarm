from Objects import *
from Interface import *


pygame.init()

map_mode = 'base'
alert = ''
Worker = Actor()
Player = User()

#Шрифты
Font25 = pygame.font.SysFont('Colibri', 20)
Font12 = pygame.font.SysFont('Colibri', 12)
#Время
clock = pygame.time.Clock()
Timer1Sec = pygame.USEREVENT+1
Timer10Sec = pygame.USEREVENT+3
Alert_Event = pygame.USEREVENT+2
pygame.time.set_timer(Timer1Sec, 1000)
pygame.time.set_timer(Timer10Sec, 10000)
#Окно
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(pygame.image.load(os.path.join('images','Bum.png')))

#Хеш с основными элементами интерфейса
PANE_INIT_DICT = {
    'HEAD': {
        'order': 0,
        'pane_type': 'head',
        'pane_image': 'Color1.png',
        'area': [],
        'alignment' : 'top',
        'height': 25,
        'screen': screen,
        'Worker': Worker,
        'buttons_area': {
            'main':{
                'order': 0,
                'draw': True,
                'switch': ('MENU', 'menu:main'),
                'button_image': 'Button_Head.png',
                'area': [],
                'alignment': 'right',
                'width': 200,
                'button_size': [100,20],
                'font': Font12,
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
                'draw': True,
                'switch': ('MENU', 'menu:text:resources'),
                'button_image': 'Button_Head.png',
                'area': [],
                'alignment': 'all',
                'button_size':[100,20],
                'font': Font12,
                'button_dict': [
                {
                    'name': '',
                    'action': Worker.switch,
                    'item': Player,
                    'params': {'res_annotation': 'coins'}
                },
                {
                    'name': '',
                    'action': Worker.switch,
                    'item': Player,
                    'params': {'res_annotation': 'bums'}
                },
                {
                    'name': '',
                    'action': Worker.switch,
                    'item':Player,
                    'params': {'res_annotation': 'reputation'}
                },
                {
                    'name': '',
                    'action': Worker.switch,
                    'item': Player,
                    'params': {'res_annotation': 'total_bums'}
                }
                ]
            }
        },
    },
    'SHOP': {
        'order': 1,
        'pane_type': 'shop',
        'pane_image': 'Color1.png',
        'area': [],
        'alignment' : 'bottom',
        'height': 150,
        'screen': screen,
        'Worker': Worker,
        'buttons_area': {
            'shop':{
                'order': 0,
                'draw': True,
                'switch': ('MENU', 'menu:shop'),
                'button_image': 'Button_Shop.png',
                'area': [],
                'alignment': 'all',
                'button_size': [125,60],
                'button_row': 2,
                'font': Font12,
                'button_dict': [
                {
                    'name': 'STATION',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'ShootingRange',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': ShootingRange(Player),
                },
                {
                    'name': 'BLDG3',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG4',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG5',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG6',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG7',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG8',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG9',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                },
                {
                    'name': 'BLDG10',
                    'action': Worker.switch,
                    'item_image': 'Build1.png',
                    'item': BusStation(Player),
                }
                ]
            },
        }
    },
    'NEWS': {
        'order': 2,
        'pane_type': 'news',
        'pane_image': 'Color2.png',
        'area': [],
        'alignment' : 'bottom',
        'height': 150,
        'height': 25,
        'screen': screen,
        'Worker': Worker,
        'buttons_area': None,
    },
    'MENU': {
        'order': 3,
        'pane_type': 'menu',
        'pane_image': 'Color2.png',
        'area': [],
        'alignment' : 'right',
        'width': 200,
        'screen': screen,
        'Worker': Worker,
        'buttons_area': {
            'menu:main':{
                'order': 0,
                'draw': True,
                'button_image': 'Button_Menu_Main.png',
                'area': [],
                'alignment': 'all',
                'button_col': 1,
                'button_size':[100,20],
                'cut_est': False,
                'font': Font12,
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
                'draw': False,
                'area': [],
                'button_image': 'Button_Menu_Shop.png',
                'alignment': 'bottom',
                'button_size':[100,20],
                'percent': 33,
                'font': Font12,
                'cut_est': False,
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
                'draw': False,
                'button_image': 'Button_Menu_Shop.png',
                'area': [],
                'alignment': 'bottom',
                'button_size':[100,20],
                'percent': 33,
                'cut_est': True,
                'font': Font12,
                'button_obj_list': [],
                'rebuild': True,
                'button_dict': None
            },

            'menu:text:resources':{
                'order': 3,
                'draw': False,
                'area': [],
                'button_obj_list': [],
                'alignment': 'all',
                'cut_est': False,
                'rebuild': True,
                'button_dict': None
            },

            'menu:text:info_screen':{
                'order': 4,
                'draw': False,
                'area': [],
                'button_obj_list': [],
                'alignment': 'bottom',
                'percent': 50,
                'cut_est': True,
                'button_dict': None
            },
            'menu:text:info_annotation':{
                'order': 5,
                'draw': False,
                'area': [],
                'button_obj_list': [],
                'alignment': 'all',
                'cut_est': True,
                'rebuild': True,
                'button_dict': None
            },
        }
    },
    'MAP': {
        'order': 4,
        'pane_type': 'map',
        'area': [],
        'alignment' : 'all',
        'screen': screen,
        'Worker': Worker,
        'buttons_area': None
    },
}

#Создание объектов интерфейса по хешу
create_areas(PANE_INIT_DICT, [[0,0],[win_size[0], win_size[1]]])
for pane in PANE_INIT_DICT:
    if PANE_INIT_DICT[pane]['buttons_area'] is not None:
        for n in range(len(PANE_INIT_DICT[pane]['buttons_area'])):
            for pane_button_group in PANE_INIT_DICT[pane]['buttons_area']:
                if PANE_INIT_DICT[pane]['buttons_area'][pane_button_group]['order'] == n:
                    create_areas(PANE_INIT_DICT[pane]['buttons_area'], PANE_INIT_DICT[pane]['area'])
create_panes(PANE_INIT_DICT, PANE_DICT, IMAGE_DICT)

#Иницализация изображений для всех зданий
for button in PANE_INIT_DICT['SHOP']['buttons_area']['shop']['button_dict']:
    Image(button['item_image'], [button['item']], screen = screen)

for pane in PANE_INIT_DICT:
    if PANE_INIT_DICT[pane]['buttons_area'] is not None:
        for pane_button_group in PANE_INIT_DICT[pane]['buttons_area']:
            if PANE_INIT_DICT[pane]['buttons_area'][pane_button_group]['button_dict'] is not None:
                create_buttons(PANE_INIT_DICT[pane]['buttons_area'], pane_button_group, IMAGE_DICT)

Worker.PANE_INIT_DICT = PANE_INIT_DICT

#Элементы интерфейса
Pane_Map = Map(PANE_INIT_DICT['MAP']['area'], [20,20])
Img_Map1 = Image('map.png', [Pane_Map], screen = screen)
Obstacle_Stones = Obstacle('Stone.png', screen)

#Игровые объекты
Budget = Coins()
Bums = Bum()
Farm_EUR = Farm(Worker, Pane_Map) #массив со зданиями

#Текст. В работе.
Txt_Resourses = Text(Font25, {'obj_list': PANE_INIT_DICT['HEAD']['buttons_area']['resources']['button_obj_list'], 'text': Player.resources}, screen, Worker = Worker)
Txt_Info_Screen = Text(Font25, PANE_INIT_DICT['MENU']['buttons_area']['menu:text:info_screen']['area'], screen, page = 'info_screen', area = True, Worker = Worker)
Txt_Info_Annotation = Text(Font25, PANE_INIT_DICT['MENU']['buttons_area']['menu:text:info_annotation']['area'], screen,  page = 'info_annotation', area = True, hyph = True, Worker = Worker)
Txt_Shop_Annotation = Text(pygame.font.SysFont('Colibri', 20), PANE_INIT_DICT['MENU']['buttons_area']['menu:main']['area'], screen,  page = 'shop_annotation', area = True, hyph = True, Worker = Worker)

Txt_Resourses_Annotation = Text(Font25, PANE_INIT_DICT['MENU']['buttons_area']['menu:text:resources']['area'], screen, page = 'res_annotation', area = True, Worker = Worker, hyph = True)

Txt_News = News_Line(PANE_INIT_DICT['NEWS']['area'], pygame.font.SysFont('Colibri', 25), screen, Worker)

# BUG: Записываем в некоторые объекты общие переменные. Кажется, это костыль.
Pane_Map.screen = screen
Farm_EUR.screen = screen
Worker.user = Player
Player.Worker = Worker
