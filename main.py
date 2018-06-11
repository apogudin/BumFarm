import pygame
from Var_Init import *
from Interface import *
from MyFunctions import *
global a
a = 10
while done == False:
    clock.tick(60)
    INTERFACE_GROUPS = CONS_INTERFACE_GROUP + TEMP_INTERFACE_GROUP

    #ЭВЕНТЫ
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEMOTION:
            CheckAll(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            out = CheckAll_And_Action(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)

            if out is not None:
                TEMP_INTERFACE_GROUP = [out]

            #Чтоб сейчас хоть как-то по-человечески выходить
            if Button_Quit.IsOn(mouse_pos):
                done = True

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    #ОТРИСОВКА
    screen.fill([255,255,255])

    Img_Fill(Image_Null1,Pane_Shop.pane, screen)
    Img_Fill(Image_Null1,Pane_Head.pane, screen)
    Img_Fill(Image_Null2,Pane_News.pane, screen)
    Img_Fill(Image_Null1,Pane_Alert.pane, screen)
    Img_Fill(Image_Null2,Pane_Menu_Main.pane, screen)

    for group in INTERFACE_GROUPS:
        if group in BUTTON_DICT:
            for button in BUTTON_DICT[group]:
                button.draw(screen)

    Text_Resourses('Всего денег', Budget.amount, 10, font, screen, 25, 1)
    Text_Resourses('Всего бомжей', Bums.amount, 10, font, screen, 25, 2)
    Text_Resourses('Всего остановок', Station.amount, 10, font, screen, 25, 3)
    Text_Resourses('Мест в останвках', Station.limit-Station.Bums, 10, font, screen, 25, 4)
    Text_Alert(alert, 25, win_size[1], font, screen)

    pygame.display.flip()

pygame.quit()
