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
    screen.fill([255,255,255])
    Pane_Map.draw_pane()

    for event in pygame.event.get():
        if Worker.map_mode == 'mode_base':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Pane_Map.IsOn(mouse_pos):
                    work_out = Farm.Activate(mouse_pos)
                    if work_out is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[work_out]
                    else:
                        TEMP_ACTIVE_PANE = []
                else:
                    work_out = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    if work_out == 'EXIT':
                        done = True
                    elif work_out is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[work_out]

        elif Worker.map_mode == 'mode_constructing':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pane_Map.user_map_place = mouse_pos
                if Pane_Map.IsOn(mouse_pos):
                    Farm.add(mouse_pos)
                else:
                    Worker.switch_map()
                    work_out = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    if work_out is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[work_out]
                Worker.switch_map()

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''
    if  Worker.map_mode == 'mode_constructing':
        pos_y, pos_x = Farm.WhoIsOn(mouse_pos)
        pos_x = (pos_x - Pane_Map.NULL_tile_draw[0]) * Pane_Map.tile_size + Pane_Map.NULL_draw[0]
        pos_y = (pos_y - Pane_Map.NULL_tile_draw[1]) * Pane_Map.tile_size + Pane_Map.NULL_draw[1]
        Worker.item.img.draw(pos_x, pos_y, [1,2])

    Pane_Map.draw_Button()
    for pane in PANE_DRAW_LIST:
        pane.draw_pane()
    for pane in ACTIVE_PANES:
        pane.draw_Button()



    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Station.amount)])

    if TEMP_ACTIVE_PANE == [Pane_Menu_Building]:
            Text02.draw([str(Worker.item.objects_dict[Worker.item_id][0])+' Бомжей',
            str(Worker.item.objects_dict[Worker.item_id][1])+' lvl',
            str(Worker.item.objects_dict[Worker.item_id][2])+' upgrade'])
    pygame.display.flip()

pygame.quit()

for group in BUTTON_DICT:
    for button in BUTTON_DICT[group]:
        print(button.get_size(), button.pane_type)
