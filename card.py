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