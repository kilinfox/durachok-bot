from coloda import *
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