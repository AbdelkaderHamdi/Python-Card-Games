import random
import itertools


def create_deck(): 
    # create all cards and shuffle them
    suits = [ "♥", "♦", "♣", "♠"]
    values= range(1,11)
    deck=[f"{value}-{suit}" for suit in suits for value in values]
    random.shuffle(deck)
    return deck

def deal_cards(deck, number):
    """Deal a specific number of cards from the deck"""
    dealt_cards = deck[:number]
    del deck[:number]
    return dealt_cards

# how can i implement this function with sys module library 
def clear_screen():
    pass

def card_value(card):
    """Get the numeric value of a card"""
    return int(card.split('-')[0])

def sum_table(table):
    return sum(card_value(card) for card in table)

def find_matching_card(card, table):
    """Find a card on the table with the same value"""
    for i, table_card in enumerate(table):
        if card_value(table_card) == card_value(card):
            return i
    return -1


def find_combinations(card, table, combo_size):
    """Find all combinations of cards on the table that sum up to the played card's value"""
    target = card_value(card)
    combinations = []
    
    for combo in itertools.combinations(enumerate(table), combo_size):
        if sum(card_value(c) for _, c in combo) == target:
            combinations.append([combo_size] + [c for _, c in combo] + [i for i, _ in combo])
    
    return combinations

def get_all_combinations(card, table):
    return (find_combinations(card, table, 2) +
            find_combinations(card, table, 3) +
            find_combinations(card, table, 4))

'''
#example of combinations:  [
    [combo_size, 'values', indexes]
    [2, '3', '2', 0, 1],
    [2, '4', '1', 2, 3]    ]
'''

def play_card(card_index, player_hand, table):
    """Play a card from the player's hand"""
    card = player_hand.pop(card_index)
    captured = []

    if sum_table(table) == card_value(card):
        captured = [card] + table
        table.clear()
    elif (match_index := find_matching_card(card, table)) != -1:
        captured = [card, table.pop(match_index)]
    elif (combinations := get_all_combinations(card, table)):   
        print("Available combinations:")
        for i, combo in enumerate(combinations, 1):
            print(f"{i}: {' '.join(combo[1:combo[0]+1])}")
        
        choice = int(input("Choose a combination (number): ")) - 1
        chosen_combo = combinations[choice]
        
        captured = [card] + chosen_combo[1:chosen_combo[0]+1]
        for index in sorted(chosen_combo[chosen_combo[0]+1:], reverse=True):
            table.pop(index)
    else:
        table.append(card)

    return captured

def play_round(player1_hand, player2_hand, table):
    """Play a single round of the game"""
    for _ in range(3):
        # Player 2's turn
        print("Player 1's turn")
        print(f"P1 Hand: {player2_hand}")
        print(f"Table: {table}")
        card_index = int(input("Choose a card to play (1-3): ")) - 1
        captured = play_card(card_index, player1_hand, table)
        player1_score.extend(captured)

        clear_screen()

        # Player 1's turn
        print("Player 2's turn")
        print(f"P2 Hand: {player1_hand}")
        print(f"Table: {table}")
        card_index = int(input("Choose a card to play (1-3): ")) - 1
        captured = play_card(card_index, player2_hand, table)
        player2_score.extend(captured)

        clear_screen()

def calculate_score(player_score):
    score = 0
    if len(player_score) > 20:
        score += 1
    if "7-♦" in player_score:
        score += 1
    if sum(1 for card in player_score if card[0] == "7") > 2:
        score += 1
    if (sum(1 for card in player_score if card[0] == "7") == 2 and 
        sum(1 for card in player_score if card[0] == "6") > 2):
        score += 1
    if sum(1 for card in player_score if card[2] == "♦") > 5:
        score += 1
    return score

# Main game loop
def play_game():

    while max(total_score) < FINAL_SCORE:
        deck = create_deck()
        
        player1_hand = []
        player2_hand = []
        table = []

        # Initial deal
        player2_hand = deal_cards(deck, 3)
        player1_hand = deal_cards(deck, 3)
        table = deal_cards(deck, 4)

        for round in range(1, 7):
            print(f"Round {round}: -------------------------------")
            play_round(player1_hand, player2_hand, table)
            
            if round < 6:
                player2_hand.extend(deal_cards(deck, 3))
                player1_hand.extend(deal_cards(deck, 3))

        #Update Total scores    
        total_score[0] += calculate_score(player1_score)
        total_score[1] += calculate_score(player2_score)

    print("Game Over!")
    print("Player 1 Wins!" if total_score[0] > total_score[1] else "Player 2 Wins!")

# Initialize game variables
FINAL_SCORE = 11  # or 21, based on user choice
total_score = [0, 0]
player1_score = []
player2_score = []

# Start the game
play_game()