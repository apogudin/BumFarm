from MyFunctions import *
from Configs import *

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

class BusStation():
    #Ларёк
    def __init__(self):
        self.cost = 25
        self.limit = 0
        self.level = 1
        self.Bums = 0
        self.amount = 0
        self.tile = [
        [1, 1, 1],
        [1, 1, 1]
        ]
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
