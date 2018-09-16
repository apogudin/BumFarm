from MyFunctions import *

class BusStation():
    #Здание - остановка
    def __init__(self, user):
        self.user = user
        self.cost = 25

        self.bums_p_sec = 0,3
        self.lvl_limit = 3

        self.tile_to_default()
        self.objects_dict = {}
        self.img = None
        self.lvl_list = [
        {'lvl': 1, 'cost': 0, 'bums':0, 'limit': 10, 'bps': 0.3, 'cash': 0},
        {'lvl': 2, 'cost': 100, 'limit': 50, 'bps': 1},
        {'lvl': 3, 'cost': 1000, 'limit': 200, 'bps': 5},
        ]
        self.button_dict = [
            {
                'name': 'LEVEL',
                'action': self.lvl,
                'item': self,
            }]
        self.button_dict_limited = []

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

    def set(self, item_state):
        print(item_state)
        self.objects_dict[item_state['item_id']]['bums'] += 1

    def lvl(self, item_state):
        self.objects_dict[item_state['item_id']]['lvl'] += 1
        self.objects_dict[item_state['item_id']]['limit'] += 10

#Проходится по всем своим объектам, считает прибыль
    def resources_income(self):
        bums_income = 0


        self.user.resources['bums']['EUR'] += bums_income



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
    def resources_income(self):
        for country in self.property_list:
            for obj in self.property_list[country]:
                obj.resources_income()
