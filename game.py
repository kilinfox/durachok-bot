from coloda import Coloda
from player import *

class Game:
    def __init__(self, id_1, id_2, bot):
        self.main_coloda = Coloda()
        self.players = [Player(self.main_coloda, id_1, id_2, bot), Player(self.main_coloda, id_2, id_1, bot)]
        self.bot = bot

    def swap_places(self):
        self.players[0], self.players[1] = self.players[1], self.players[0]

    def check_num_of_cards(self):
        for player in self.players:
            if len(player.pl_hand) < 6:
                for i in range(6 - len(player.pl_hand)):
                    if len(self.main_coloda):
                        player.pl_hand.to_app(self.main_coloda)
            if len(player.pl_hand) == 0 and len(self.main_coloda) == 0:
                for player_won in self.players:
                    try:
                        if player == player_won:
                            player.trn.show('Вы выиграли!!!', player.pl_id)
                        else:
                            player.trn.show('Ваш соперник выиграл!!! ', player.pl_id)
                    finally:
                        return False


    def main_loop(self):
        while True:
            if self.check_num_of_cards() == False and self.check_num_of_cards() != None :
                print('the end')
                break
            else:
                cool_stack = []
                if self.attack_func(cool_stack):
                    self.swap_places()
                    print('bito')
                    print('chahge attacking')
                else:
                    print('attacking players won!')
                    self.players[1].pl_get(cool_stack)

    def throw_recurtion(self, stack):
        result = self.players[1].pl_defend(self.players[0].pl_throw(stack), stack)
        if result:
            self.throw_recurtion(stack)
        else:
            return False

    def attack_func(self, stack):
        # результат защиты второго игрока из кортежа на атаку первого
        result = self.players[1].pl_defend(self.players[0].pl_attack(stack), stack)
        if result:
            res_of_throw = self.throw_recurtion(stack)
            if res_of_throw:
                self.throw_recurtion(stack)
            else:
                return True
        else:
            self.players[1].pl_get(stack)
            return False