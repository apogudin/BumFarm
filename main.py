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
        if Worker.map_mode == 'base':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                out = CheckAll_And_Action(INTERFACE_GROUPS, BUTTON_DICT, mouse_pos)
                if out is not None:
                    TEMP_INTERFACE_GROUP = [out]

                #Чтоб сейчас хоть как-то по-человечески выходить
                if Button_Quit.IsOn(mouse_pos):
                    done = True

        elif Worker.map_mode == 'building':
            if event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pane_Map.user_map_place = mouse_pos
                if Pane_Map.IsOn(mouse_pos):
                    Pane_Map.Button_Init([Building1])
                    print('if')
                else:
                    Worker.switch_map()
                    print('else')


        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    #ОТРИСОВКА
    screen.fill([255,255,255])

    for pane in PANE_DRAW:
        pane.draw_pane()
    for pane in INTERFACE_GROUPS:
        pane.draw_Button()

    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Station.amount)])
    pygame.display.flip()

pygame.quit()
