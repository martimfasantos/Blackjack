class Card:
    def __init__(self, value, suit):
        self.value = value
        self.number = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'][value-1]
        self.suit = '♥♦♣♠'[suit]


    def show(self):
        print('┌───────┐')
        print(f'| {self.number:<2}    |')
        print('|       |')
        print(f'|   {self.suit}   |')
        print('|       |')
        print(f'|    {self.number:>2} |')
        print('└───────┘') 

    def facedown(self):
        print('┌───────┐')
        print('| ───── |')
        print('| |   | |')
        print('| |   | |')
        print('| |   | |')
        print('| ───── |')
        print('└───────┘') 

    def points(self):
        if self.value >= 10:
            return 10
        elif self.value == 1:
            return [1,11]
        return self.value
    
    def equalValue(self, other):
        if isinstance(other, Card):
            if self.value == other.value:
                return True
        return False
