import pygame
import os, sys
from MyClasses import *
from MyFunctions import *

pygame.init()

Budget = Coins()
Bums = Bum()
Station = BusStation()

clock = pygame.time.Clock()

Image_Bum = pygame.image.load(os.path.join('images','Bum.png'))
Image_Null1 = pygame.image.load(os.path.join('images', 'Color1.png'))
Image_Null2 = pygame.image.load(os.path.join('images', 'Color2.png'))
Image_Null3 = pygame.image.load(os.path.join('images', 'Color3.png'))

screen_x = 1024
screen_y = 768

win_size = [screen_x, screen_y]
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption('Бомжеферма')
pygame.display.set_icon(Image_Bum)

Time1sec = pygame.USEREVENT+1
Alert_Event = pygame.USEREVENT+2
pygame.time.set_timer(Time1sec, 1000)

alert = ''
font = pygame.font.SysFont('Colibri', 25)
done = False

#Button_Quit = Old_Button('Выйти', win_size, 0)
#Button_Buy_Bum = Old_Button('Купить бомжа', win_size, 2)
#Button_Buy_Station = Old_Button('Купить остановку', win_size, 4)
#Button_Bum_Station = Old_Button('Посадить бомжа', win_size, 5)

Button_Buy_Bum = Button('Купить бомжа','shop',[0,0],Image_Null3,Image_Null2,win_size)
Button_Buy_Station = Button('ОСТАНОВКА','shop',[1,0],Image_Null3,Image_Null2,win_size)
TEST_BUTTON20 = Button('TEST20','shop',[2,0],Image_Null3,Image_Null2,win_size)
Button_Bum_Station = Button('Поселить бомжа','shop',[0,1],Image_Null3,Image_Null2,win_size)
#Button_Menu = Button('Menu','menu',[0,0],Image_Null3,Image_Null2,win_size)
Button_Quit = Button('ВЫЙТИ','shop',[2,1],Image_Null3,Image_Null2,win_size)

#Button_Menu = New_Button('MENU_TEST', 300, 300, 200, 20, Image_Null1, Image_Null2)

#NewButt = New_Button('TEST')

Panes = Interface_Pane(win_size)

menu_type = 1
while done == False:
    clock.tick(60)

    #принимаем значение переключателя МЕНЮ и создаём все кнопки МЕНЮ

    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEMOTION:
            Button_Buy_Bum.IsOn(mouse_pos)
            Button_Quit.IsOn(mouse_pos)
            Button_Buy_Station.IsOn(mouse_pos)
            Button_Bum_Station.IsOn(mouse_pos)
            #Button_Menu.IsOn(mouse_pos)



        if event.type == pygame.MOUSEBUTTONDOWN:
            if Button_Buy_Bum.IsOn(mouse_pos):
                Bums.buy()
                Budget.outgo(Bums.cost)
            if Button_Quit.IsOn(mouse_pos):
                done = True
            if Button_Buy_Station.IsOn(mouse_pos):
                Station.buy()
                Budget.outgo(Station.cost)
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

            #if Button_Menu.IsOn(mouse_pos):            #отладка
            #    menu_type *= -1

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''


    screen.fill([255,255,255])

    #Button_Menu.draw(screen)

    #if menu_type == 1:
    Img_Fill(Image_Null1,Panes.shop(), screen)    #тут будет блок проверки типа меню и отрисовка

    Img_Fill(Image_Null1,Panes.head(), screen)
    Img_Fill(Image_Null2,Panes.news(), screen)
    Img_Fill(Image_Null1,Panes.alert(), screen)
    Img_Fill(Image_Null2,Panes.menu_main(), screen)



#    Button_Menu.draw(screen,font_size=12)
    Button_Buy_Bum.draw(screen, font_size=12)
    Button_Quit.draw(screen,font_size=12)
    Button_Bum_Station.draw(screen,font_size=12)
    Button_Buy_Station.draw(screen,font_size=12)

    Text_Resourses('Всего денег', Budget.amount, 10, font, screen, 25, 1)
    Text_Resourses('Всего бомжей', Bums.amount, 10, font, screen, 25, 2)
    Text_Resourses('Всего остановок', Station.amount, 10, font, screen, 25, 3)
    Text_Resourses('Мест в останвках', Station.limit-Station.Bums, 10, font, screen, 25, 4)

    Text_Alert(alert, 25, screen_y, font, screen)

    pygame.display.flip()

pygame.quit()