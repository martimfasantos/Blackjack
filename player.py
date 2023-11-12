from card import Card
from deck import Deck

class Player:
    def __init__(self, isDealer, deck):
        self.hands = [[]]
        self.isDealer = isDealer
        self.deck = deck
        self.scores = [0]

    def hit(self, hand_idx=0):
        hand = self.hands[hand_idx]
        hand.extend(self.deck.draw())
        self.check_score_hand(hand, hand_idx)
        if self.scores[hand_idx] > 21:
            return True
        else: 
            return False

    def deal(self):
        self.hands[0].extend(self.deck.draw(2)) 
        self.init_scores()
        if self.scores[0] == 21:
            return True
        return False
        
    def init_scores(self):
        self.scores = []
        for hand in range(len(self.hands)):
            score = 0
            for card in self.hands[hand]:
                # if the card is an Ace
                if isinstance(card.points(), list):
                    options = card.points() # [1, 11]

                    if score + options[1] > 21:
                        score += options[0]
                    else:
                        score += options[1]
                else:
                    score += card.points()
                
                # Only sum one card (the only card shown)
                if self.isDealer:
                    break
            
            self.scores.append(score)

    def can_split(self):
        # One hand and the 2 cards have equal value
        return len(self.hands) == 1 and \
            len(self.hands[0]) == 2 and \
            self.hands[0][0].equalValue(self.hands[0][1])

    def split(self):
        self.hands.append([self.hands[0][1]])
        self.hands[0].pop(1)
        self.init_scores()
        self.hit(hand_idx=0)
        self.hit(hand_idx=1)

    def check_score_hand(self, hand, hand_idx=0):
        score = 0
        nr_aces = 0
        for card in hand:
            # if the card is an Ace
            if isinstance(card.points(), list):
                nr_aces += 1
                # add largest value by default
                score += card.points()[1] 
            else:
                score += card.points()
        for _ in range(nr_aces):
            if score > 21:
                score -= 10 # ace_max_points - ace_min_points
        self.scores[hand_idx] = score

    def check_scores(self):
        for hand_idx, hand in enumerate(self.hands):
            self.check_score_hand(hand, hand_idx)
            
    def has_blackjack(self, hand_idx=0):
        return len(self.hands[hand_idx]) == 2 and self.scores[hand_idx] == 21

    def showCards(self, showAll):
        if self.isDealer:
            print("Dealer's Cards")  
        else:
            print("Player's Cards")
        
        for hand in range(len(self.hands)):
            rows = ['','','','','','','']
            for idx, card in enumerate(self.hands[hand]):
                rows[0] += '┌───────┐  '
                if not showAll and idx == 1:
                    rows[1] += '| ───── |  '
                    rows[2] += '| |   | |  '
                    rows[3] += '| |   | |  '
                    rows[4] += '| |   | |  '
                    rows[5] += '| ───── |  '

                else:
                    rows[1] += f'| {card.number:<2}    |  '
                    rows[2] += f'|       |  '
                    rows[3] += f'|   {card.suit}   |  '
                    rows[4] += f'|       |  '
                    rows[5] += f'|    {card.number:>2} |  '

                rows[6] += '└───────┘  '

            # Show the hands
            for row in rows:
                print(row)

            print(f"Score: {self.scores[hand]}\n")