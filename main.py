import random


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    SUITS = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
    RANKS = {
        "A": 11, "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 10, "Q": 10, "K": 10
    }

    def __init__(self):
        self.cards = [Card(suit, rank, value) for suit in self.SUITS for rank, value in self.RANKS.items()]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number=1):
        return [self.cards.pop() for _ in range(number)] if self.cards else []


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.dealer = dealer

    def add_card(self, cards):
        self.cards.extend(cards)

    def calculate_value(self):
        value = sum(card.value for card in self.cards)
        # Adjust for Aces if value exceeds 21
        if any(card.rank == 'A' for card in self.cards) and value > 21:
            value -= 10
        return value

    def is_blackjack(self):
        return self.calculate_value() == 21

    def display(self, show_all_dealer_cards=False):
        hand_description = "Dealer's hand: " if self.dealer else "Your hand: "
        print(hand_description)
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards:
                print("Hidden")
            else:
                print(card)
        if not self.dealer:
            print("Value:", self.calculate_value())
        print()


class Game:
    def __init__(self):
        self.game_number = 0
        self.games_to_play = self.get_number_of_games()

    def get_number_of_games(self):
        while True:
            try:
                games_to_play = int(input("How many games do you want to play? "))
                if games_to_play > 0:
                    return games_to_play
            except ValueError:
                print("Please enter a valid number.")

    def play(self):
        while self.game_number < self.games_to_play:
            self.game_number += 1
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            player_hand.add_card(deck.deal(2))
            dealer_hand.add_card(deck.deal(2))

            self.show_game_status(player_hand, dealer_hand)

            if self.check_winner(player_hand, dealer_hand):
                continue

            while player_hand.calculate_value() < 21:
                choice = input("Please choose 'Hit' or 'Stand' (H/S): ").lower()
                if choice in ['h', 'hit']:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
                    if self.check_winner(player_hand, dealer_hand):
                        break
                elif choice in ['s', 'stand']:
                    break

            if not self.check_winner(player_hand, dealer_hand):
                self.dealer_turn(dealer_hand, deck)
                self.check_winner(player_hand, dealer_hand, game_over=True)

        print("\nThanks for playing!")

    def show_game_status(self, player_hand, dealer_hand):
        print(f"\n{'*' * 30}\nGame {self.game_number} of {self.games_to_play}\n{'*' * 30}")
        player_hand.display()
        dealer_hand.display()

    def dealer_turn(self, dealer_hand, deck):
        while dealer_hand.calculate_value() < 17:
            dealer_hand.add_card(deck.deal(1))
        dealer_hand.display(show_all_dealer_cards=True)

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        player_value = player_hand.calculate_value()
        dealer_value = dealer_hand.calculate_value()

        if not game_over:
            if player_value > 21:
                print("You busted. Dealer wins!")
                return True
            elif dealer_value > 21:
                print("Dealer busted. You win!")
                return True
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print("Both players have blackjack! It's a tie!")
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack! You win!")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack! Dealer wins!")
                return True
        else:
            if player_value > dealer_value:
                print("You win!")
            elif player_value < dealer_value:
                print("Dealer wins.")
            else:
                print("It's a tie!")
            return True
        return False


if __name__ == "__main__":
    Game().play()