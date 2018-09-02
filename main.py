import pygame
from Var_Init import *
from Interface import *
from MyFunctions import *

rand_stones(Farm_RUS.tile_info, Img_Stone, 20)

while done == False:
    clock.tick(60)
    ACTIVE_PANES = CONS_ACTIVE_PANE + TEMP_ACTIVE_PANE
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    Pane_Map.Move(keys)
    screen.fill([255,255,255])
    Pane_Map.draw()

    for event in pygame.event.get():
        if Worker.map_mode == 'mode_base':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Pane_Map.IsOn(mouse_pos):
                    Worker_Output = Farm_RUS.Activate(mouse_pos)
                    if Worker_Output is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]
                    else:
                        TEMP_ACTIVE_PANE = []
                else:
                    Worker_Output = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    if Worker_Output == 'EXIT':
                        done = True
                    elif Worker_Output is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]


        elif Worker.map_mode == 'mode_constructing':
            if event.type == pygame.MOUSEMOTION:
                CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif keys[pygame.K_r]:
                Worker.item_rotate = (Worker.item_rotate+1) % 4
                Worker.item.tile = rotate_build(Worker.item.tile, True)
            elif keys[pygame.K_t]:
                Worker.item_rotate = (Worker.item_rotate+3) % 4
                Worker.item.tile = rotate_build(Worker.item.tile)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                Pane_Map.user_map_place = mouse_pos
                if Farm_RUS.can_build(mouse_pos) and Pane_Map.IsOn(mouse_pos):
                    Farm_RUS.add(mouse_pos)
                else:
                    Worker_Output = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    if Worker_Output is not None:
                        TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]
                Worker.switch_map()

        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    #"Призрак" при строительстве
    if  Worker.map_mode == 'mode_constructing' and hasattr(Worker.item, 'img') and Pane_Map.IsOn(mouse_pos):
        pos_y, pos_x = Farm_RUS.WhoIsOn(mouse_pos)
        pos_x = (pos_x - Pane_Map.NULL_tile_draw[0]) * Pane_Map.tile_size + Pane_Map.NULL_draw[0]
        pos_y = (pos_y - Pane_Map.NULL_tile_draw[1]) * Pane_Map.tile_size + Pane_Map.NULL_draw[1]
        if Farm_RUS.can_build(mouse_pos):
            Worker.item.img.draw(pos_x, pos_y, [4,4],[1,Worker.item_rotate])
        else:
            Worker.item.img.draw(pos_x, pos_y, [4,4],[0,Worker.item_rotate])

    for pane in PANE_DRAW_LIST:
        pane.draw_pane()
    for pane in ACTIVE_PANES:
        pane.draw_Button()

    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Station.amount)])

    if TEMP_ACTIVE_PANE == [Pane_Menu_Building]:
            Text02.draw([str(Worker.item.objects_dict[Worker.item_id]['bums'])+' бомжей',
            str(Worker.item.objects_dict[Worker.item_id]['limit'])+' лимит бомжей',
            str(Worker.item.objects_dict[Worker.item_id]['lvl'])+' уровень'])
    pygame.display.flip()

pygame.quit()
