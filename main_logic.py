import random
import telebot
from telebot import types
import json
from player import *
from inf import Information

#классы TRans и Game

class Trans:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def str_to_unicode(card):
        try:
            u_masts = list('♣♠♥♦')
            masts = list('cshd')
            dct = dict(zip(masts, u_masts))
            return card[0:-1] + dct[card[-1]]
        except:
            print(f'ERROR in str_to_unicode with card {card}!!!')

    @staticmethod
    def card_to_str(card):
        return [card.name, card.cost, card.mast]

    @staticmethod
    def str_to_card_trn(s):
        return Card(s[0], s[1])

    def request(self, text, player):
        #возвращает выбранную пользователем карту
        #pl - объект класса Player
        markup = types.InlineKeyboardMarkup(row_width=1)
        if player.pl_hand.hand:
            buttons = [types.InlineKeyboardButton(self.str_to_unicode(str(x)), callback_data= x.name + ' ' + str(x.cost)) for x in player.pl_hand.hand]
            empty = types.InlineKeyboardButton('Ничего', callback_data="empty")
            for but in buttons:
                markup.add(but)
            markup.add(empty)
            self.bot.send_message(player.pl_id, text, reply_markup=markup)

    def answer(self, player):
        while True:
            with open('ans.json', 'r') as f:
                try:
                    data = json.load(f)
                    if data != '':
                        print(data)
                    if data == "empty":
                        return ""
                    elif data != 'empty' and data != '':
                        return self.str_to_card_trn([data[0:-1], data[-1]])
                except:
                    continue
                finally:
                    with open('ans.json', 'w') as f:
                        json.dump("", f)

    def show(self, text, player):
        self.bot.send_message(player.pl_id, text)

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
