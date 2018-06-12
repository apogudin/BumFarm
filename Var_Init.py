import pygame
import os
import sys
from Interface import *
from Objects import *

pygame.init()

Font25 = pygame.font.SysFont('Colibri', 25)
Font12 = pygame.font.SysFont('Colibri', 12)


Budget = Coins()
Bums = Bum()
Station = BusStation()

clock = pygame.time.Clock()

Image_Bum = pygame.image.load(os.path.join('images','Bum.png'))
Image_Null1 = pygame.image.load(os.path.join('images', 'Color1.png'))
Image_Null2 = pygame.image.load(os.path.join('images', 'Color2.png'))
Image_Null3 = pygame.image.load(os.path.join('images', 'Color3.png'))
Image_Null5 = pygame.image.load(os.path.join('images', 'Color5.png'))
Image_Null4 = pygame.image.load(os.path.join('images', 'Color4.png'))





screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)





Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2

pygame.time.set_timer(Time1sec, 1000)

alert = ''
done = False

Worker = Actor()

Pane_Head = Pane('head')
Pane_Shop = Pane('shop')
Pane_News = Pane('news')
Pane_Alert = Pane('alert')
Pane_Main = Pane('main')
Pane_Menu_Main = Pane('menu:main')
Pane_Menu_Shop = Pane('menu:shop')
Pane_Map = Pane('map')


Button_Menu = Button('Menu', Worker.switch, Bums)

Button_Shop11 = Button('BUM', Worker.switch, Bums)
Button_Shop12 = Button('STATION', Worker.switch, Station)
Button_Shop13 = Button('SHOP13', Worker.switch, Bums)
Button_Shop14 = Button('SHOP14', Worker.switch, Bums)
Button_Shop15 = Button('SHOP15', Worker.switch, Bums)
Button_Shop21 = Button('SHOP21', Worker.switch, Bums)
Button_Shop22 = Button('SHOP22', Worker.switch, Bums)
Button_Shop23 = Button('SHOP23', Worker.switch, Bums)
Button_Shop24 = Button('SHOP24', Worker.switch, Bums)
Button_Shop25 = Button('SHOP25', Worker.switch, Bums)

Button_Head1 = Button('', Worker.switch, Bums)
Button_Head2 = Button('', Worker.switch, Bums)
Button_Head3 = Button('', Worker.switch, Bums)

Button_Quit = Button('EXIT', Worker.nothing)
Button_Menu_Main2 = Button('MAIN2', Worker.buy)

Button_Menu_Shop1 = Button('BUY1', Worker.buy)
Button_Menu_Shop2 = Button('BUY2', Worker.buy)

Building1 = Button ('yep', Worker.buy)


Pane_Head.Button_Init([Button_Head1, Button_Head2, Button_Head3])
Pane_Shop.Button_Init([Button_Shop11, Button_Shop12, Button_Shop13, Button_Shop14, Button_Shop15,
                       Button_Shop21, Button_Shop22, Button_Shop23, Button_Shop24, Button_Shop25, ])
Pane_Main.Button_Init([Button_Menu])
Pane_Menu_Main.Button_Init([Button_Quit, Button_Menu_Main2])
Pane_Menu_Shop.Button_Init([Button_Menu_Shop1, Button_Menu_Shop2])

Img_B_Shop = Image('Button_Shop.png', BUTTON_DICT['shop'])
Img_B_Menu_Shop = Image('Button_Menu_Shop.png', BUTTON_DICT['menu:shop'])
Img_B_Main = Image('Button_Main.png', BUTTON_DICT['main'])
Img_B_Menu_Main = Image('Button_Menu_Main.png', BUTTON_DICT['menu:main'])
Img_B_Head = Image('Button_Head.png', BUTTON_DICT['head'])
Img_Bg1 = Image('Color1.png', [Pane_Head, Pane_Main, Pane_Alert, Pane_Shop])
Img_Bg2 = Image('Color2.png', [Pane_Menu_Main, Pane_Menu_Shop, Pane_News, Building1])


Img_Map1 = Image('map.png', [Pane_Map])

Text01 = Text(Font25, [Button_Head1, Button_Head2, Button_Head3], 'type')




#Text_Resourses('Всего денег', Budget.amount, 10, Font25, screen, 25, 1)
##Text_Resourses('Всего бомжей', Bums.amount, 10, Font25, screen, 25, 2)
#Text_Resourses('Всего остановок', Station.amount, 10, Font25, screen, 25, 3)
#Text_Resourses('Мест в останвках', Station.limit-Station.Bums, 10, Font25, screen, 25, 4)



for text in TEXT_LIST:
    text.screen  = screen
for pane in PANE_LIST:
    pane.screen = screen
for image in IMAGE_LIST:
    image.screen = screen
for group in BUTTON_DICT:
    for button in BUTTON_DICT[group]:
        button.screen = screen
        button.font = Font12
