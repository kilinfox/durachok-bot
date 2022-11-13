from card import Card
import random
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