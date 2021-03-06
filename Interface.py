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
        self.tile_info = [[{'obj': None, 'img_list': [], 'id': None, 'rotate': None} for i in range(map.NxNy[0])] for j in range (map.NxNy[1]) ]   #[объект, изображение, алиас, поворот?]
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

        self.tile_info[pos_row][pos_col]['img_list'].append({
            'img': obj.img,
            'rotate': self.worker.item_rotate,
            'img_obj_bind': obj,
            'img_obj_bind_id': item_id,
            'NxNy': obj.NxNy,
        })
        #self.tile_info[pos_row][pos_col]['img_obj_bind'] = obj
        #self.tile_info[pos_row][pos_col]['img_obj_bind_id'] = item_id
        #self.tile_info[pos_row][pos_col]['rotate'] = self.worker.item_rotate
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
                if (i < self.map.NxNy[0] and j < self.map.NxNy[1]) and len(self.tile_info[j][i]['img_list']):
                    pos_x = (i - self.map.NULL_tile_draw[0]) * self.map.tile_size + self.map.NULL_draw[0]
                    pos_y = (j - self.map.NULL_tile_draw[1]) * self.map.tile_size + self.map.NULL_draw[1]
                    for image in self.tile_info[j][i]['img_list']:
                        obj_draw_frame = image['img_obj_bind'].objects_dict[image['img_obj_bind_id']]['draw_frame']
                        draw_col = image['img_obj_bind'].objects_dict[image['img_obj_bind_id']]['draw_col']
                        obj_rotate = image['rotate']
                        image['img'].draw(pos_x, pos_y, image['NxNy'], [obj_draw_frame, obj_rotate + 4*draw_col])

    def Activate(self, mouse_pos):
        pos = self.WhoIsOn(mouse_pos)
        obj = self.tile_info[pos[0]][pos[1]]['obj']
        #if obj == 'Stone':
        #    pass
        if (obj is not None) and obj.__class__.__name__ != 'Obstacle':
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
            'continue_game': True,
        }

    '''
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
    '''

    def switch(self, params):
        pane = params['switch'][0]
        switch_group = params['switch'][1]

        if switch_group == 'menu:text:resources':
            self.user.text_dict['res_annotation']['text']['text'] = self.user.texts[params['res_annotation']]

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
#рендерит весь текст в заданной области по словарю {header:str, body:[name, atr] }

class Text():
    def __init__(self, font, input_list, screen, page = None, area = False, hyph = False, static = False, Worker = None):
        #Либо указываем area, которая заполнится текстом из Worker.item_state['item'].text_dict[self.page]
        #Либо указываем {'obj_list': [], 'text': []} - заливаем текст в центр area объекта
        self.Worker = Worker
        self.hyph = hyph
        self.font = font
        self.screen = screen
        self.page = page
        self.is_area = area
        self.static = static
        self.draw_text_list = []
        self.draw_pos_list = []

        if self.is_area:
            self.area = input_list
        else:
            self.obj_list = input_list['obj_list']
            self.text_dict = input_list['text']

    def hyphenation(self, text_list, border):
        tmp_list = text_list[0].split()
        area_w = self.area[1][0] - self.area[0][0] - border
        app_len = self.font.render('a', True, [0,0,0]).get_width() #костыль! Получаем примерную ширину одного символа
        row = 0
        is_first = True
        text_list = []

        text_list.append(tmp_list[0] + ' ')

        for word in tmp_list[1:]:
            if (len(text_list[row]) + len(word) + 1) * app_len < area_w:
                text_list[row] += str(word) + ' '
                continue

            else:
                text_list.append(word + ' ')
                row += 1

        return text_list

    def draw_new(self):
        text_list = []
        pos_list = []
        if self.is_area:
            text_dict = self.Worker.item_state['item'].text_dict[self.page]
            interline = 1
            border = 10
            area_w = self.area[1][0] - self.area[0][0]
            area_h = self.area[1][1] - self.area[0][1]
            max_w = 0

            item = self.Worker.item_state['item']
            #info_screen = item.info_screen
            item_id = self.Worker.item_state['item_id']

            if 'header' in text_dict:
                #text_list ++ pos llist++
                #изменить crop area, сделать одну новую
                pass

            for text_block in text_dict:
                tmp_text_list = []
                tmp_pos_list = []
                if text_block == 'header':
                    tmp_text_list.append(self.font.render(text_dict[text_block]['text'], True, [0,0,0]))

                    txt_H = tmp_text_list[0].get_height()
                    top_y = self.area[0][1] + border

                    tmp_pos_list.append([self.area[0][0] + (area_w/2 - tmp_text_list[0].get_width()/2), top_y])
                    text_list.extend(tmp_text_list)
                    pos_list.extend(tmp_pos_list)

                else:
                    tmp_text_list = []
                    tmp_pos_list = []

                    if 'text' in text_dict[text_block]:
                        if self.hyph:
                            new_hyph_list = self.hyphenation(text_dict[text_block]['text'], border)
                            for phrase in new_hyph_list:
                                tmp_text_list.append(self.font.render(phrase, True, [0,0,0]))
                        else:
                            for phrase in text_dict[text_block]['text']:
                                tmp_text_list.append(self.font.render(phrase, True, [0,0,0]))
                    elif 'attr' in text_dict[text_block]:
                        for attribute in text_dict[text_block]['attr']:
                            tmp_text_list.append((self.font.render(str(item.objects_dict[item_id][attribute]), True, [0,0,0])))

                    if text_dict[text_block]['alignment'] == 'left':
                        left_x = self.area[0][0]
                        txt_H = tmp_text_list[0].get_height()
                        dy = txt_H * (interline + 1)
                        all_txt_H = txt_H + len(tmp_text_list) * dy
                        top_y = self.area[0][1] + (area_h - all_txt_H) / 2

                        for i in range(len(tmp_text_list)):
                            tmp_pos_list.append([left_x + border, top_y + i * dy])

                    elif text_dict[text_block]['alignment'] == 'right':
                        txt_H = tmp_text_list[0].get_height()
                        dy = txt_H * (interline + 1)
                        all_txt_H = txt_H + len(tmp_text_list) * dy
                        top_y = self.area[0][1] + (area_h - all_txt_H) / 2

                        for i in range(len(tmp_text_list)):
                            tmp_pos_list.append([self.area[1][0] - tmp_text_list[i].get_width() - border, top_y + i * dy])

                    elif text_dict[text_block]['alignment'] == 'center':
                        txt_H = tmp_text_list[0].get_height()
                        dy = txt_H * (interline + 1)
                        all_txt_H = txt_H + len(tmp_text_list) * dy
                        top_y = self.area[0][1] + (area_h - all_txt_H) / 2

                        for i in range(len(tmp_text_list)):
                            tmp_pos_list.append([self.area[0][0] + (area_w/2 - tmp_text_list[i].get_width()/2), top_y + i * dy])

                    text_list.extend(tmp_text_list)
                    pos_list.extend(tmp_pos_list)

        else:
            obj_pos_list = [obj.pos() for obj in self.obj_list]
            obj_size_list = [obj.get_size() for obj in self.obj_list]
            tmp_text_list = []
            tmp_pos_list = []

            for i in range(len(self.text_dict['text_list'])):
                tmp_text_list.append(self.font.render(str(self.text_dict[self.text_dict['text_list'][i]]), True, [0,0,0]))


                tmp_pos_list.append([
                    obj_pos_list[i][0] + (obj_size_list[i][0]/2 - tmp_text_list[i].get_width()/2),
                    obj_pos_list[i][1] +(obj_size_list[i][1]/2 - tmp_text_list[i].get_height()/2)
                    ])

            text_list.extend(tmp_text_list)
            pos_list.extend(tmp_pos_list)

        return text_list, pos_list

    def draw (self):
        #Если текст статичный, то используем один раз заготовленные списки, а не делаем их заново
        if self.static:
            if len(self.draw_text_list):
                for i in range(len(self.draw_text_list)):
                    self.screen.blit(self.draw_text_list[i], self.draw_pos_list[i])
            else:
                self.draw_text_list, self.draw_pos_list = self.draw_new()
                self.draw()
                print ('ONE TIME')
        else:
            self.draw_text_list, self.draw_pos_list = self.draw_new()
            for i in range(len(self.draw_text_list)):
                self.screen.blit(self.draw_text_list[i], self.draw_pos_list[i])


class News_Line():
    def __init__(self, area, font, screen, Worker):
        self.news_dict = {
            'event1': ['Вы заработали много денег', 'Вы заработали ещё больше денег', 'Вы невероятно богаты'],
            'event2': ['У вас очень много бомжей', 'Вы обомжевали весь мир'],
            'event3': ['Народ охренел от вас', 'Все вами недовольны', 'Вы террорист вас ненавидят'],
        }
        #self.queue_text = []
        self.Worker = Worker
        self.text_in_drawing = None
        self.text_len = 0
        self.text_area_y_center = area[0][1] + (area[1][1] - area[0][1])/2
        self.area_x_right = area[1][0]
        self.area_x_left = area[0][0]
        self.font = font
        self.speed = 5
        self.screen = screen
        self.queue_event = []

    def queue_jobs(self):
        event = self.queue_event.pop(0)

        #if len(self.news_dict[event]):
        self.text_in_drawing = self.news_dict[event].pop(0)
        #else:
        #    return 'No texts'

        self.text_in_drawing = self.font.render(self.text_in_drawing, True, [0,0,0])
        self.pos_y = self.text_area_y_center - self.text_in_drawing.get_height()/2
        self.text_len = self.text_in_drawing.get_width()
        self.pos_x = self.area_x_right
        self.pos_x_end = self.area_x_left - self.text_len
        return

    def add_jobs(self, event):
        if self.queue_event.count(event) < len(self.news_dict[event]):
            self.queue_event.append(event)

    def get_event_and_draw(self):
        #берем новый, если тот кончился
        #if self.Worker.interface_state['news_event'] is not None and len(self.news_dict[self.Worker.interface_state['news_event']]):
        #    self.queue_event.append(self.Worker.interface_state['news_event'])
        #    self.Worker.interface_state['news_event'] = None

        if self.text_in_drawing is None:
            if not len(self.queue_event):
                return
            self.queue_jobs()
            #if self.queue_jobs() == 'No texts':
            #    return


        self.pos_x -= self.speed
        if self.pos_x > self.pos_x_end:
            self.screen.blit(self.text_in_drawing, [self.pos_x, self.pos_y])
        else:
            self.text_in_drawing = None
            #очищаем джобы





#евент в джобы - и на отпску


#Рандомайзер одноклеточных препятствий на карте
class Obstacle():
    def __init__(self, img, screen):
        self.img = img
        Image(img, [self], screen = screen)
        self.objects_dict = {}
        self.NxNy = [4,4]

    def rand_stones (self, tile_info, N):
        for i in range(N):
            R_row = random.randrange(0, 19, 1)
            R_column = random.randrange(0, 19, 1)

            item_id='r' + str(R_row) + 'c' + str(R_column)
            self.objects_dict[item_id] = {'draw_frame': random.randrange(0, self.NxNy[0], 1), 'draw_col': 0}
            tile_info[R_row][R_column]['obj'] = self
            tile_info[R_row][R_column]['img_list'].append({
                'img': self.img,
                'rotate': random.randrange(0, self.NxNy[1], 1),
                'img_obj_bind': self,
                'img_obj_bind_id': item_id,
                'NxNy': self.NxNy,
            })

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
        if 'params' in Butt:
            buttons_area[pane_button_group]['button_obj_list'][i].params.update(Butt['params'])

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
