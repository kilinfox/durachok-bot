from card import Card
class Secul:

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