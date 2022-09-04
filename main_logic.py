import random
import telebot
from telebot import types
import json

class Information:
    def __init__(self):
        self.file_name = 'data.json'
        self.game_users = []

    def put(self, name, idd):
        with open(self.file_name, 'r') as file_rd:
            dct_ids = json.load(file_rd)
            if name not in dct_ids:
                dct_ids[name] = idd
                with open(self.file_name, 'w') as file_wr:
                    json.dump(dct_ids, file_wr)
            else:
                print('user is already registered!!!')

    def show(self, name):
        with open(self.file_name, 'r') as file:
            dct_ids = json.load(file)
            if name in dct_ids:
                return dct_ids[name]
            else:
                return False

    def app_user(self, name):
        self.game_users.append(name)

    def first_pl(self):
        return self.game_users[0]

    def second_pl(self):
        #returns false if only one user in users
        try:
            return self.game_users[1]
        except:
            return False

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

class Card:
    '''класс карт, имеет в атрибутах строчное представление, стоимость карты, отдельно выделенную
    для удобства масть '''
    def __init__(self, name, cost):
        assert isinstance(name, str) and isinstance(cost, int), 'TypeError'
        self.name = name
        self.cost = cost
        self.mast = name[-1]

    # строчное представление объекта для удобства работы с выводом колоды и руки
    def __str__(self):
        return self.name


class Coloda:
    '''класс колода, инициализирует колоду с учетом козыря и создает 36 объектов карт'''

    def helper(self, costs, defval, mast):
        for cost in costs:
            self._coloda.append(Card(cost + mast, defval))
            defval += 1

    def __init__(self):
        masts = ('h', 'd', 'c', 's')
        costs = ('6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
        self._coloda = []
        for mast in masts:
            default_value = 6
            self.helper(costs, default_value, mast)
        # перемешивает колоду
        random.shuffle(self._coloda)
        self.coz_card = self._coloda[0]
        self.coz = self.coz_card.mast
        for card in self._coloda:
            if card.mast == self.coz:
                card.cost += 9

    def _card_out(self):
        # удаляет верхнюю карту из колоды, возвращает эту карту
        return self._coloda.pop()

    def show_coloda(self):
        # возвращает строковое представление колоды, для удобства нахождения ошибок
        return f'Козырная карта: !{self.coz_card}! ' +  ', '.join([str(card) for card in self._coloda])

    def __len__(self):
        # возвращает длину колоды для удобства нахождения ошибок
        return len(self._coloda)

    def __str__(self):
        return str([str(card) + ' ' for card in self._coloda])

class Hand:
    '''класс руки, создает руку и при ините сразу добвляет в нее 6 карт, удаляя их при этом из указанной колоды'''
    def __init__(self, coloda):
        assert isinstance(coloda, Coloda), 'coloda is not Coloda'
        self.hand = []
        self.to_app(coloda,iters=6)

    # добавляет в руку карт из указанной колоды,
    # iters - аргумент по умолчанию равен одному, может иметь любое числовое значение
    # ничего не возвращает
    def to_app(self, coloda, iters=1):
        for i in range(0, iters):
            self.hand.append(coloda._card_out())

    def out(self, card):
        # удаляет из руки карты
        # ничего не возвращает
        assert card in self.hand
        del self.hand[self.hand.index(card)]

    def out_str(self, card):
        assert isinstance(card, str), 'not card requested to out_str'
        str_hand = [str(card) for card in self.hand]
        print(str_hand)
        if card in str_hand:
            return self.hand.pop(str_hand.index(card))

    def show_hand(self):
        # возвращает колоду, для удобства нахождения ошибок
        return ', '.join([str(card) for card in self.hand])

    def __len__(self):
        # возвращает длину колоды, для удобства нахождения ошибок
        return len(self.hand)

    def __str__(self):
        return str([str(card) for card in self.hand])


class Player:
    '''класс игрок, при ините создает(и пополняет) руку игрока и созраняет колоду'''
    def __init__(self, coloda, pl_id, othpl_id, bot):
        self.pl_hand = Hand(coloda)
        self.pl_coloda = coloda
        self.pl_id = pl_id
        self.othpl_id = othpl_id
        self.trn = Trans(bot)

    def show_coz(self):
        return 'Первая карта в колоде: ' + str(self.pl_coloda.coz_card)

    def pl_attack(self, stack):
        # консольный выбор атаки, возвращает выбранную карту и добавляет ее в стэк раунда
        self.trn.request('Атакуйте: ', self)
        att_card = self.trn.answer(self)
        self.pl_hand.out(att_card)
        stack.append(att_card)
        print('Attack ended!!!')
        return att_card

    def str_to_card(self, s_ca):
        str_cards = [str(card) for card in self.pl_hand.hand]
        assert s_ca in str_cards, 'ERROR in str_to_card card is not in hand!!!!'
        return self.pl_hand[str_cards.index(s_ca)]

    def pl_throw(self, stack):
        # консольный выбор подкидывания, берет в аргументы стек раунда, чтобы понять можно ли подкинуть эту карту
        # возвращает выбранную карту или false если ничего не подкинули
        print('Throw started!!!')
        self.trn.request('Подбрасывайте: ', self)
        thr_card = self.trn.answer(self)
        if thr_card == '':
            return False
        stack_costs = [card.cost for card in stack]
        may_be_cost = thr_card.cost + 9
        assert (thr_card.cost in stack_costs) or (may_be_cost in stack_costs), 'CardNotFoundError'
        stack.append(thr_card)
        self.pl_hand.out(thr_card)
        return thr_card


    def pl_get(self, stack):
        # реализует ситуацию, когда игрок берет карты, т.к. проиграл, в аргументах стек,
        # где копятся карты за весь раунд
        for card in stack:
            self.pl_hand.to_app(card)
            del stack[stack.index(card)]

    def pl_defend(self, att_card, stack):
        try:
            self.trn.show('Новая карта нападения: ' + self.trn.str_to_unicode(att_card))
            self.trn.request('Defend', self)
            df_card = self.trn.answer(self)
            #df_card - типа Card
            coz = self.pl_coloda.coz
            if df_card:
                df_card = self.str_to_card(df_card)
                self.pl_hand.out(df_card)
                if att_card.mast == coz:
                    if df_card.mast == coz:
                        result = df_card.cost > att_card.cost
                    else:
                        result = False
                else:
                    if df_card.mast == coz:
                        result = True
                    else:
                        result = df_card.cost > att_card.cost
                if result:
                    stack.append(df_card)
                    return True
                else:
                    raise ValueError
            else:
                return False
        except ValueError:
            #TODO: сделать функцию, которая стирает весь результат
            print('ERROR Вы поломали игру введя неправильную карту, это на твоей совести, сука, а мне лень писать код, обрабатывающий данную ошибку, понимаешь! ПОНИМАЕШЬ! так что перезапусти игру и играйте заново блять.')
        # реализует защиту на определенную карту, возвращает булевое значение: true - отбился, false - нет.

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
