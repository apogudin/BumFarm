from Var_Init import *

Obstacle_Stones.rand_stones(Farm_EUR.tile_info, 20)
active_tile = None
frame = 0
fps = 0

while Worker.interface_state['continue_game']:
    fps += 1
    clock.tick(60)
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    Pane_Map.Move(keys)
    screen.fill([255,255,255])

    for event in pygame.event.get():
        #Обычный режим
        if not Worker.interface_state['constructing_mode']:
            if event.type == pygame.MOUSEMOTION:
                Check_All(PANE_INIT_DICT, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Pane_Map.IsOn(mouse_pos):
                    active_tile = Farm_EUR.Activate(mouse_pos)
                    if active_tile is not None:
                        PANE_INIT_DICT['MENU']['buttons_area']['menu:building']['button_dict'] = active_tile
                        create_buttons(PANE_INIT_DICT['MENU']['buttons_area'], 'menu:building', IMAGE_DICT)
                    else:
                        Worker.clear_buttons_areas(PANE_INIT_DICT, 'MENU')
                else:
                    button_params = Check_All(PANE_INIT_DICT, mouse_pos, True)
                    if button_params is not None and button_params['rebuild']:
                        if Worker.item_state['item'].objects_dict[Worker.item_state['item_id']]['lvl'] >= len( Worker.item_state['item'].lvl_list):
                            PANE_INIT_DICT['MENU']['buttons_area']['menu:building']['button_dict'] = Worker.item_state['item'].button_dict_limited
                            create_buttons(PANE_INIT_DICT['MENU']['buttons_area'], 'menu:building', IMAGE_DICT)
            elif keys[pygame.K_1]:
                Worker.interface_state['news_event'] = 'event1'
            elif keys[pygame.K_2]:
                Worker.interface_state['news_event'] = 'event2'
            elif keys[pygame.K_3]:
                Worker.interface_state['news_event'] = 'event3'
        #Режим строительства
        else:
            if event.type == pygame.MOUSEMOTION:
                Check_All(PANE_INIT_DICT, mouse_pos)

            #Поворот здания
            elif keys[pygame.K_r]:
                Worker.item_rotate = (Worker.item_rotate+1) % 4
                Worker.item_state['item'].tile = rotate_build(Worker.item_state['item'].tile, True)
            elif keys[pygame.K_t]:
                Worker.item_rotate = (Worker.item_rotate+3) % 4
                Worker.item_state['item'].tile = rotate_build(Worker.item_state['item'].tile)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Farm_EUR.can_build(mouse_pos) and Pane_Map.IsOn(mouse_pos):
                    Farm_EUR.add(mouse_pos)
                else:
                    Check_All(PANE_INIT_DICT, mouse_pos, True)
                Worker.switch_constructing_mode()

        if event.type == Timer1Sec:
            Player.resources_update()
            frame = (frame + 1) % 3
            print (fps)
            fps = 0

        #Новостная лента, не зависящая от процесса игры
        if event.type == Timer10Sec:
            Txt_News.add_jobs('event3')

    #Отрисовка карты
    Pane_Map.draw(frame)

    #Отрисовка контура здания в режиме строительства
    if  Worker.interface_state['constructing_mode'] and hasattr(Worker.item_state['item'], 'img') and Pane_Map.IsOn(mouse_pos):
        pos_y, pos_x = Farm_EUR.WhoIsOn(mouse_pos)
        pos_x = (pos_x - Pane_Map.NULL_tile_draw[0] - Worker.item_state['item'].pivot[1]) * Pane_Map.tile_size + Pane_Map.NULL_draw[0]
        pos_y = (pos_y - Pane_Map.NULL_tile_draw[1] - Worker.item_state['item'].pivot[0]) * Pane_Map.tile_size + Pane_Map.NULL_draw[1]
        if Farm_EUR.can_build(mouse_pos):
            Worker.item_state['item'].img.draw(pos_x, pos_y, [12,8],[1,Worker.item_rotate])
        else:
            Worker.item_state['item'].img.draw(pos_x, pos_y, [12,8],[0,Worker.item_rotate])

    #Отрисовка панелей и кнопок
    for pane in PANE_INIT_DICT:
        if PANE_INIT_DICT[pane]['pane_obj'].img is not None:
            PANE_INIT_DICT[pane]['pane_obj'].draw()
        if PANE_INIT_DICT[pane]['buttons_area'] is not None:
            for button_area in PANE_INIT_DICT[pane]['buttons_area']:
                for button in PANE_INIT_DICT[pane]['buttons_area'][button_area]['button_obj_list']:
                    if PANE_INIT_DICT[pane]['buttons_area'][button_area]['draw']:
                        button.draw()

    Txt_Resourses.draw()
    if PANE_INIT_DICT['MENU']['buttons_area']['menu:building']['draw']:
        Txt_Info_Screen.draw()
        Txt_Info_Annotation.draw()
    elif PANE_INIT_DICT['MENU']['buttons_area']['menu:shop']['draw']:
        Txt_Shop_Annotation.draw()
    elif PANE_INIT_DICT['MENU']['buttons_area']['menu:text:resources']['draw']:
        Txt_Resourses_Annotation.draw()

    #Новостная лента согласно игровым событиям
    Player.get_news(Txt_News)
    Txt_News.get_event_and_draw()

    pygame.display.flip()

pygame.quit()
