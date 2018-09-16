import math
import random

#Выводит текст в зоне ресурсов
def Text_Resourses (text, amount, txt_x, font, screen, interval, position):
    txt_y = position * interval
    text = font.render(text, True, [0, 0, 0])
    amt = font.render(str(amount), True, [0, 0, 0])
    screen.blit(text, [txt_x, txt_y])
    screen.blit(amt, [txt_x+150, txt_y])

#Выводит текст в зоне алертов
def Text_Alert (message, font_size, screen_y, font, screen):
    txt_x = 10
    txt_y = screen_y - font_size
    text = font.render(message, True, [0, 0, 0])
    screen.blit(text, [txt_x, txt_y])

#Временный текст, возвращает текст и заводит таймер
def Temporary_Text (text, event, duration):
    pygame.time.set_timer(event, duration)
    return text

#Замостить изображением прямоугольник по двум точкам: лево-верх и право-низ
def Img_Fill(Image, area, screen):
    img = Image.img
    width = Image.width
    height = Image.height
    total_x = area[1][0] - area[0][0]
    total_y = area[1][1]-area[0][1]
    Nx = math.ceil(total_x/width)
    Ny = math.ceil(total_y/height)
    X_null, Y_null = area[0][0], area[0][1]
    for i in range(Ny):
        crop_x, crop_y = width, height
        Yi = Y_null + height*i
        if total_y - height*i < height:
            crop_y = total_y - height*i
        for j in range(Nx):
            Xi = X_null + width*j
            if total_x - width*j < height:
                crop_x = total_x - width*j
            screen.blit(img, [Xi, Yi],(0,0,crop_x,crop_y))

#Пробегаемся по всем объектам (поправить: только по определённой панели), вызываем у них IsOn
def Check_All (PANE_INIT_DICT, mouse_pos, activate = False):
    for pane in PANE_INIT_DICT:
        if PANE_INIT_DICT[pane]['buttons_area'] is not None:
            for button_area in PANE_INIT_DICT[pane]['buttons_area']:
                if PANE_INIT_DICT[pane]['buttons_area'][button_area]['draw']:
                    for button in  PANE_INIT_DICT[pane]['buttons_area'][button_area]['button_obj_list']:
                        if activate:
                            if button.IsOn(mouse_pos):
                                button.Activate()
                        else:
                            button.IsOn(mouse_pos)

#Поворот здания: поворачивает матрицу тайлов по/против часовой стрелки. 
def rotate_build(matrix, right = False):
    if right:
        return[list(reversed(col)) for col in zip(*matrix)]
    else:
        return[list(col) for col in reversed(list(zip(*matrix)))]
