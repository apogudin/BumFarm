import pygame
import math
from MyFunctions import *
class Bum():
    #Все существующие бомжи#
    def __init__(self):
        self.cost = 10          #Цена одного бомжа
        self.amount = 0         #Количество свободных бомжей
        self.efficiency = 1     #Эффективность бомжей
        self.trash = 0          #Счётчик отработанных бомжей
    def buy(self):
        self.amount += 1
    def set(self):
        self.amount -= 1

class Coins():
    #Деньги игрока
    def __init__(self):
        self.amount = 20
    def income(self, sum):      #Прибыль
        self.amount += sum
    def outgo(self, sum):       #Расход
        self.amount -= sum

class BusStation():
    #Ларёк
    def __init__(self):
        self.cost = 25
        self.limit = 0
        self.level = 1
        self.Bums = 0
        self.amount = 0
    def levelUp():
        self.levelUp += 1
        self.limit += 5
    def buy(self):
        self.amount += 1
        self.limit += 5
    def setBum(self):
        self.Bums += 1

class Interface_Pane():
#Возвращает область выбранной панели [[x1,y1],[x2,y2]]
    def __init__(self, win_size):
        self.screen_x = win_size[0]
        self.screen_y = win_size[1]
        self.head_h = 25
        self.shop_h = 150
        self.news_h = 25
        self.alert_h = 100
        self.menu_w = 200

    def head(self):                                #ПАНЕЛЬ РЕСУРСОВ
        return [[0,0],[self.screen_x,self.head_h]]

    def shop(self):                                #ПАНЕЛЬ МАГАЗИНА
        return [[0,self.screen_y-self.shop_h],[self.screen_x, self.screen_y]]

    def news(self):                                 #ЛЕНТА НОВОСТЕЙ
        shop_pos_y = self.shop()[0][1]
        return [[0,shop_pos_y-self.news_h],[self.screen_x,shop_pos_y]]

    def alert(self):                                #ПАНЕЛЬ АЛЕРТОВ
        news_pos_y = self.news()[0][1]
        return [[self.screen_x - self.menu_w, news_pos_y - self.alert_h],[self.screen_x, news_pos_y]]

    def menu_main(self):                            #МЕНЮШКА СПРАВА
        alert_top_y = self.alert()[0][1]
        return [[self.screen_x-self.menu_w, self.head_h],[self.screen_x, alert_top_y]]
    def menu_shop():
        pass
    def menu_building():
        pass
    def menu_info():
        pass

class Button(Interface_Pane):
    #Кнопки с любыми шрифтами, размерами, положением. Grid_place - с нуля.
    def __init__(self, name, type, grid_place, bg, bg_on, win_size):
        super().__init__(win_size)
        self.name = name
        self.bg = bg
        self.bg_draw = bg
        self.bg_on = bg_on
        self.grid_x = grid_place[0]
        self.grid_y = grid_place[1]

        def XY_From_Grid (wight, hight, Nx, Ny, gap_x, gap_y, pane):
            #Сколько занимают все кнопки с пробелами
            total_x = wight*Nx + gap_x*(Nx-1)
            total_y = hight*Ny + gap_y*(Ny-1)

            #Wight и hight панели
            pane_x =  pane[1][0] - pane[0][0]
            pane_y =  pane[1][1] - pane[0][1]

            #Левый верхний угол матрицы
            start_x = pane[0][0] + (pane_x/2 - total_x/2)
            start_y = pane[0][1] + (pane_y/2 - total_y/2)

            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(wight + gap_x),start_y + j*(hight+gap_y)] \
            for i in range(Nx)] for j in range(Ny)]

            pos_x = Grid[self.grid_y][self.grid_x][0]
            pos_y = Grid[self.grid_y][self.grid_x][1]
            return [pos_x, pos_y]

        if type == 'shop':
            self.wight = 100
            self.hight = 60
            Nx = 3
            Ny = 2
            gap_x = 20
            gap_y = 10
            pane = super(Button, self).shop()  #Внутри какой панели будем строить сетку
            self.pos_x, self.pos_y = XY_From_Grid(self.wight, self.hight, Nx, Ny, gap_x, gap_y, pane)

        if type == 'head':
            pass
        if type == 'menu':
            Nx = 1
            Ny = 1
            self.wight = 100
            head_pane = super(Button, self).head()
            self.hight = head_pane[1][1] - head_pane[0][1]
            gap_x = 0
            gap_y = 0
            pane = super(Button, self).head()
            self.pos_x = pane [1][0] - self.wight
            self.pos_y = pane [0][1]
        if type == 'menu_shop':
            pass
        if type == 'menu_main':
            pass





    def draw (self, screen, font = 'Colibri',font_size = 25):
        Font_Text = pygame.font.SysFont(font, font_size)
        Img_Fill(self.bg_draw,[[self.pos_x,self.pos_y],[self.pos_x+self.wight, self.pos_y+self.hight]], screen)
        text = Font_Text.render(self.name, True, [0,0,0])
        screen.blit(text, (self.pos_x + (self.wight/2 - text.get_width()/2), self.pos_y +(self.hight/2 - text.get_height()/2)))

    def IsOn (self, mouse_pos):
        if (self.pos_x < mouse_pos[0] < self.pos_x + self.wight) :
            if (self.pos_y < mouse_pos[1] < self.pos_y + self.hight):
                self.bg_draw = self.bg_on
                return True
        self.bg_draw = self.bg
        return False
