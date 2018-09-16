from MyFunctions import *


#Области экрана
class Pane():
    def __init__(self, PANE_INIT_DICT, pane_name, PANE_DICT):
        #для выбранного type высчитывает область: левый-верхний, правый-нижний угол
        self.name = pane_name
        self.area = PANE_INIT_DICT[pane_name]['area']
        self.area_type = PANE_INIT_DICT[pane_name]['pane_type']
        self.img = None

    def draw(self):
        Img_Fill(self.img, self.area, self.screen)

    def IsOn (self, mouse_pos):
        if (self.area[0][0] < mouse_pos[0] < self.area[1][0]) :
            if (self.area[0][1] < mouse_pos[1] < self.area[1][1]):
                return True
        return False

    def get_size(self):
        return(self.area)



class Button():
    #Кнопки с любыми шрифтами, размерами, положением.
    def __init__(self, name, action, item = None):
        self.action = action
        self.name = name
        self.item = item
        self.state = 'off'
        self.params = {'item_id': None, 'rebuild': False}

    def IsOn (self, mouse_pos):
        if (self.pos_x < mouse_pos[0] < self.pos_x + self.width) :
            if (self.pos_y < mouse_pos[1] < self.pos_y + self.height):
                self.state = 'on'
                return True
        self.state = 'off'
        return False

    def draw (self):
        text = self.font.render(self.name, True, [0,0,0])
        self.img.draw_Button(self.pos_x, self.pos_y, self.state)
        #Img_Fill(self.bg_draw,[[self.pos_x,self.pos_y],[self.pos_x+self.width, self.pos_y+self.height]], self.screen)
        self.screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y +(self.height/2 - text.get_height()/2)))

    def Activate(self):
        if self.item is not None:
            self.Worker.item_state['item'] = self.item
        self.params['item'] = self.Worker.item_state['item']
        self.params['item_id'] = self.Worker.item_state['item_id']
        self.action(self.params)
        return self.params

    def get_size(self):
        return [self.width, self.height]

    def pos(self):
        return [self.pos_x, self.pos_y]


# BUG: кажется, можно объединять с Farm.
class Map():
    def __init__(self, pane, NxNy, building_list = []):
        self.pane = pane
        self.pane_type = 'Map'
        self.NxNy = NxNy
        self.building_list = building_list
        self.pane_width = self.pane[1][0] - self.pane[0][0]
        self.pane_height = self.pane[1][1] - self.pane[0][1]
        self.tile_size = 50
        self.tile_visible_NxNy = [self.pane_width//self.tile_size+1, self.pane_height//self.tile_size+1]
        self.img = None

        self.GRID_pos = [[[i,j] for i in range(NxNy[0])] for j in range(NxNy[1])]
        self.GRID_coo = [[[i*self.tile_size, j*self.tile_size] for i in range(NxNy[0])] for j in range(NxNy[1])]

        self.NULL = [0,0]
        self.NULL_tile_draw = [0,0]
        self.NULL_draw =  [self.pane[0][0], self.pane[1][1]]

    def IsOn (self, mouse_pos):
        if (self.pane[0][0] < mouse_pos[0] < self.pane[1][0]) :
            if (self.pane[0][1] < mouse_pos[1] < self.pane[1][1]):
                return True
        return False

    def Move(self, keys):
        speed = 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.NULL[0] + self.pane_width <= self.tile_size*self.NxNy[0]:
            self.NULL[0] += speed
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.NULL[0] >= 2:
            self.NULL[0] -= speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.NULL[1] + self.pane_height <= self.tile_size*self.NxNy[1]:
            self.NULL[1] += speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.NULL[1] >= 2:
            self.NULL[1] -= speed
        self.NULL_tile_draw = [self.NULL[0]//self.tile_size, self.NULL[1]//self.tile_size]
        self.NULL_draw = [(-1)*(self.NULL[0]%self.tile_size) + self.pane[0][0], (-1)*(self.NULL[1]%self.tile_size) + self.pane[0][1]]

    def draw(self, frame):
        Img_Fill(self.img, [self.NULL_draw, self.pane[1]], self.screen)
        self.Building.draw(frame)


#Хранит информацию о каждой клетке: какие объекты, какие здания
class Farm():
    def __init__(self, worker, map):
        self.worker = worker
        self.tile_info = [[{'obj': None, 'img': [], 'id': None, 'rotate': None} for i in range(map.NxNy[0])] for j in range (map.NxNy[1]) ]   #[объект, изображение, алиас, поворот?]
        self.pane_type = 'buildings'
        self.map = map
        map.Building = self

    #Проверка на занятость
    def can_build(self, mouse_pos):
        obj = self.worker.item_state['item']
        obj_size = len(obj.tile)
        obj_j, obj_i = 0, 0
        pos = self.WhoIsOn(mouse_pos)
        pos_row = pos[0] - obj.pivot[0]
        pos_col = pos[1] - obj.pivot[1]
        for j in range(pos_row, pos_row+obj_size):
            for i in range(pos_col, pos_col+obj_size):
                if self.worker.item_state['item'].tile[obj_j][obj_i]:
                    if pos_row+obj_j >= self.map.NxNy[1] or pos_col+obj_i >= self.map.NxNy[0]:
                        return False
                    elif pos_row+obj_j < 0 or pos_col+obj_i < 0:
                        return False
                    elif self.tile_info[j][i]['obj'] is not None:
                        return False
                obj_i += 1
            obj_i = 0
            obj_j += 1
        return True

    def add (self, mouse_pos):
        obj = self.worker.item_state['item']
        obj_size = len(self.worker.item_state['item'].tile)
        pos = self.WhoIsOn(mouse_pos)
        pos_row = pos[0] - obj.pivot[0]
        pos_col = pos[1] - obj.pivot[1]

        #Записали в объект новый элемент, например 'r1c2r1c3r1c4': [bums, limit, lvl]
        item_id=''
        for j in range(pos_row, pos_row+obj_size):
            for i in range(pos_col, pos_col+obj_size):
                item_id += 'r' + str(j) + 'c' + str(i)
        obj.objects_dict[item_id] = {}
        obj.SetNewID(item_id)

        #Записали в массив новый объект
        for j in range(obj_size):
            for i in range(obj_size):
                if obj.tile[j][i]:
                    self.tile_info[pos_row+j][pos_col+i]['obj'] = obj
                    self.tile_info[pos_row+j][pos_col+i]['id'] = item_id
        self.tile_info[pos_row][pos_col]['img'].append(obj.img)
        self.tile_info[pos_row][pos_col]['img_obj_bind'] = obj
        self.tile_info[pos_row][pos_col]['img_obj_bind_id'] = item_id
        #self.tile_info[pos_row][pos_col]['rotate'] = [3,self.worker.item_rotate]
        self.tile_info[pos_row][pos_col]['rotate'] = self.worker.item_rotate
        self.worker.item_rotate = 0
        self.worker.item_state['item'].tile_to_default()

    def WhoIsOn(self, mouse_pos):
        for i in range(1,self.map.NxNy[0]+1):
            if mouse_pos[0] < self.map.GRID_coo[0][i][0] + self.map.NULL_draw[0]:
                pos_x = self.map.GRID_pos[0][i-1][0] + self.map.NULL_tile_draw[0]
                break
        for j in range(1,self.map.NxNy[1]+1):
            if mouse_pos[1] < self.map.GRID_coo[j][0][1] + self.map.NULL_draw[1]:
                pos_y = self.map.GRID_pos[j-1][0][1] + self.map.NULL_tile_draw[1]
                break
        return [pos_y, pos_x]

    def draw(self, frame):
        max_bldg_size = 2
        for j in range(self.map.NULL_tile_draw[1]-max_bldg_size, self.map.NULL_tile_draw[1]+self.map.tile_visible_NxNy[1]+1):
            for i in range(self.map.NULL_tile_draw[0]-max_bldg_size, self.map.NULL_tile_draw[0]+self.map.tile_visible_NxNy[0]+1):
                if (i < self.map.NxNy[0] and j < self.map.NxNy[1]) and self.tile_info[j][i]['img'] is not None:
                    pos_x = (i - self.map.NULL_tile_draw[0]) * self.map.tile_size + self.map.NULL_draw[0]
                    pos_y = (j - self.map.NULL_tile_draw[1]) * self.map.tile_size + self.map.NULL_draw[1]
                    for image in self.tile_info[j][i]['img']:
                        if 'img_obj_bind' in self.tile_info[j][i]:
                            obj_frame_start_row = self.tile_info[j][i]['img_obj_bind'].objects_dict[self.tile_info[j][i]['img_obj_bind_id']]['frame_start']
                            obj_lvl = self.tile_info[j][i]['img_obj_bind'].objects_dict[self.tile_info[j][i]['img_obj_bind_id']]['lvl']
                            obj_rotate = self.tile_info[j][i]['rotate']
                            image.draw(pos_x, pos_y, [12,8], [obj_frame_start_row + frame, obj_rotate + 4*(obj_lvl - 1)])
                        # BUG: Временно оставлено - для рисования камней
                        else:
                            image.draw(pos_x, pos_y, [4,4], [0, self.tile_info[j][i]['rotate']])

    def Activate(self, mouse_pos):
        pos = self.WhoIsOn(mouse_pos)
        obj = self.tile_info[pos[0]][pos[1]]['obj']
        if obj == 'Stone':
            pass
        elif obj is not None:
            self.worker.item_state['item'] = obj
            self.worker.item_state['item_id'] = self.tile_info[pos[0]][pos[1]]['id']
            self.worker.switch({'switch': ('MENU', 'menu:building')})
            if obj.objects_dict[self.worker.item_state['item_id']]['lvl'] < len(obj.lvl_list):
                return obj.button_dict
            else:
                return obj.button_dict_limited

#Для более удобной работы с изображениями. Кропаем, застилаем, пишем в объекты.
#Object_list должен содержать объекты, пренадлежащие одной группе
class Image():
    def __init__(self, image, object_list = [], folder = 'images', screen=None):

        if len(object_list) >= 1 and hasattr(object_list[0], 'pane_type'):
            if object_list[0].pane_type not in IMAGE_DICT:
                IMAGE_DICT[object_list[0].pane_type] = []
            IMAGE_DICT[object_list[0].pane_type].append(self)
        else:
            IMAGE_DICT['No pane_type'].append(self)
        self.screen = screen
        self.img = pygame.image.load(os.path.join(folder,image))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        for obj in object_list:
            obj.img = self

    def draw(self, pos_x, pos_y, Nxy = [1,1], elem = [0,0]):
        crop_width = self.width/Nxy[0]
        crop_height = self.height/Nxy[1]
        crop_pos_x = crop_width*elem[1]
        crop_pos_y = crop_height*elem[0]
        self.screen.blit(self.img, [pos_x, pos_y],(crop_pos_x,crop_pos_y,crop_width,crop_height))

    def draw_Button(self, pos_x, pos_y, state):
        if state == 'off':
            elem = [0,0]
        elif state == 'on':
            elem = [1,0]
        self.draw(pos_x, pos_y, [1,2], elem)

    def fill(self, area):
        Img_Fill(area, self.screen)


#Переключатели, работа с хешом интерфейса, указатели на объекты
class Actor ():
    def __init__(self):
        self.item_state = {
            'item': None,
            'item_id':None,
        }
        self.item_rotate = 0
        self.interface_state = {
            'map_mode': 'base',
            'constructing_mode': False,
            'continue_game': True
        }

    def text_info_screen(self, Txt_Obj):
        text_output = []
        item = self.item_state['item']
        info_screen = item.info_screen
        item_ID = item.objects_dict[self.item_state['item_id']]

        for i in range(len(info_screen)):
            text_output.append(
            info_screen[i]['display_name'] + str(item_ID[info_screen[i]['attr']])
            )
        Txt_Obj.draw(text_output)

    def switch(self, params):
        pane = params['switch'][0]
        switch_group = params['switch'][1]

        for button_area in self.PANE_INIT_DICT[pane]['buttons_area']:
            if button_area == switch_group:
                self.PANE_INIT_DICT[pane]['buttons_area'][button_area]['draw'] = True
            else:
                self.PANE_INIT_DICT[pane]['buttons_area'][button_area]['draw'] = False
        return

    def switch_constructing_mode(self, params = None):
        self.interface_state['constructing_mode'] = not self.interface_state['constructing_mode']

    def clear_buttons_areas(self, PANE_INIT_DICT, pane):
        for buttons_area_i in PANE_INIT_DICT[pane]['buttons_area']:
            PANE_INIT_DICT[pane]['buttons_area'][buttons_area_i]['draw'] = False
        for key in self.item_state:
            self.item_state[key] = None

    def clear_button_dict(self, PANE_INIT_DICT, pane):
        PANE_INIT_DICT[pane]['button_dict'] = []

    def end_game(self, params = None):
        self.interface_state['continue_game'] = False


#Для более удобной работы с текстом. В разработке
class Text():
    def __init__(self, font, input_list, screen, area = False):
        #либо указываем напрямую список позиций pos_list,
        #либо передаём список объектов и указываем их тип (для типов тут прописаны специфики расположения)
        #TEXT_LIST.append(self)
        self.font = font
        self.screen = screen
        self.is_area = area
        if self.is_area:
            self.area = input_list
        else:
            self.obj_list = input_list



    def draw(self, text_list, event = None, duration = None):
        text_list = [self.font.render(text, True, [0,0,0]) for text in text_list]
        self.pos_list = []

        if self.is_area:
            interline = 1.5
            area_w = self.area[1][0] - self.area[0][0]

            max_w = 0
            for text in text_list:
                w = text.get_width()
                if w > max_w:
                    max_w = w
            left_x = self.area[0][0] + (area_w/2 - max_w/2)

            area_h = self.area[1][1] - self.area[0][1]
            max_h = text_list[0].get_height()
            dy = max_h * (interline + 1)
            all_h = max_h + len(text_list) * dy
            top_y = self.area[0][1] + (area_h - all_h) / 2

            for i in range(len(text_list)):
                self.pos_list.append([
                left_x,
                top_y + i * dy
                ])

            #return self.pos_list
        else:
            obj_pos_list = [obj.pos() for obj in self.obj_list]
            obj_size_list = [obj.get_size() for obj in self.obj_list]

            for i in range(len(text_list)):
                self.pos_list.append([
                    obj_pos_list[i][0] + (obj_size_list[i][0]/2 - text_list[i].get_width()/2),
                    obj_pos_list[i][1] +(obj_size_list[i][1]/2 - text_list[i].get_height()/2)
                    ])



        for i in range(len(text_list)):
            self.screen.blit(text_list[i], self.pos_list[i])


#Рандомайзер препятствий на карте
class Obstacle():
    def __init__(self, img, screen):
        self.img = img
        Image(img, [self], screen = screen)


    def rand_stones (self, tile_info, N):
        for i in range(N):
            R_row = random.randrange(0, 19, 1)
            R_column = random.randrange(0, 19, 1)
            tile_info[R_row][R_column]['obj'] = 'Stone'
            tile_info[R_row][R_column]['img'] = [self.img]
            tile_info[R_row][R_column]['rotate'] = 0


#Записывает в кнопки окончательные координаты для рендеринга
def coordinates_to_button (buttons_area, pane_button_group):
    button_obj_list = buttons_area[pane_button_group]['button_obj_list']
    button_dict = buttons_area[pane_button_group]['button_dict']
    button_group_dict = buttons_area[pane_button_group]
    size = buttons_area[pane_button_group]['button_size']
    gap = [10,10]
    if 'button_row' in button_group_dict:
        Nrow_Ncol = [button_group_dict['button_row'], math.ceil(len(button_dict)/button_group_dict['button_row'])]
    elif 'button_col' in button_group_dict:
        Nrow_Ncol = [math.ceil(len(button_dict)/button_group_dict['button_col']), button_group_dict['button_col']]
    else:
        Nrow_Ncol = [1, len(button_dict)]

    grid_area = button_group_dict['area']

    def Grid(size, NxNy, gap, grid_area):
        total_x = size[0]*Nrow_Ncol[1] + gap[0]*(Nrow_Ncol[1]-1)
        total_y = size[1]*Nrow_Ncol[0] + gap[1]*(Nrow_Ncol[0]-1)
        pane_x =  grid_area[1][0] - grid_area[0][0]
        pane_y =  grid_area[1][1] - grid_area[0][1]
        start_x = grid_area[0][0] + (pane_x/2 - total_x/2)
        start_y = grid_area[0][1] + (pane_y/2 - total_y/2)

        #Матрица Nx на Ny по центру области win_size,
        #где элементы - [Y][X][x,y] левого верхнего угла распологаемого объекта для позиции X, Y в матрице
        Grid = [[[start_x + i*(size[0] + gap[0]),start_y + j*(size[1]+gap[1])] \
        for i in range(Nrow_Ncol[1])] for j in range(Nrow_Ncol[0])]

        pos_x = Grid[grid_y][grid_x][0]
        pos_y = Grid[grid_y][grid_x][1]
        return [pos_x, pos_y]

    #Записываем в кнопки их координаты
    grid_x, grid_y = 0, 0
    #    if group == 'menu:building':
    #        BUTTON_DICT['menu:building'] = []

    for button in button_obj_list:
        i = button_obj_list.index(button)
        if ((i+1)-(grid_y*Nrow_Ncol[1])) > Nrow_Ncol[1]:
            grid_x = 0
            grid_y += 1
        button.pos_x, button.pos_y = Grid(size, Nrow_Ncol, gap, grid_area)
        button.pane_type = pane_button_group
        button.width = size[0]
        button.height = size[1]

        grid_x += 1
    return

#Создание объектов Button() по хешу интерфейса
def create_buttons (buttons_area, pane_button_group, IMAGE_DICT):
    button_dict = buttons_area[pane_button_group]['button_dict']
    buttons_area[pane_button_group]['button_obj_list'] = []
    i = 0

    IMAGE_DICT[pane_button_group] = []

    for Butt in button_dict:
        # BUG: Пора бы упаковать параметры нормально
        buttons_area[pane_button_group]['button_obj_list'].append(Button(Butt['name'], Butt['action']))
        buttons_area[pane_button_group]['button_obj_list'][i].item = Butt['item']
        buttons_area[pane_button_group]['button_obj_list'][i].screen = buttons_area[pane_button_group]['screen']
        buttons_area[pane_button_group]['button_obj_list'][i].font = buttons_area[pane_button_group]['font']
        buttons_area[pane_button_group]['button_obj_list'][i].Worker = buttons_area[pane_button_group]['Worker']
        if 'rebuild' in buttons_area[pane_button_group]:
            buttons_area[pane_button_group]['button_obj_list'][i].params['rebuild'] = buttons_area[pane_button_group]['rebuild']
        if 'switch' in buttons_area[pane_button_group]:
            buttons_area[pane_button_group]['button_obj_list'][i].params['switch'] = buttons_area[pane_button_group]['switch']
        if 'button_image' not in buttons_area[pane_button_group]:
            Image(Butt['button_image'], [buttons_area[pane_button_group]['button_obj_list'][i]], screen = buttons_area[pane_button_group]['screen'])
        i += 1

    if 'button_image' in buttons_area[pane_button_group]:
        Image(buttons_area[pane_button_group]['button_image'], buttons_area[pane_button_group]['button_obj_list'], screen = buttons_area[pane_button_group]['screen'])

    coordinates_to_button(buttons_area, pane_button_group)

    #BUTTON_DICT[pane_button_group] = buttons_area[pane_button_group]['button_obj_list']
    #if 'static' not in buttons_area[pane_button_group] or buttons_area[pane_button_group]['static']:
    #    BUTTON_DRAW_GROUPS['static'].append(buttons_area[pane_button_group]['button_obj_list'])

    return buttons_area[pane_button_group]['button_obj_list']

#Вычисление координат для панелей или областей для кнопок по хешу интерфейса
def create_areas(PANE_INIT_DICT, input_est_screen):
    est_screen = [[None, None],[None, None]]
    est_screen[0] = [input_est_screen[0][0], input_est_screen[0][1]]
    est_screen[1] = [input_est_screen[1][0], input_est_screen[1][1]]

    #Если нужна область, занимающая опрелённый процент от доступного места
    def percentage(elem, input_est_screen):
        if elem['alignment'] == 'top' or elem['alignment'] == 'bottom':
            elem['height'] = (est_screen[1][1] - est_screen[0][1]) * elem['percent'] // 100
        if elem['alignment'] == 'left' or elem['alignment'] == 'right':
            elem['width'] = (est_screen[1][0] - est_screen[0][0]) // elem['percent']

    for n in range(len(PANE_INIT_DICT)):
        for elem in PANE_INIT_DICT:
            if PANE_INIT_DICT[elem]['order'] == n:
                created_area = [[None, None],[None, None]]
                created_area[0] = [est_screen[0][0], est_screen[0][1]]
                created_area[1] = [est_screen[1][0], est_screen[1][1]]

                if 'percent' in PANE_INIT_DICT[elem]:
                    percentage(PANE_INIT_DICT[elem], est_screen)

                if PANE_INIT_DICT[elem]['alignment'] == 'top':
                    created_area[1][1] = est_screen[0][1] + PANE_INIT_DICT[elem]['height']
                    PANE_INIT_DICT[elem]['area'] = created_area
                    if ('cut_est' not in PANE_INIT_DICT[elem]) or PANE_INIT_DICT[elem]['cut_est']:
                        est_screen[0][1] += PANE_INIT_DICT[elem]['height']

                elif PANE_INIT_DICT[elem]['alignment'] == 'bottom':
                    created_area[0][1] = est_screen[1][1] - PANE_INIT_DICT[elem]['height']
                    PANE_INIT_DICT[elem]['area'] = created_area
                    if ('cut_est' not in PANE_INIT_DICT[elem]) or PANE_INIT_DICT[elem]['cut_est']:
                        est_screen[1][1] -= PANE_INIT_DICT[elem]['height']

                elif PANE_INIT_DICT[elem]['alignment'] == 'left':
                    created_area[1][0] = est_screen[0][0] + PANE_INIT_DICT[elem]['width']
                    PANE_INIT_DICT[elem]['area'] = created_area
                    if ('cut_est' not in PANE_INIT_DICT[elem]) or PANE_INIT_DICT[elem]['cut_est']:
                        est_screen[0][0] += PANE_INIT_DICT[elem]['width']

                elif PANE_INIT_DICT[elem]['alignment'] == 'right':
                    created_area[0][0] = est_screen[1][0] - PANE_INIT_DICT[elem]['width']
                    PANE_INIT_DICT[elem]['area'] = created_area
                    if ('cut_est' not in PANE_INIT_DICT[elem]) or PANE_INIT_DICT[elem]['cut_est']:
                        est_screen[1][0] -= PANE_INIT_DICT[elem]['width']

                elif PANE_INIT_DICT[elem]['alignment'] == 'all':
                    created_area[0] = [est_screen[0][0], est_screen[0][1]]
                    created_area[1] = [est_screen[1][0], est_screen[1][1]]
                    PANE_INIT_DICT[elem]['area'] = created_area
                    if ('cut_est' not in PANE_INIT_DICT[elem]) or PANE_INIT_DICT[elem]['cut_est']:
                        est_screen = None

#Создание объектов Pane() по хешу интерфейса
def create_panes(PANE_INIT_DICT, PANE_DICT, IMAGE_DICT):
    for pane_name in PANE_INIT_DICT:
        PANE_DICT[PANE_INIT_DICT[pane_name]['pane_type']] = Pane(PANE_INIT_DICT, pane_name, PANE_INIT_DICT[pane_name]['pane_type'])
        PANE_INIT_DICT[pane_name]['pane_obj'] = PANE_DICT[PANE_INIT_DICT[pane_name]['pane_type']]
        PANE_INIT_DICT[pane_name]['pane_obj'].pane_type = PANE_INIT_DICT[pane_name]['pane_type']
        PANE_INIT_DICT[pane_name]['pane_obj'].screen = PANE_INIT_DICT[pane_name]['screen']
        if 'pane_image' in PANE_INIT_DICT[pane_name]:
            Image(PANE_INIT_DICT[pane_name]['pane_image'], [PANE_INIT_DICT[pane_name]['pane_obj']], screen = PANE_INIT_DICT[pane_name]['screen'])
        if PANE_INIT_DICT[pane_name]['buttons_area'] is not None:
            for button_group in PANE_INIT_DICT[pane_name]['buttons_area']:
                PANE_INIT_DICT[pane_name]['buttons_area'][button_group]['Worker'] = PANE_INIT_DICT[pane_name]['Worker']
                PANE_INIT_DICT[pane_name]['buttons_area'][button_group]['screen'] = PANE_INIT_DICT[pane_name]['screen']

                if PANE_INIT_DICT[pane_name]['buttons_area'][button_group]['button_dict'] is not None:
                    for button in PANE_INIT_DICT[pane_name]['buttons_area'][button_group]['button_dict']:
                        button['pane'] = PANE_INIT_DICT[pane_name]['pane_obj']
