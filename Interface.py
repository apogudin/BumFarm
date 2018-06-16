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

    def Building_Init(self,building):
        self.Building = building

    def Building_add(self, obj, pos):
        #берём obj, напрмяую записываем в object_list и тут же obj.img - в img_list
        pass

    def Move(self, keys):
        if keys[pygame.K_RIGHT] and self.NULL[0] + self.pane_width <= self.tile_size*self.NxNy[0]:
            self.NULL[0] += 2
        if keys[pygame.K_LEFT] and self.NULL[0] >= 2:
            self.NULL[0] -= 2
        if keys[pygame.K_DOWN] and self.NULL[1] + self.pane_height <= self.tile_size*self.NxNy[1]:
            self.NULL[1] += 2
        if keys[pygame.K_UP] and self.NULL[1] >= 2:
            self.NULL[1] -= 2
        self.NULL_tile_draw = [self.NULL[0]//self.tile_size, self.NULL[1]//self.tile_size]
        self.NULL_draw = [(-1)*(self.NULL[0]%self.tile_size) + self.pane[0][0], (-1)*(self.NULL[1]%self.tile_size) + self.pane[0][1]]
        #print (self.NULL_draw)

    def draw_Button(self):
        self.Building.draw()

    def draw_pane(self):
        Img_Fill(self.img, [self.NULL_draw, self.pane[1]], self.screen)

class Building():
    def __init__(self, worker, map):
        self.worker = worker
        self.object_list = [[[None, None, None] for i in range(map.NxNy[0])] for j in range (map.NxNy[1]) ]
        self.pane_type = 'buildings'
        self.map = map
        self.screen = None


    def add (self, mouse_pos):
        pos = self.WhoIsOn(mouse_pos)
        obj = self.worker.item
        obj_size_yx = [len(obj.tile), len(obj.tile[0])]

        #Проверка на занятость
        if pos[0]+obj_size_yx[0] > self.map.NxNy[1] or pos[1]+obj_size_yx[1] > self.map.NxNy[0]:
            print ('BORDER!')
            return
        for j in range(pos[0], pos[0]+obj_size_yx[0]):
            for i in range(pos[1], pos[1]+obj_size_yx[1]):
                if self.object_list[j][i][0] is not None:
                    print('ENGAGED')
                    return

        #Записали в массив новый объект
        for j in range(obj_size_yx[0]):
            for i in range(obj_size_yx[1]):
                if obj.tile[j][i]:
                    self.object_list[pos[0]+j][pos[1]+i][0] = obj
        self.object_list[pos[0]][pos[1]][1] = obj.img

        #Записали в объект новый элемент
        default = [0, 1, None]
        for j in range(pos[0], pos[0]+obj_size_yx[0]):
            for i in range(pos[1], pos[1]+obj_size_yx[1]):
                id = str(j) + ':' + str(i)
                obj.objects_dict[id] = default

    def WhoIsOn(self, mouse_pos):


        for i in range(1,self.map.NxNy[0]+1):
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
        '''
        if request == 'pos_id':
            return str(pos_y) + ':' + str(pos_x)
        elif request == 'obj':
            j = self.WhoIsOn('pos_tile', mouse_pos)[0]
            i = self.WhoIsOn('pos_tile', mouse_pos)[1]
            return self.object_list[j][i][0]
        '''
        return [pos_y, pos_x]

    def draw(self):
        max_bldg_size = 2
        for j in range(self.map.NULL_tile_draw[1]-max_bldg_size, self.map.NULL_tile_draw[1]+self.map.tile_visible_NxNy[1]+1):
            for i in range(self.map.NULL_tile_draw[0]-max_bldg_size, self.map.NULL_tile_draw[0]+self.map.tile_visible_NxNy[0]+1):
                if i < self.map.NxNy[0] and j < self.map.NxNy[1]:
                    if self.object_list[j][i][1] is not None:
                        pos_x = (i - self.map.NULL_tile_draw[0]) * self.map.tile_size + self.map.NULL_draw[0]
                        pos_y = (j - self.map.NULL_tile_draw[1]) * self.map.tile_size + self.map.NULL_draw[1]
                        self.object_list[j][i][1].draw(pos_x, pos_y, [1,2])

    def Activate(self, mouse_pos):
        pos = self.WhoIsOn(mouse_pos)
        obj = self.object_list[pos[0]][pos[1]][0]
        pos_id = str(pos[0]) + ':' + str(pos[1])
        print(obj, pos_id)
        if obj is not None:
            self.worker.item = obj
            self.worker.item_id = pos_id
            return self.worker.switch_build(self)


class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, worker_act, item = None):
        self.worker_act = worker_act
        self.name = name
        self.item = item
        self.state = 'off'
        self.img = None
        self.pos_x = None
        self.pos_y = None
        self.pane_type = None
        self.width = None
        self.height = None
        self.screen = None
        self.font = None

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
        return self.worker_act(self)

    def size(self):
        return [self.width, self.height]

    def pos(self):
        return [self.pos_x, self.pos_y]


class Image():
    def __init__(self, image, object_list = [], folder = 'images'):
        IMAGE_LIST.append(self)
        self.img = pygame.image.load(os.path.join(folder,image))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.screen = None
        for obj in object_list:
            obj.img = self

    def draw(self, pos_x, pos_y, Nxy = [1,1], elem = [0,0]):
        crop_width = self.width/Nxy[0]
        crop_height = self.height/Nxy[1]
        crop_pos_x = crop_width*elem[0]
        crop_pos_y = crop_height*elem[1]
        self.screen.blit(self.img, [pos_x, pos_y],(crop_pos_x,crop_pos_y,crop_width,crop_height))


    def draw_Button(self, pos_x, pos_y, state):
        if state == 'off':
            elem = [0,0]
        elif state == 'on':
            elem = [0,1]
        self.draw(pos_x, pos_y, [1,2], elem)


    def fill(self, area):
        Img_Fill(area, self.screen)


class Actor ():
    def __init__(self):
        self.item = None
        self.item_id = None
        self.interface_group = None
        self.map_mode = 'base'
        self.map_mode_switch = 'building'
        self.co = 0

    def switch(self, button):
        self.interface_group ="menu:" + button.pane_type
        self.item = button.item
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
            self.obj_size_list = [obj.size() for obj in pos_list]

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
