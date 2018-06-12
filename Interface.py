import math
import pygame
import os
import sys
from Objects import *
from MyFunctions import *
from Configs import *
import copy

class Pane():
    def __init__(self, type):
        #для выбранного type высчитывает область: левый-верхний, правый-нижний угол
        PANE_LIST.append(self)
        self.screen_x = win_size[0]
        self.screen_y = win_size[1]
        self.pane_type = type
        self.head_h = 25
        self.news_h = 25
        self.alert_h = 100
        self.shop_h = 150
        self.menu_w = 200
        self.img = None
        self.screen = None

        pane_head = [[0,0],[self.screen_x,self.head_h]]
        pane_shop = [[0,self.screen_y-self.shop_h],[self.screen_x, self.screen_y]]
        pane_news = [[0,pane_shop[0][1]-self.news_h],[self.screen_x,pane_shop[0][1]]]
        pane_alert = [[self.screen_x - self.menu_w, pane_news[0][1] - self.alert_h],[self.screen_x, pane_news[0][1]]]
        pane_menu = [[self.screen_x-self.menu_w, self.head_h],[self.screen_x, pane_alert[0][1]]]

        if self.pane_type ==  'head':
            PANE_LIST_DRAW.append(self)
            self.pane = pane_head
        if self.pane_type ==  'shop':
            PANE_LIST_DRAW.append(self)
            self.pane = pane_shop
        if self.pane_type ==  'news':
            PANE_LIST_DRAW.append(self)
            self.pane = pane_news
        if self.pane_type ==  'alert':
            PANE_LIST_DRAW.append(self)
            self.pane = pane_alert
        if self.pane_type ==  'menu:shop':
            self.pane = pane_menu
        if self.pane_type ==  'menu:main':
            PANE_LIST_DRAW.append(self)
            self.pane = pane_menu
        if self.pane_type ==  'main':
            self.pane = pane_head

        print(self.pane_type, self.pane, sep = ' ')

    def Button_Init(self, button_list):
        #записывает в кнопки их координаты
        self.button_list = button_list
        self.height = 25
        self.grid_area = self.pane
        Nbutton = len(button_list)
        gap_x = 10
        gap_y = 10
        #Строит матрицу для кнопок, возвращает [pos_x, pos_y]
        def Grid (width, height, Nx, Ny, gap_x, gap_y, pane):
            total_x = width*Nx + gap_x*(Nx-1)
            total_y = height*Ny + gap_y*(Ny-1)
            pane_x =  pane[1][0] - pane[0][0]
            pane_y =  pane[1][1] - pane[0][1]
            start_x = pane[0][0] + (pane_x/2 - total_x/2)
            start_y = pane[0][1] + (pane_y/2 - total_y/2)

            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(width + gap_x),start_y + j*(height+gap_y)] \
            for i in range(Nx)] for j in range(Ny)]

            pos_x = Grid[grid_y][grid_x][0]
            pos_y = Grid[grid_y][grid_x][1]
            return [pos_x, pos_y]

        def NxNy (amount, row = 1):
            return [math.ceil(amount/row), row]

        #В зависимости от типа панели определяем параметры для Grid
        if self.pane_type == 'shop':
            Nx, Ny = NxNy(Nbutton, row = 2)
            gap_x = 20
            self.width = 125
            self.height = 60
        if self.pane_type == 'head':
            Nx, Ny = NxNy(Nbutton)
            gap_x = 50
            self.width = 50
            self.height = self.grid_area[1][1] - self.grid_area[0][1]
        if self.pane_type == 'menu:shop':
            Nx, Ny = NxNy(Nbutton)
            self.width = (self.menu_w - (Nx+1)*gap_x)/Nx
            self.grid_area[0][1] = self.grid_area[1][1]-100
        if self.pane_type == 'menu:main':
            Ny, Nx = NxNy(Nbutton)
            self.width = (self.grid_area[1][0] - self.grid_area[0][0]) - gap_x*2
        if self.pane_type == 'main':
            Nx, Ny = NxNy(Nbutton)
            gap_x, gap_y = 0, 0
            self.width = 100
            self.grid_area[0][0] = self.grid_area[1][0] - self.width


        #Записываем в кнопки их координаты
        grid_x = 0
        grid_y = 0
        for button in button_list:
            i = button_list.index(button)
            if ((i+1)-(grid_y*Nx)) > Nx:
                grid_x = 0
                grid_y += 1
            button.pos_x, button.pos_y = Grid(self.width, self.height, Nx, Ny, gap_x, gap_y, self.grid_area)
            button.pane = self.pane_type
            button.width = self.width
            button.height = self.height
            Append_To_Dict(BUTTON_DICT, self.pane_type, button)
            grid_x += 1

    def fill(self):
        Img_Fill(self.img, self.pane, self.screen)





class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, worker_act, item = ''):
        self.worker_act = worker_act
        self.name = name
        self.item = item
        self.state = 'off'
        self.img = None
        self.pos_x = None
        self.pos_y = None
        self.pane = None
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
        self.item = 'None'
        self.interface_group = 'None'

    def switch(self, button):
        self.interface_group ="menu:" + button.pane
        self.item = button.item
        #print(self.interface_group)
        return self.interface_group


    def buy(self, button):
        self.item.buy()

    def nothing(self, item=''):
        return


class Text():
    def __init__(self, font, pos_list, type = None):
        #либо указываем напрямую список позиций pos_list,
        #либо передаём список объектов и указываем их тип (для типов тут прописаны специфики расположения)
        TEXT_LIST.append(self)
        self.font = font
        self.screen = None

        self.obj_pos_list = [obj.pos() for obj in pos_list]
        self.obj_size_list = [obj.size() for obj in pos_list]

    def draw(self, text_list, event = None, duration = None):

        self.text_list = [self.font.render(text, True, [0,0,0]) for text in text_list]

        if type is None:
            self.pos_list = pos_list
        else:
            self.pos_list = []
            if type == 'head':
                pass
            elif type is not None:
                #Для любого указанного, но непрописанного type ставим по центру
                for i in range(len(self.text_list)):
                    self.pos_list.append([
                        self.obj_pos_list[i][0] + (self.obj_size_list[i][0]/2 - self.text_list[i].get_width()/2),
                        self.obj_pos_list[i][1] +(self.obj_size_list[i][1]/2 - self.text_list[i].get_height()/2)
                        ])

        for i in range(len(self.text_list)):
            self.screen.blit(self.text_list[i], self.pos_list[i])
        #for ... pos_list ... blit..
