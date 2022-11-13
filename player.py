from hand import *
from secul import Secul
from main import Trans

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
            self.trn.show('Новая карта нападения: ' + Secul.str_to_unicode(att_card))
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