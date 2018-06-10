import pygame
from Var_Init import *

while done == False:
    clock.tick(60)

    #ЭВЕНТЫ
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            CheckAll(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            CheckAll_And_Action(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)

            #Чтоб сейчас хоть как-то по-человечески выходить
            if Button_Quit.IsOn(mouse_pos):
                done = True

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    #ОТРИСОВКА
    screen.fill([255,255,255])

    Img_Fill(Image_Null1,Panes.shop(), screen)
    Img_Fill(Image_Null1,Panes.head(), screen)
    Img_Fill(Image_Null2,Panes.news(), screen)
    Img_Fill(Image_Null1,Panes.alert(), screen)
    Img_Fill(Image_Null2,Panes.menu_main(), screen)

    Button_Menu.draw(screen,font_size=12)
    Button_Buy_Bum.draw(screen, font_size=12)
    Button_Quit.draw(screen,font_size=12)
    Button_Bum_Station.draw(screen,font_size=12)
    Button_Buy_Station.draw(screen,font_size=12)

    Text_Resourses('Всего денег', Budget.amount, 10, font, screen, 25, 1)
    Text_Resourses('Всего бомжей', Bums.amount, 10, font, screen, 25, 2)
    Text_Resourses('Всего остановок', Station.amount, 10, font, screen, 25, 3)
    Text_Resourses('Мест в останвках', Station.limit-Station.Bums, 10, font, screen, 25, 4)
    Text_Alert(alert, 25, win_size[1], font, screen)

    pygame.display.flip()

pygame.quit()
