from loadinganimation import loadingAnimation
from deck import Deck
from player import Player
import messages

class Blackjack:
    def __init__(self):
        # Entities
        self.deck = Deck()
        self.deck.generate()
        self.player = Player(False, self.deck)
        self.dealer = Player(True, self.deck)
        
        # Flags
        self.force_stand = [False]
        self.player_busted = [False]
        self.single_hand = True
        self.curr_hand = 0
    

    def get_command(self):

        if self.force_stand == [True for _ in range(len(self.force_stand))]:
            return 'fs'
        
        try:
            if (self.player.can_split()):
                command = input("Stand or Hit or Split? (s/h/S): ")
            else:
                if self.single_hand:
                    command = input("Stand or Hit? (s/h): ")
                else:
                    command = input(f"Stand or Hit on HAND {self.curr_hand+1}? (s/h): ")

            while (command != 's' and command != 'h' and command != 'S'):
                if (self.player.can_split()):
                    command = input("Invalid input. Press 's' or 'h' or 'S': ")
                else:
                    command = input("Invalid input. Press 's' or 'h': ")
            
            return command 
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            exit()
    
    # HIT
    def hit(self):
        
        if self.single_hand:
            loadingAnimation("Player chose to Hit...", 0.1)
        else:
            loadingAnimation(f"Player chose to Hit on HAND {self.curr_hand+1}...", 0.1)

        # Hit on the current hand
        self.player_busted[self.curr_hand] = self.player.hit(self.curr_hand)

        self.dealer.showCards(False)
        self.player.showCards(True)

        # if single hand and bust
        if self.single_hand:
            if self.player_busted[self.curr_hand]:
                print(messages.BUSTED)
                return False # stop playing
            elif self.player.scores[0] == 21:
                print(messages.GOT_21)
                self.force_stand = [True]

        # for double hand
        else:
            if self.player_busted[self.curr_hand]:
                print(messages.HAND_BUSTED.format(self.curr_hand+1))
                self.force_stand[self.curr_hand] = True
                # if both hands busted
                if self.player_busted == [True for _ in range(len(self.force_stand))]:
                    return False # stop playing
            
            elif self.player.scores[self.curr_hand] == 21:
                print(messages.GOT_21_ON_HAND.format(self.curr_hand+1))
                self.force_stand[self.curr_hand] = True

            # maximum 2 hands (0 and 1); switch to next if playable
            self.curr_hand = (self.curr_hand + 1)%2 if not self.force_stand[(self.curr_hand + 1)%2] else self.curr_hand
            
        return True # keep playing

    def stand(self, command):
        if command == 's' and self.single_hand:
            loadingAnimation("Player chose to Stand...", 0.3)
        elif command == 's' and not self.single_hand:
            loadingAnimation(f"Player chose to Stand on Hand {self.curr_hand+1}...", 0.3)
            self.force_stand[self.curr_hand] = True
            # if there is still a playable hand
            if not self.force_stand[(self.curr_hand + 1)%2]:
                self.curr_hand = (self.curr_hand + 1)%2
                return True # keep playing
        
        # Add the faced down card
        self.dealer.check_scores()
        
        loadingAnimation("Revealing dealer's cards...", 0.3)

        self.dealer.showCards(True)
        self.player.showCards(True)

        dealer_score = self.dealer.scores[0]
        dealer_bust = False if dealer_score <= 21 else True

        # Dealer keeps hitting until >= 17
        while dealer_score < 17:
            loadingAnimation("Dealer is playing...", 0.1)
            dealer_bust = self.dealer.hit()
            dealer_score = self.dealer.scores[0]
            self.dealer.showCards(True)
            self.player.showCards(True)

        # Check if dealer busted (and player didn't bust on all hands)
        if dealer_bust and self.player_busted != [True for _ in range(len(self.player_busted))]:
            print(messages.DEALER_BUSTED)
            if self.single_hand:
                # player has blackjack
                if self.player.has_blackjack():
                    print(messages.BLACKJACK_WIN)
                # player won (no blackjack)
                else:
                    print(messages.WIN)
            
            else:
                for hand_idx in range(len(self.player.hands)):
                    # player busted on this hand
                    if self.player_busted[hand_idx]:
                        print(messages.HAND_BUSTED.format(hand_idx+1))
                        
                    # player has blackjack on this hand
                    elif self.player.has_blackjack(hand_idx):
                        print(messages.BLACKJACK_ON_HAND.format(hand_idx+1))
                    
                    # player won on this hand (no blackjack)
                    else:
                        print(messages.WIN_ON_HAND.format(hand_idx+1))
            return False
        
        # if dealer didn't bust and has blackjack
        if self.dealer.has_blackjack():
            print(messages.BLACKJACK_DEALER)
        
        # Dealer didn't bust (neither did the player in all hands)
        # Single hand
        if self.single_hand:
            # player won 
            if dealer_score < self.player.scores[0]:
                print(messages.WIN)
                
            # player lost
            elif dealer_score > self.player.scores[0]:
                print(messages.LOSS)
                
            # player draw
            else: # if self.dealer.score == self.player.score
                print(messages.DRAW)
            return False
        
        # Double hand
        else:
            for hand_idx in range(len(self.player.hands)):
                # player busted on this hand
                if self.player_busted[hand_idx]:
                    print(messages.HAND_BUSTED.format(hand_idx+1))
                        
                # player won on this hand
                elif dealer_score < self.player.scores[hand_idx]:
                    # player has blackjack on this hand
                    if self.player.has_blackjack(hand_idx):
                        print(messages.BLACKJACK_WIN_ON_HAND.format(hand_idx+1))
                    # player won on this hand (no blackjack)
                    else:
                        print(messages.WIN_ON_HAND.format(hand_idx+1))
                        
                # player lost on this hand
                elif dealer_score > self.player.scores[hand_idx]:
                    print(messages.LOSS_ON_HAND.format(hand_idx+1))
                    
                # draw on this hand
                else: # if dealer_score == self.player.score[hand_idx]
                    print(messages.DRAW_ON_HAND.format(hand_idx+1))
        
        return False


    def split(self):
        loadingAnimation("Player chose to Split... Splitting...", 0.2)

        self.player.split()

        self.can_split = False
        self.force_stand = [False, False]
        self.player_busted = [False, False]
        self.single_hand = False
        self.curr_hand = 0

        self.dealer.showCards(False)
        self.player.showCards(True)
        
        # if player got blackjack after split, force stand on that hand
        for hand_idx in range(len(self.player.hands)):
            if self.player.has_blackjack(hand_idx):
                print(messages.BLACKJACK_ON_HAND.format(hand_idx+1))
                self.force_stand[hand_idx] = True
                # switch to next hand
                self.curr_hand = (hand_idx + 1)%2
        
        # if player got blackjack on all hands after splitting, game ends and check if dealer has blackjack
        if all(self.player.has_blackjack(hand_idx) == True for hand_idx in range(len(self.player.hands))):
            self.dealer.showCards(True)
            self.player.showCards(True)
            # if dealer has blackjack too
            if self.dealer.has_blackjack():
                print(messages.BLACKJACK_DEALER)
                print(messages.DRAW_ON_BOTH_HANDS)
            else:
                print(messages.BLACKJACK_WIN_ON_BOTH_HANDS)
            return  


    def play(self):
        # one dealer
        dealer_blackjack = self.dealer.deal()
        # one player but can have multiple hands (if Split)
        player_blackjack = self.player.deal()

        self.dealer.showCards(False)
        self.player.showCards(True)

        if player_blackjack:
            self.dealer.showCards(True)
            self.player.showCards(True)
            if dealer_blackjack:
                print(messages.DRAW)
            else:
                print(messages.BLACKJACK_WIN)
            return    
                        
        next_turn = True # keep playing
        while next_turn:
            command = self.get_command()
            
            if command == 's' or command == 'fs':
                next_turn = self.stand(command)
            elif command == 'h': 
                next_turn = self.hit()
            elif command == 'S' and self.player.can_split():
                self.split()
            else:
                print("Invalid input. Press 's' or 'h' or 'S': ")


def main():
    b = Blackjack()
    b.play()

if __name__ == "__main__":
    main()