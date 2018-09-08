import math
import pygame
import os
import sys
from Objects import *
from MyFunctions import *
from Configs import *
import copy

class Pane():
    def __init__(self, area, pane_type=None, grid=None):
        #для выбранного type высчитывает область: левый-верхний, правый-нижний угол
        self.pane = area
        self.grid_area = grid
        self.pane_type = pane_type
        self.img = None
        self.screen = None
        self.user_map_place = None
        Append_To_Dict(PANE_DICT, self.pane_type, self)

    def Button_Init(self, button_list, NxNy, size = [100, 150], gap = [10,10]):
        self.button_list = button_list

        def Grid(size_x, size_y, Nx, Ny, gap_x, gap_y, grid_area):
            total_x = size[0]*NxNy[0] + gap[0]*(NxNy[0]-1)
            total_y = size[1]*NxNy[1] + gap[1]*(NxNy[1]-1)
            pane_x =  grid_area[1][0] - grid_area[0][0]
            pane_y =  grid_area[1][1] - grid_area[0][1]
            start_x = grid_area[0][0] + (pane_x/2 - total_x/2)
            start_y = grid_area[0][1] + (pane_y/2 - total_y/2)

            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(size[0] + gap[0]),start_y + j*(size[1]+gap[1])] \
            for i in range(NxNy[0])] for j in range(NxNy[1])]

            pos_x = Grid[grid_y][grid_x][0]
            pos_y = Grid[grid_y][grid_x][1]
            return [pos_x, pos_y]

        #Записываем в кнопки их координаты
        grid_x = 0
        grid_y = 0

        if self.pane_type == 'menu:building':
            BUTTON_DICT['menu:building'] = []

        for button in button_list:
            i = button_list.index(button)
            if ((i+1)-(grid_y*NxNy[0])) > NxNy[0]:
                grid_x = 0
                grid_y += 1
            button.pos_x, button.pos_y = Grid(size[0], size[1], NxNy[0], NxNy[1], gap[0], gap[1], self.grid_area)
            button.pane_type = self.pane_type
            button.width = size[0]
            button.height = size[1]

            Append_To_Dict(BUTTON_DICT, self.pane_type, button)
            grid_x += 1

    def draw_Button(self):
        for button in self.button_list:
            button.draw()

    def draw_pane(self):
        Img_Fill(self.img, self.pane, self.screen)

    def IsOn (self, mouse_pos):
        if (self.pane[0][0] < mouse_pos[0] < self.pane[1][0]) :
            if (self.pane[0][1] < mouse_pos[1] < self.pane[1][1]):
                return True
        return False

    def get_size(self):
        return(self.pane)


class Map():
    def __init__(self, pane, NxNy, building_list = []):
        self.pane = pane
        self.pane_type = 'Map'
        self.NxNy = NxNy
        self.building_list = building_list
        self.pane_width = self.pane[1][0] - self.pane[0][0]
        self.pane_height = self.pane[1][1] - self.pane[0][1]
        self.tile_size = 50
        self.tile_visible_NxNy = [self.pane_width//self.tile_size+1, self.pane_height//self.tile_size+1]
        self.img = None

        self.GRID_pos = [[[i,j] for i in range(NxNy[0])] for j in range(NxNy[1])]
        self.GRID_coo = [[[i*self.tile_size, j*self.tile_size] for i in range(NxNy[0])] for j in range(NxNy[1])]

        self.NULL = [0,0]
        self.NULL_tile_draw = [0,0]
        self.NULL_draw =  [self.pane[0][0], self.pane[1][1]]

    def IsOn (self, mouse_pos):
        if (self.pane[0][0] < mouse_pos[0] < self.pane[1][0]) :
            if (self.pane[0][1] < mouse_pos[1] < self.pane[1][1]):
                return True
        return False

    def Move(self, keys):
        speed = 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.NULL[0] + self.pane_width <= self.tile_size*self.NxNy[0]:
            self.NULL[0] += speed
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.NULL[0] >= 2:
            self.NULL[0] -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.NULL[1] + self.pane_height <= self.tile_size*self.NxNy[1]:
            self.NULL[1] += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.NULL[1] >= 2:
            self.NULL[1] -= speed
        self.NULL_tile_draw = [self.NULL[0]//self.tile_size, self.NULL[1]//self.tile_size]
        self.NULL_draw = [(-1)*(self.NULL[0]%self.tile_size) + self.pane[0][0], (-1)*(self.NULL[1]%self.tile_size) + self.pane[0][1]]

    def draw(self):
        Img_Fill(self.img, [self.NULL_draw, self.pane[1]], self.screen)
        self.Building.draw()

#Хранит информацию о каждой клетке
class Farm():
    def __init__(self, worker, map):
        self.worker = worker
        self.tile_info = [[{'obj': None, 'img': [], 'id': None, 'rotate': None} for i in range(map.NxNy[0])] for j in range (map.NxNy[1]) ]   #[объект, изображение, алиас, поворот?]
        self.pane_type = 'buildings'
        self.map = map
        map.Building = self

    #Проверка на занятость
    def can_build(self, mouse_pos):
        obj = self.worker.item_state['item']
        obj_size = len(obj.tile)
        obj_j, obj_i = 0, 0
        pos = self.WhoIsOn(mouse_pos)
        pos_row = pos[0] - obj.pivot[0]
        pos_col = pos[1] - obj.pivot[1]
        for j in range(pos_row, pos_row+obj_size):
            for i in range(pos_col, pos_col+obj_size):
                if self.worker.item_state['item'].tile[obj_j][obj_i]:
                    if pos_row+obj_j >= self.map.NxNy[1] or pos_col+obj_i >= self.map.NxNy[0]:
                        return False
                    elif pos_row+obj_j < 0 or pos_col+obj_i < 0:
                        return False
                    elif self.tile_info[j][i]['obj'] is not None:
                        return False
                obj_i += 1
            obj_i = 0
            obj_j += 1
        return True

    def add (self, mouse_pos):
        obj = self.worker.item_state['item']
        obj_size = len(self.worker.item_state['item'].tile)
        pos = self.WhoIsOn(mouse_pos)
        pos_row = pos[0] - obj.pivot[0]
        pos_col = pos[1] - obj.pivot[1]

        #Записали в объект новый элемент, например '0:0': [bums, limit, lvl]
        item_id=''
        for j in range(pos_row, pos_row+obj_size):
            for i in range(pos_col, pos_col+obj_size):
                item_id += '_' + str(j) + ':' + str(i) + '_'
        obj.objects_dict[item_id] = {}
        obj.set_default(item_id)

        #Записали в массив новый объект
        for j in range(obj_size):
            for i in range(obj_size):
                if obj.tile[j][i]:
                    self.tile_info[pos_row+j][pos_col+i]['obj'] = obj
                    self.tile_info[pos_row+j][pos_col+i]['id'] = item_id
        self.tile_info[pos_row][pos_col]['img'].append(obj.img)
        self.tile_info[pos_row][pos_col]['rotate'] = [3,self.worker.item_rotate]
        self.worker.item_rotate = 0
        self.worker.item_state['item'].tile_to_default()

    def WhoIsOn(self, mouse_pos): #хуйня, переписать
        for i in range(1,self.map.NxNy[0]+1): #хуйня какая-то. Это все клетки чтоли проверяются???
            if mouse_pos[0] < self.map.GRID_coo[0][i][0] + self.map.NULL_draw[0]:
                #Указатель на абсолютную позицию в массиве
                #if request == 'pos_tile' or request == 'pos_id':
                pos_x = self.map.GRID_pos[0][i-1][0] + self.map.NULL_tile_draw[0]
                #Что-то странное. Массив с абсолютными координатами? Зачем? Это не используется же.
                #if request == 'pos_coordinates':
                #    pos_x = self.map.GRID_coo[0][i-1][0] + self.map.NULL_draw[0]
                break
        for j in range(1,self.map.NxNy[1]+1):
            if mouse_pos[1] < self.map.GRID_coo[j][0][1] + self.map.NULL_draw[1]:
                #if request == 'pos_tile' or request == 'pos_id':
                pos_y = self.map.GRID_pos[j-1][0][1] + self.map.NULL_tile_draw[1]
                #if request == 'pos_coordinates':
                #    pos_y = self.map.GRID_coo[j-1][0][1] + self.map.NULL_draw[1]
                break
        return [pos_y, pos_x]

    def draw(self):
        max_bldg_size = 2
        for j in range(self.map.NULL_tile_draw[1]-max_bldg_size, self.map.NULL_tile_draw[1]+self.map.tile_visible_NxNy[1]+1):
            for i in range(self.map.NULL_tile_draw[0]-max_bldg_size, self.map.NULL_tile_draw[0]+self.map.tile_visible_NxNy[0]+1):
                if (i < self.map.NxNy[0] and j < self.map.NxNy[1]) and self.tile_info[j][i]['img'] is not None:
                    pos_x = (i - self.map.NULL_tile_draw[0]) * self.map.tile_size + self.map.NULL_draw[0]
                    pos_y = (j - self.map.NULL_tile_draw[1]) * self.map.tile_size + self.map.NULL_draw[1]
                    for image in self.tile_info[j][i]['img']:
                        image.draw(pos_x, pos_y, [4,4], self.tile_info[j][i]['rotate'])

    def Activate(self, mouse_pos):
        pos = self.WhoIsOn(mouse_pos)
        obj = self.tile_info[pos[0]][pos[1]]['obj']
        if obj == 'Stone':
            pass
        elif obj is not None:
            self.worker.item_state['item'] = obj
            self.worker.item_state['item_id'] = self.tile_info[pos[0]][pos[1]]['id']
            return self.worker.switch_build(self)


class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, action, item = None):
        self.action = action
        self.name = name
        self.item = item
        self.state = 'off'
        self.params = {'item_id': None}

    def IsOn (self, mouse_pos):
        if (self.pos_x < mouse_pos[0] < self.pos_x + self.width) :
            if (self.pos_y < mouse_pos[1] < self.pos_y + self.height):
                self.state = 'on'
                return True
        self.state = 'off'
        return False

    def draw (self):
        text = self.font.render(self.name, True, [0,0,0])
        self.img.draw_Button(self.pos_x, self.pos_y, self.state)
        #Img_Fill(self.bg_draw,[[self.pos_x,self.pos_y],[self.pos_x+self.width, self.pos_y+self.height]], self.screen)
        self.screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y +(self.height/2 - text.get_height()/2)))

    def Activate(self):
        self.Worker.item_state['button'] = self
        return self.action(self.Worker.item_state)

    def get_size(self):
        return [self.width, self.height]

    def pos(self):
        return [self.pos_x, self.pos_y]

#Для более удобной работы с изображениями.
#Object_list должен содержать объекты, пренадлежащие одной группе
class Image():
    def __init__(self, image, object_list = [], folder = 'images'):
        if hasattr(object_list[0], 'pane_type'):
            if object_list[0].pane_type not in IMAGE_DICT:
                IMAGE_DICT[object_list[0].pane_type] = []
            IMAGE_DICT[object_list[0].pane_type].append(self)
        else:
            IMAGE_DICT['No pane_type'].append(self)

        self.img = pygame.image.load(os.path.join(folder,image))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        for obj in object_list:
            obj.img = self

    def draw(self, pos_x, pos_y, Nxy = [1,1], elem = [0,0]):
        crop_width = self.width/Nxy[0]
        crop_height = self.height/Nxy[1]
        crop_pos_x = crop_width*elem[1]
        crop_pos_y = crop_height*elem[0]
        self.screen.blit(self.img, [pos_x, pos_y],(crop_pos_x,crop_pos_y,crop_width,crop_height))


    def draw_Button(self, pos_x, pos_y, state):
        if state == 'off':
            elem = [0,0]
        elif state == 'on':
            elem = [1,0]
        self.draw(pos_x, pos_y, [1,2], elem)


    def fill(self, area):
        Img_Fill(area, self.screen)
##

class Actor ():
    def __init__(self):
        self.item = None
        self.item_id = None
        self.item_state = {
            'item': None,
            'item_id':None,
            'button': None,
        }
        self.item_rotate = 0
        self.interface_group = None
        self.map_mode = 'mode_base'
        self.map_mode_switch = 'mode_constructing'
        #self.co = 0

    def switch(self, params):
        self.interface_group ="menu:" + self.item_state['button'].pane_type
        self.item_state['item'] = self.item_state['button'].item
        return self.interface_group

    def switch_build(self, build):
        self.interface_group ="menu:building"
        return self.interface_group

    def switch_map(self, button=None):
        self.map_mode,self.map_mode_switch = self.map_mode_switch, self.map_mode

    def buy(self, button):
        self.item.buy()

    def set(self, button=None):
        self.item.set(self.item_id)

    def lvl(self, button=None):
        self.item.lvl(self.item_id)

    def EXIT(self, item=''):
        return 'EXIT'


class Text():
    def __init__(self, font, pos_list, text_type = None):
        #либо указываем напрямую список позиций pos_list,
        #либо передаём список объектов и указываем их тип (для типов тут прописаны специфики расположения)
        TEXT_LIST.append(self)
        self.font = font
        self.screen = None
        self.text_type = text_type
        self.pos_list = pos_list
        if text_type is not None:
            self.obj_pos_list = [obj.pos() for obj in pos_list]
            self.obj_size_list = [obj.get_size() for obj in pos_list]

    def draw(self, text_list, event = None, duration = None):

        self.text_list = [self.font.render(text, True, [0,0,0]) for text in text_list]

        if self.text_type is None:
            self.pos_list = self.pos_list
        else:
            self.pos_list = []
            if self.text_type == 'head':
                pass
            elif self.text_type is not None:
                #Для любого указанного, но непрописанного type ставим по центру
                for i in range(len(self.text_list)):
                    self.pos_list.append([
                        self.obj_pos_list[i][0] + (self.obj_size_list[i][0]/2 - self.text_list[i].get_width()/2),
                        self.obj_pos_list[i][1] +(self.obj_size_list[i][1]/2 - self.text_list[i].get_height()/2)
                        ])

        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], self.pos_list[i])
        #for ... pos_list ... blit..


class Obstacle():
    def __init__(self, img):
        self.img = img
        Image(img, [self])

    def rand_stones (self, object_list, N):
        for i in range(N):
            R_row = random.randrange(0, 19, 1)
            R_column = random.randrange(0, 19, 1)
            object_list[R_row][R_column]['obj'] = 'Stone'
            object_list[R_row][R_column]['img'] = [self.img]
            object_list[R_row][R_column]['rotate'] = [0, 0]


# BUG: позорище. NxNy и size должны генерироваться в pane
def create_buttons (buttons_dict, IMAGE_DICT, NxNy, size):
    Button_list=[]
    i = 0
    if buttons_dict['pane'].pane_type == 'menu:building':
        IMAGE_DICT['menu:building'] = []

    for Butt in buttons_dict['buttons']:
        Button_list.append(Button(Butt['name'], Butt['action']))
        Button_list[i].item = Butt['item']
        buttons_dict['pane'].Button_Init(Button_list, NxNy, size)
        if 'image' not in buttons_dict:
            Image(Butt['image'], [Button_list[i]])
        i += 1

    if 'image' in buttons_dict:
        Image(buttons_dict['image'], Button_list)


    return Button_list
