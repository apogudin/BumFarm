import pygame
from Var_Init import *
from Interface import *
from MyFunctions import *

while done == False:
    clock.tick(60)


    ACTIVE_PANES = CONS_ACTIVE_PANE + TEMP_ACTIVE_PANE
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    Pane_Map.Move(keys)



    for event in pygame.event.get():

        if Worker.map_mode == 'base':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                work_out = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                if work_out == 'EXIT':
                    done = True
                elif work_out is not None:
                    TEMP_ACTIVE_PANE = PANE_DICT[work_out]

        elif Worker.map_mode == 'building':
            
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pane_Map.user_map_place = mouse_pos
                if Pane_Map.IsOn(mouse_pos):
                    print(Buildings01.WhoIsOn(mouse_pos))
                    print(Worker.item)
                    print(Worker.map_mode)
                else:
                    Worker.switch_map()
                    work_out = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    if work_out is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[work_out]
                    print(Worker.map_mode)


        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    screen.fill([255,255,255])
    Pane_Map.bg_draw()

    for pane in PANE_DRAW_LIST:
        pane.draw_pane()
    for pane in ACTIVE_PANES:
        pane.draw_Button()

    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Station.amount)])
    pygame.display.flip()

pygame.quit()
