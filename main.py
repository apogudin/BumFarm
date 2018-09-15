import pygame
from Var_Init import *
from Interface import *
from MyFunctions import *

Obstacle_Stones.rand_stones(Farm_RUS.tile_info, 20)

while Worker.interface_state['continue_game']:
    clock.tick(60)
    #ACTIVE_PANES = CONS_ACTIVE_PANE + TEMP_ACTIVE_PANE
    #ACTIVE_PANES = BUTTON_DRAW_GROUPS['static']

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    Pane_Map.Move(keys)
    screen.fill([255,255,255])
    Pane_Map.draw()

    for event in pygame.event.get():
        if not Worker.interface_state['constructing_mode']:
            if event.type == pygame.MOUSEMOTION:
                Check_All(PANE_INIT_DICT, mouse_pos)
                #CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('BEFORE: ', Worker.item_state)
                if Pane_Map.IsOn(mouse_pos):
                    active_tile = Farm_RUS.Activate(mouse_pos)
                    PANE_INIT_DICT['MENU']['buttons_area']['menu:building']['button_dict'] = active_tile
                    if active_tile is not None:
                        create_buttons(PANE_INIT_DICT['MENU']['buttons_area'], 'menu:building', IMAGE_DICT, BUTTON_DICT, BUTTON_DRAW_GROUPS)
                    else:
                        Worker.clear_buttons_areas(PANE_INIT_DICT, 'MENU')
                        #create_buttons(Worker.item_state['item'].buttons_dict, IMAGE_DICT,[3,2],[80,120], screen)
                        #TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]
                        #for button in BUTTON_DICT["menu:building"]:
                        #    button.screen = screen
                        #    button.font = Font12
                        #    button.Worker = Worker
                        #for image in IMAGE_DICT["menu:building"]:
                        #    image.screen = screen


                    #else:
                    #    TEMP_ACTIVE_PANE = []
                else:
                    Check_All(PANE_INIT_DICT, mouse_pos, True)
                    #Worker_Output = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    #if Worker_Output == 'EXIT':
                    #    done = True
                    #elif Worker_Output is not None:
                    #    TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]
                print('AFTER: ', Worker.item_state)

        else:
            if event.type == pygame.MOUSEMOTION:
                Check_All(PANE_INIT_DICT, mouse_pos)
                #CheckAll(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
            elif keys[pygame.K_r]:
                Worker.item_rotate = (Worker.item_rotate+1) % 4
                Worker.item_state['item'].tile = rotate_build(Worker.item_state['item'].tile, True)
            elif keys[pygame.K_t]:
                Worker.item_rotate = (Worker.item_rotate+3) % 4
                Worker.item_state['item'].tile = rotate_build(Worker.item_state['item'].tile)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('BEFORE: ', Worker.item_state)
                Pane_Map.user_map_place = mouse_pos
                if Farm_RUS.can_build(mouse_pos) and Pane_Map.IsOn(mouse_pos):
                    Farm_RUS.add(mouse_pos)
                else:
                    Check_All(PANE_INIT_DICT, mouse_pos, True)
                    #Worker_Output = CheckAll_And_Action(ACTIVE_PANES, BUTTON_DICT, mouse_pos)
                    #if Worker_Output is not None:
                    #    TEMP_ACTIVE_PANE = PANE_DICT[Worker_Output]
                Worker.switch_constructing_mode()
                print('AFTER: ', Worker.item_state)
        if event.type == Time1sec:
            Budget.income(Bums.amount*10)
        if event.type == Alert_Event:
            alert = ''

    #"Призрак" при строительстве


    if  Worker.interface_state['constructing_mode'] and hasattr(Worker.item_state['item'], 'img') and Pane_Map.IsOn(mouse_pos):
        pos_y, pos_x = Farm_RUS.WhoIsOn(mouse_pos)
        pos_x = (pos_x - Pane_Map.NULL_tile_draw[0] - Worker.item_state['item'].pivot[1]) * Pane_Map.tile_size + Pane_Map.NULL_draw[0]
        pos_y = (pos_y - Pane_Map.NULL_tile_draw[1] - Worker.item_state['item'].pivot[0]) * Pane_Map.tile_size + Pane_Map.NULL_draw[1]
        if Farm_RUS.can_build(mouse_pos):
            Worker.item_state['item'].img.draw(pos_x, pos_y, [4,4],[1,Worker.item_rotate])
        else:
            Worker.item_state['item'].img.draw(pos_x, pos_y, [4,4],[0,Worker.item_rotate])


    for pane in PANE_INIT_DICT:
        if PANE_INIT_DICT[pane]['pane_obj'].img is not None:
            PANE_INIT_DICT[pane]['pane_obj'].draw()
        if PANE_INIT_DICT[pane]['buttons_area'] is not None:
            for button_area in PANE_INIT_DICT[pane]['buttons_area']:
                for button in PANE_INIT_DICT[pane]['buttons_area'][button_area]['button_obj_list']:
                    if PANE_INIT_DICT[pane]['buttons_area'][button_area]['draw']:
                        button.draw()

#############больше нет
#    for pane in PANE_DRAW_LIST:
#        pane.draw_pane()

#############весь драв листaaaa
#    for pane in ACTIVE_PANES:
#        pane.draw_Button()


    Text_Alert(alert, 25, win_size[1], Font25, screen)
    Text01.draw([str(Budget.amount), str(Bums.amount), str(Bums.amount)])


    if PANE_INIT_DICT['MENU']['buttons_area']['menu:building']['draw']:
            Text02.draw([str(Worker.item_state['item'].objects_dict[Worker.item_state['item_id']]['bums'])+' бомжей',
            str(Worker.item_state['item'].objects_dict[Worker.item_state['item_id']]['limit'])+' лимит бомжей',
            str(Worker.item_state['item'].objects_dict[Worker.item_state['item_id']]['lvl'])+' уровень'])
    pygame.display.flip()

pygame.quit()
