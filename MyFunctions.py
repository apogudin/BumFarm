import math

def YouBum(have, need):
    #Проверка: достаточно ли денег
    if have.amount >= need.cost:
        return
    else:
        print('>>>Ты бомжара, держи монетку')
        have.income(100)
        return

def Text_Resourses (text, amount, txt_x, font, screen, interval, position):
    #Выводит текст в зоне ресурсов
    txt_y = position * interval
    text = font.render(text, True, [0, 0, 0])
    amt = font.render(str(amount), True, [0, 0, 0])
    screen.blit(text, [txt_x, txt_y])
    screen.blit(amt, [txt_x+150, txt_y])

def Text_Alert (message, font_size, screen_y, font, screen):
    #Выводит текст в зоне алертов
    txt_x = 10
    txt_y = screen_y - font_size
    text = font.render(message, True, [0, 0, 0])
    screen.blit(text, [txt_x, txt_y])

def Temporary_Text (text, event, duration):
    #Временный текст, возвращает текст и заводит таймер
    pygame.time.set_timer(event, duration)
    return text

def Img_Fill(bg, area, screen):
    #Замостить изображением прямоугольник по двум точкам: лево-верх и право-низ
    left_up = area[0]
    right_down = area[1]
    bg_width = bg.get_width()
    bg_height = bg.get_height()
    total_x = right_down[0] - left_up[0]
    total_y = right_down[1]-left_up[1]
    Nx = math.ceil(total_x/bg_width)
    Ny = math.ceil(total_y/bg_height)
    X_null, Y_null = left_up[0], left_up[1]

    for i in range(Ny):
        crop_x, crop_y = bg_width, bg_height
        Yi = Y_null + bg_height*i
        if total_y - bg_height*i < bg_height:
            crop_y = total_y - bg_height*i

        for j in range(Nx):
            Xi = X_null + bg_width*j
            if total_x - bg_width*j < bg_height:
                crop_x = total_x - bg_width*j

            screen.blit(bg, [Xi, Yi],(0,0,crop_x,crop_y))

def Append_To_Dict(dict, key, value):
    if key in dict:
        dict[key].append(value)
    else:
        dict[key] = [value]




def CheckAll (group_list, dict, mouse_pos):
    for group in group_list:
        if group in dict:
            for button in dict[group]:
                button.IsOn(mouse_pos)
def CheckAll_And_Action (group_list, dict, mouse_pos):
    for group in group_list:
        if group in dict:
            for button in dict[group]:
                if button.IsOn(mouse_pos):
                    button.Action()
                    break

'''
def CheckAll (mass, mouse_pos):
    for button in mass:
        button.IsOn(mouse_pos)
def CheckAll_And_Action(mass, mouse_pos):
    for button in mass:
        if button.IsOn(mouse_pos):
            button.Action()
            break
'''
