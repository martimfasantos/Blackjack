import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []

    def generate(self):
        for i in range(1,14):
            for j in range(4):
                self.cards.append(Card(i, j))

    def draw(self, number = 1):
        cards = []
        for _ in range(number):
            # if number == 2:
            #     card = self.cards[0]
            # else:
            card = random.choice(self.cards)
            cards.append(card)
            self.cards.remove(card)
        return cards 