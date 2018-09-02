import math
import random
#Проверка: достаточно ли денег
def YouBum(have, need):
    if have.amount >= need.cost:
        return
    else:
        print('>>>Ты бомжара, держи монетку')
        have.income(100)
        return

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

#Добавление объекта в словарь
def Append_To_Dict(dict, key, value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]

#Пробегаемся по всем объектам (поправить: только по определённой панели), вызываем у них IsOn
def CheckAll (pane_list, dict, mouse_pos):
    for pane in pane_list:
        if pane.pane_type in dict:
            for button in dict[pane.pane_type]:
                button.IsOn(mouse_pos)

#Пробегаемся по всем объектам (поправить: только по определённой панели) и активируем
def CheckAll_And_Action (pane_list, dict, mouse_pos):
    for pane in pane_list:
        if pane.pane_type in dict:
            for button in dict[pane.pane_type]:
                if button.IsOn(mouse_pos):
                    return button.Activate()

def rand_stones (object_list, img, N):
    for i in range(N):
        R_row = random.randrange(0, 19, 1)
        R_column = random.randrange(0, 19, 1)
        object_list[R_row][R_column]['obj'] = 'Stone'
        object_list[R_row][R_column]['img'] = [img]
        object_list[R_row][R_column]['rotate'] = [0, 0]

def rotate_build(matrix, right = False):
    if right:
        return[list(reversed(col)) for col in zip(*matrix)]
    else:
        return[list(col) for col in reversed(list(zip(*matrix)))]
