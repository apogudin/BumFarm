import pygame
from Var_Init import *
from Interface import *
from MyFunctions import *

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

    #BUG! pane menu_ - прорисовываются тоже все!
    for pane in PANES_LIST:
        pane.fill()

    for group in INTERFACE_GROUPS:
        if group in BUTTON_DICT:
            for button in BUTTON_DICT[group]:
                button.draw()


    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Station.amount)])
    pygame.display.flip()

pygame.quit()

#print(Button_Menu.size(), Button_Head3.size(), Button_Quit.size(),
# Button_Menu_Shop2.size())
