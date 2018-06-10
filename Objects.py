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
    def levelUp():
        self.levelUp += 1
        self.limit += 5
    def buy(self):
        self.amount += 1
        self.limit += 5
    def setBum(self):
        self.Bums += 1


'''            if Button_Quit.IsOn(mouse_pos):
                done = True
            if menu_type == 2:
                if Button_Buy_Station.IsOn(mouse_pos):
                    Station.buy()
                    Budget.outgo(Station.cost)
            if menu_type == 1:
                if Button_Bum_Station.IsOn(mouse_pos):
                    if Station.amount > 0 and Station.limit > Station.Bums and Bums.amount > 0:
                        Station.setBum()
                        Bums.set()
                    elif Station.limit == Station.Bums and Station.amount != 0:
                        alert = Temporary_Text('Все остановки заняты бомжами', Alert_Event, 5000)
                    elif Bums.amount <= 0:
                        alert = Temporary_Text('Закончились бомжи', Alert_Event, 5000)
                    elif Station.amount == 0:
                        alert = Temporary_Text('Остановок нет', Alert_Event, 5000)'''
