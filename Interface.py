import pygame
from MyFunctions import *
from Configs import *
from Objects import *

class Interface_Pane():
    #Возвращает область выбранной панели [[x1,y1],[x2,y2]]
    def __init__(self):
        self.screen_x = win_size[0]
        self.screen_y = win_size[1]
        self.head_h = 25
        self.shop_h = 150
        self.news_h = 25
        self.alert_h = 100
        self.menu_w = 200

    #ПАНЕЛЬ РЕСУРСОВ
    def head(self):
        return [[0,0],[self.screen_x,self.head_h]]

    #ПАНЕЛЬ МАГАЗИНА
    def shop(self):
        return [[0,self.screen_y-self.shop_h],[self.screen_x, self.screen_y]]

    #ЛЕНТА НОВОСТЕЙ
    def news(self):
        shop_pos_y = self.shop()[0][1]
        return [[0,shop_pos_y-self.news_h],[self.screen_x,shop_pos_y]]

    #ПАНЕЛЬ АЛЕРТОВ
    def alert(self):
        news_pos_y = self.news()[0][1]
        return [[self.screen_x - self.menu_w, news_pos_y - self.alert_h],[self.screen_x, news_pos_y]]

    #МЕНЮШКА СПРАВА
    def menu(self):
        alert_top_y = self.alert()[0][1]
        return [[self.screen_x-self.menu_w, self.head_h],[self.screen_x, alert_top_y]]

    def set_menu(self, interface_group):
        #global TEMP_INTERFACE_GROUP
        TEMP_INTERFACE_GROUP = [interface_group]

        #a = 333333333333333333333333333333333
        return interface_group
        #print(TEMP_INTERFACE_GROUP)
class Button(Interface_Pane):
    #Кнопки с любыми шрифтами, размерами, положением. Grid_place - с нуля.
    def __init__(self, name, pane, grid_place, bg, bg_on, worker_act, item = ''):
        super().__init__()
        #if item != '':
        #    item = ':'+item
        #group = type + item
        Append_To_Dict(BUTTON_DICT, pane, self)
        #self.interface_group = interface_group
        self.worker_act = worker_act
        self.name = name
        self.bg = bg
        self.bg_draw = bg
        self.bg_on = bg_on
        self.grid_x = grid_place[0]
        self.grid_y = grid_place[1]
        self.hight = 25
        self.pane = pane
        self.item = item

        gap_x = 10
        gap_y = 10


        #Высчитываем [pos_x, pos_y]
        def XY_From_Grid (width, hight, Nx, Ny, gap_x, gap_y, pane):
            #Сколько занимают все кнопки с пробелами
            total_x = width*Nx + gap_x*(Nx-1)
            total_y = hight*Ny + gap_y*(Ny-1)
            #width и hight панели
            pane_x =  pane[1][0] - pane[0][0]
            pane_y =  pane[1][1] - pane[0][1]
            #Левый верхний угол матрицы
            start_x = pane[0][0] + (pane_x/2 - total_x/2)
            start_y = pane[0][1] + (pane_y/2 - total_y/2)
            #Матрица Nx на Ny по центру области win_size,
            #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
            Grid = [[[start_x + i*(width + gap_x),start_y + j*(hight+gap_y)] \
            for i in range(Nx)] for j in range(Ny)]
            pos_x = Grid[self.grid_y][self.grid_x][0]
            pos_y = Grid[self.grid_y][self.grid_x][1]
            return [pos_x, pos_y]

        if pane == 'shop':
            Nx = 5
            Ny = 2
            gap_x = 20
            pane = super(Button, self).shop()  #Внутри какой панели будем строить сетку
            self.width = 125
            self.hight = 60
            self.pos_x, self.pos_y = XY_From_Grid(self.width, self.hight, Nx, Ny, gap_x, gap_y, pane)
        if pane == 'head':
            Nx = 4
            Ny = 1
            gap_x = 50
            pane = super(Button,self).head()
            self.width = 50
            self.hight = pane[1][1] - pane[0][1]
            self.pos_x, self.pos_y = XY_From_Grid(self.width, self.hight, Nx, Ny, gap_x, gap_y, pane)
        if pane == 'main':
            Nx = 1
            Ny = 1
            pane = super(Button, self).head()
            self.width = 100
            head_pane = super(Button, self).head()
            self.hight = head_pane[1][1] - head_pane[0][1]
            self.pos_x = pane [1][0] - self.width
            self.pos_y = pane [0][1]
        if pane == 'menu:shop':
            Nx = 2
            Ny = 1
            self.width = (self.menu_w - (Nx+1)*gap_x)/Nx
            print(self.menu_w)
            pane_menu = super(Button, self).menu()
            pane_alert = super(Button, self).alert()

            pane_menu[0][1] = pane_alert[0][1] - 100
            pane = [pane_menu[0],pane_menu[1]]
            print (pane)
            self.pos_x, self.pos_y = XY_From_Grid(self.width, self.hight, Nx, Ny, gap_x, gap_y, pane)
        if pane == 'menu:main':
            Nx = 1
            Ny = 3
            pane = super(Button, self).menu()
            self.width = (pane[1][0] - pane[0][0]) - gap_x*2
            self.pos_x, self.pos_y = XY_From_Grid(self.width, self.hight, Nx, Ny, gap_x, gap_y, pane)


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

    '''def Action (self):
        if self.interface_group:
            return self.act(self.interface_group)
        else:
            self.act()'''

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
