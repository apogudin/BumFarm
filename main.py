import pygame
import os, sys
from MyClasses import *
from MyFunctions import *
from Global import *

pygame.init()

Budget = Coins()
Bums = Bum()
Station = BusStation()

clock = pygame.time.Clock()

Image_Bum = pygame.image.load(os.path.join('images','Bum.png'))
Image_Null1 = pygame.image.load(os.path.join('images', 'Color1.png'))
Image_Null2 = pygame.image.load(os.path.join('images', 'Color2.png'))
Image_Null3 = pygame.image.load(os.path.join('images', 'Color3.png'))



screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)

Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2

pygame.time.set_timer(Time1sec, 1000)

alert = ''
font = pygame.font.SysFont('Colibri', 25)
done = False


Button_Buy_Bum = Button('Купить бомжа','shop',[0,0],Image_Null3,Image_Null2, Bums.buy)
Button_Buy_Station = Button('ОСТАНОВКА','shop',[1,0],Image_Null3,Image_Null2, Station.buy)
TEST_BUTTON20 = Button('TEST20','shop',[2,0],Image_Null3,Image_Null2, Bums.buy)
Button_Bum_Station = Button('Поселить бомжа','shop',[0,1],Image_Null3,Image_Null2, Station.setBum)
Button_Menu = Button('Menu','menu',[0,0],Image_Null3,Image_Null2, Bums.buy)
Button_Quit = Button('ВЫЙТИ','shop',[2,1],Image_Null3,Image_Null2, Bums.buy)


Panes = Interface_Pane()

menu_type = 1
while done == False:
    clock.tick(60)


    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            CheckAll(BUTTONS_LIST, mouse_pos)
            #Button_Buy_Bum.IsOn(mouse_pos)
            #Button_Quit.IsOn(mouse_pos)
            #Button_Menu.IsOn(mouse_pos)
            #if menu_type == 2:
            #    Button_Buy_Station.IsOn(mouse_pos)
            #if menu_type == 1:
            #    Button_Bum_Station.IsOn(mouse_pos)


        if event.type == pygame.MOUSEBUTTONDOWN:
            CheckAll_And_Action(BUTTONS_LIST, mouse_pos)

            #if Button_Menu.IsOn(mouse_pos):
            #    menu_type = 2
            #f Button_Buy_Bum.IsOn(mouse_pos):
            #    menu_type = 1
                #menu_type = [type, param]

            #    Button_Buy_Bum.Action()
                #Bums.buy()
                #Budget.outgo(Bums.cost)
            if Button_Quit.IsOn(mouse_pos):
                done = True
            if menu_type == 2:
                if Button_Buy_Station.IsOn(mouse_pos):
                    Station.buy()
                    Budget.outgo(Station.cost)
            if menu_type == 1:
                if Button_Bum_Station.IsOn(mouse_pos):
                    if Station.amount > 0 and Station.limit > Station.Bums and Bums.amount > 0:
                        Station.setBum()
                        Bums.set()
                    elif Station.limit == Station.Bums and Station.amount != 0:
                        alert = Temporary_Text('Все остановки заняты бомжами', Alert_Event, 5000)
                    elif Bums.amount <= 0:
                        alert = Temporary_Text('Закончились бомжи', Alert_Event, 5000)
                    elif Station.amount == 0:
                        alert = Temporary_Text('Остановок нет', Alert_Event, 5000)


            if Button_Quit.IsOn(mouse_pos):
                done = True

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''


    screen.fill([255,255,255])

    Img_Fill(Image_Null1,Panes.shop(), screen)    #тут будет блок проверки типа меню и отрисовка

    Img_Fill(Image_Null1,Panes.head(), screen)
    Img_Fill(Image_Null2,Panes.news(), screen)
    Img_Fill(Image_Null1,Panes.alert(), screen)
    Img_Fill(Image_Null2,Panes.menu_main(), screen)



    Button_Menu.draw(screen,font_size=12)
    Button_Buy_Bum.draw(screen, font_size=12)
    Button_Quit.draw(screen,font_size=12)
    if menu_type == 1:
        Button_Bum_Station.draw(screen,font_size=12)
    if menu_type == 2:
        Button_Buy_Station.draw(screen,font_size=12)

    Text_Resourses('Всего денег', Budget.amount, 10, font, screen, 25, 1)
    Text_Resourses('Всего бомжей', Bums.amount, 10, font, screen, 25, 2)
    Text_Resourses('Всего остановок', Station.amount, 10, font, screen, 25, 3)
    Text_Resourses('Мест в останвках', Station.limit-Station.Bums, 10, font, screen, 25, 4)

    Text_Alert(alert, 25, win_size[1], font, screen)

    pygame.display.flip()

pygame.quit()
print(BUTTONS_LIST)
print(BUTTON_DICT)
