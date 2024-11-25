import random
from collections import defaultdict

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}-{self.suit}"

    def __repr__(self):
        return self.__str__()

class Deck:
    suits = [ "♥", "♦", "♣", "♠"]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
        

    def deal(self):
        return [self.cards.pop() for _ in range(10)]

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def remove_card(self, card):
        self.hand.remove(card)

    def __str__(self):
        return f"{self.name}: {self.hand}"

class RummyGame:
    def __init__(self, player_names, cards_per_player=10):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.cards_per_player = cards_per_player
        self.discard_pile = []
        self.current_player_index = 0

    def setup(self):
        for player in self.players:
            player.hand = self.deck.deal()
        self.discard_pile.append(self.deck.deal()[0])

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def current_player(self):
        return self.players[self.current_player_index]

    def draw_card(self, from_discard=False):
        if from_discard and self.discard_pile:
            return self.discard_pile.pop()
        elif self.deck.cards:
            return self.deck.cards.pop()
        else:
            self.reshuffle_discard()
            return self.deck.cards.pop() if self.deck.cards else None

    def reshuffle_discard(self):
        if not self.discard_pile:
            return
        top_card = self.discard_pile.pop()
        self.deck.cards.extend(self.discard_pile)
        self.discard_pile = [top_card]
        self.deck.shuffle()

    def discard(self, card):
        self.discard_pile.append(card)

    def check_meld(self, cards):
        if len(cards) < 3:
            return False
        
        # Check for set
        if all(card.rank == cards[0].rank for card in cards):
            return True
        
        # Check for run
        if all(card.suit == cards[0].suit for card in cards):
            rank_indices = [Deck.ranks.index(card.rank) for card in cards]
            rank_indices.sort()
            return all(rank_indices[i] == rank_indices[0] + i for i in range(len(rank_indices)))
        
        return False

    def play_turn(self):
        player = self.current_player()
        print(f"\n{player.name}'s turn")
        print(f"Hand: {player.hand}")
        print(f"Top of discard pile: {self.discard_pile[-1] if self.discard_pile else 'Empty'}")

        # Draw a card
        draw_from_discard = input("Draw from discard pile? (y/n): ").lower() == 'y'
        drawn_card = self.draw_card(draw_from_discard)
        if drawn_card:
            player.add_card(drawn_card)
            print(f"Drew: {drawn_card}")
        else:
            print("No cards available to draw.")
            return

        print(f"Updated hand: {player.hand}")

        # Check for melds
        melds = self.find_melds(player.hand)
        if melds:
            print("Possible melds:")
            for i, meld in enumerate(melds):
                print(f"{i + 1}: {meld}")
            meld_choice = input("Choose a meld to play (number) or press Enter to skip: ")
            if meld_choice.isdigit() and 0 < int(meld_choice) <= len(melds):
                chosen_meld = melds[int(meld_choice) - 1]
                for card in chosen_meld:
                    player.remove_card(card)
                print(f"Played meld: {chosen_meld}")

        # Discard a card
        while True:
            discard_input = input("Choose a card to discard (e.g., '7♤'): ")
            discard_card = next((card for card in player.hand if str(card) == discard_input), None)
            if discard_card:
                player.remove_card(discard_card)
                self.discard(discard_card)
                print(f"Discarded: {discard_card}")
                break
            else:
                print("Invalid card. Try again.")

        self.next_player()

    def find_melds(self, hand):
        melds = []
        # Check for sets
        rank_groups = defaultdict(list)
        for card in hand:
            rank_groups[card.rank].append(card)
        for group in rank_groups.values():
            if len(group) >= 3:
                melds.append(group)

        # Check for runs
        suit_groups = defaultdict(list)
        for card in hand:
            suit_groups[card.suit].append(card)
        for group in suit_groups.values():
            group.sort(key=lambda c: Deck.ranks.index(c.rank))
            for i in range(len(group) - 2):
                for j in range(i + 2, len(group)):
                    potential_run = group[i:j+1]
                    if self.check_meld(potential_run):
                        melds.append(potential_run)

        return melds

    def play_game(self):
        self.setup()
        while True:
            self.play_turn()
            if any(len(player.hand) == 0 for player in self.players):
                winner = next(player for player in self.players if len(player.hand) == 0)
                print(f"\nGame Over! {winner.name} wins!")
                break

# Start the game
player1_name=input("Enter your name: ")
player2_name=input("Enter your friend's name: ")
player_names = [player1_name, player2_name]
game = RummyGame(player_names)
game.play_game()