import pygame
from MyFunctions import *
from Configs import *
from Objects import *
import math


class Panes():
    def __init__(self, type):
        #для выбранного type высчитывает область: левый-верхний, правый-нижний угол
        PANES_LIST.append(self)
        self.screen_x = win_size[0]
        self.screen_y = win_size[1]
        self.pane_type = type
        self.head_h = 25
        self.news_h = 25
        self.alert_h = 100
        self.shop_h = 150
        self.menu_w = 200

        pane_head = [[0,0],[self.screen_x,self.head_h]]
        pane_shop = [[0,self.screen_y-self.shop_h],[self.screen_x, self.screen_y]]
        pane_news = [[0,pane_shop[0][1]-self.news_h],[self.screen_x,pane_shop[0][1]]]
        pane_alert = [[self.screen_x - self.menu_w, pane_news[0][1] - self.alert_h],[self.screen_x, pane_news[0][1]]]
        pane_menu = [[self.screen_x-self.menu_w, self.head_h],[self.screen_x, pane_alert[0][1]]]

        if self.pane_type ==  'head':
            self.pane = pane_head
        if self.pane_type ==  'shop':
            self.pane = pane_shop
        if self.pane_type ==  'news':
            self.pane = pane_news
        if self.pane_type ==  'alert':
            self.pane = pane_alert
        if self.pane_type ==  'menu:shop' or self.pane_type ==  'menu:main' :
            self.pane = pane_menu
        if self.pane_type ==  'main':
            self.pane = pane_head


    def Button_Init(self, button_list):
        #записывает в кнопки их координаты
        self.button_list = button_list
        self.hight = 25
        self.grid_area = self.pane
        Nbutton = len(button_list)
        gap_x = 10
        gap_y = 10

        #Строит матрицу для кнопок, возвращает [pos_x, pos_y]
        def Grid (width, hight, Nx, Ny, gap_x, gap_y, pane):
            total_x = width*Nx + gap_x*(Nx-1)
            total_y = hight*Ny + gap_y*(Ny-1)
            pane_x =  pane[1][0] - pane[0][0]
            pane_y =  pane[1][1] - pane[0][1]
            start_x = pane[0][0] + (pane_x/2 - total_x/2)
            start_y = pane[0][1] + (pane_y/2 - total_y/2)

            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(width + gap_x),start_y + j*(hight+gap_y)] \
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
            self.hight = 60
        if self.pane_type == 'head':
            Nx, Ny = NxNy(Nbutton)
            gap_x = 50
            self.width = 50
            self.hight = self.pane[1][1] - self.pane[0][1]
        if self.pane_type == 'menu:shop':
            Nx, Ny = NxNy(Nbutton)
            self.width = (self.menu_w - (Nx+1)*gap_x)/Nx
            self.grid_area[0][1] = self.grid_area[1][1]-100
        if self.pane_type == 'menu:main':
            Ny, Nx = NxNy(Nbutton)
            self.width = (self.pane[1][0] - self.pane[0][0]) - gap_x*2
        if self.pane_type == 'main':
            Nx, Ny = NxNy(Nbutton)
            gap_x, gap_y = 0, 0
            self.width = 100
            self.pane[0][0] = self.pane[1][0] - self.width

        #Записываем в кнопки их координаты
        grid_x = 0
        grid_y = 0
        for button in button_list:
            i = button_list.index(button)
            if ((i+1)-(grid_y*Nx)) > Nx:
                grid_x = 0
                grid_y += 1
            button.pos_x, button.pos_y = Grid(self.width, self.hight, Nx, Ny, gap_x, gap_y, self.grid_area)
            button.pane = self.pane_type
            button.width = self.width
            button.hight = self.hight
            Append_To_Dict(BUTTON_DICT, self.pane_type, button)
            grid_x += 1

class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, bg, bg_on, worker_act, item = ''):
        self.worker_act = worker_act
        self.name = name
        self.bg = bg
        self.bg_draw = bg
        self.bg_on = bg_on
        self.item = item
        self.pos_x = 0
        self.pos_y = 0
        self.pane = ''
        self.width = 0
        self.hight = 0

    def draw (self, screen, font = 'Colibri',font_size = 12):
        Font_Text = pygame.font.SysFont(font, font_size)
        Img_Fill(self.bg_draw,[[self.pos_x,self.pos_y],[self.pos_x+self.width, self.pos_y+self.hight]], screen)
        text = Font_Text.render(self.name, True, [0,0,0])
        screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y +(self.hight/2 - text.get_height()/2)))

    def IsOn (self, mouse_pos):
        if (self.pos_x < mouse_pos[0] < self.pos_x + self.width) :
            if (self.pos_y < mouse_pos[1] < self.pos_y + self.hight):
                self.bg_draw = self.bg_on
                return True
        self.bg_draw = self.bg
        return False

    def Activate(self):
        return self.worker_act(self)


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
