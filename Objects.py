from MyFunctions import *

#Майнер бомжей
class BusStation():
    def __init__(self, user):
        self.user = user
        self.cost = 25

        self.bums_p_sec = 0,3
        self.lvl_limit = 3
        self.tile_to_default()
        self.objects_dict = {}
        self.img = None
        self.lvl_list = [
        {'lvl': 1, 'cost': 0, 'bums':0, 'limit': 10, 'bps': 0.3, 'bum_cash': 0, 'frame_start': 2},
        {'lvl': 2, 'cost': 100, 'limit': 50, 'bps': 1},
        {'lvl': 3, 'cost': 1000, 'limit': 200, 'bps': 5},
        ]
        self.button_dict = [
            {
                'name': 'LEVEL',
                'action': self.lvl,
                'item': self,
            },
            {
                'name': 'GRAB',
                'action': self.GrabBums,
                'item': self,
            },
            ]
        self.button_dict_limited = [
            {
                'name': 'GRAB',
                'action': self.GrabBums,
                'item': self,
            },
            ]

    def tile_to_default(self):
        self.tile = [
        [1, 1, 1],
        [1, 1, 1],
        [0, 0, 0]
        ]
        self.pivot = [1,1]

    def SetNewID(self, item_id):
        self.objects_dict[item_id].update(self.lvl_list[0])

        if self not in self.user.property_list['EUR']:
            self.user.property_list['EUR'].append(self)

    def GrabBums(self, item_state):
        item_id = item_state['item_id']
        self.user.resources['bums']['EUR'] += self.objects_dict[item_id]['bums']
        self.objects_dict[item_id]['bums'] = 0

    def lvl(self, item_state):
        new_lvl = self.objects_dict[item_state['item_id']]['lvl']
        self.objects_dict[item_state['item_id']].update(self.lvl_list[new_lvl])

#Проходится по всем своим объектам, считает прибыль
    def resources_update(self):
        for ID in self.objects_dict:
            if self.objects_dict[ID]['bums'] < self.objects_dict[ID]['limit']:
                self.objects_dict[ID]['bum_cash'] += self.objects_dict[ID]['bps']
                self.objects_dict[ID]['bums'] += int((self.objects_dict[ID]['bum_cash'] // 1))
                self.objects_dict[ID]['bum_cash'] = self.objects_dict[ID]['bum_cash'] % 1
            if self.objects_dict[ID]['bums'] / self.objects_dict[ID]['limit'] < 0.2:
                self.objects_dict[ID]['frame_start'] = 3
            else:
                self.objects_dict[ID]['frame_start'] = 5



class Bum():
    #Все существующие бомжи#
    def __init__(self):
        self.cost = 10          #Цена одного бомжа
        self.amount = 0         #Количество свободных бомжей
        self.efficiency = 1     #Эффективность бомжей
        self.trash = 0          #Счётчик отработанных бомжей
    def buy(self):
        self.amount += 1
    def set(self):
        self.amount -= 1

class Coins():
    #Деньги игрока
    def __init__(self):
        self.amount = 20
    def income(self, sum):      #Прибыль
        self.amount += sum
    def outgo(self, sum):       #Расход
        self.amount -= sum

#Игровой процесс пользователя
class User():
    def __init__(self):
        self.resources = {
        'coins': 0,
        'reputation': 0,
        'bums': {
            'EUR': 0,
        },
        }
        self.property_list = {
            'EUR': [],
        }

#Просит все свои объекты посчитать поступления
    def resources_update(self):
        for country in self.property_list:
            for obj in self.property_list[country]:
                obj.resources_update()
