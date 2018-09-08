from MyFunctions import *
from Configs import *




class BusStation():
    #Здание - остановка
    def __init__(self, pane):
        self.cost = 25
        self.limit = 0
        self.level = 1
        self.Bums = 0
        self.amount = 0
        self.tile_to_default()
        self.objects_dict = {}
        self.img = None
        self.buttons_dict = {
            'pane': pane,
            'image': 'Button_Menu_Shop.png',
            'buttons': [
            {
                'name': 'BUY',
                'action': self.set,
                'item': self,
            },
            {
                'name': 'LEVEL',
                'action': self.lvl,
                'item': self,
            }
            ]
        }

    def tile_to_default(self):
        self.tile = [
        [1, 1, 1],
        [1, 1, 1],
        [0, 0, 0]
        ]
        self.pivot = [1,1]
    def set_default(self, item_id):
        self.objects_dict[item_id].update({'bums':0, 'limit': 10,'lvl': 1})


    def set(self, item_state):
        self.objects_dict[item_state['item_id']]['bums'] += 1

    def lvl(self, item_state):
        self.objects_dict[item_state['item_id']]['lvl'] += 1
        self.objects_dict[item_state['item_id']]['limit'] += 10

    def levelUp():
        self.levelUp += 1
        self.limit += 5
    def buy(self):
        self.amount += 1
        self.limit += 5
    def setBum(self):
        self.Bums += 1
    def rotate(self):
        pass
    def build():
        #Добавление в словарь нового объекта
        pass
    def delete():
        pass
    def upgrade():
        pass


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
