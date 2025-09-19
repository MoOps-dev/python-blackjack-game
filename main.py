import random

logo = r"""
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   < 
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
      |  \/ K|                            _/ |                
      `------'                           |__/           
"""

card_deck = {'A':8, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8, '10':8, 'J':8, 'Q':8, 'K':8} #total 104 cards
card_value = {'A':[1, 11], '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

player_hand = []
computer_hand = []

scores = [0, 0]
balance = [300]
d_amount = [0]

def draw_card(players, cards):
    for player in players:
        for pick in range(cards):
            choice = random.choice(list(card_deck.keys()))
            player.append(choice)
            card_deck[choice] = card_deck[choice] - 1

def calc_scores(hand):
    for h in hand:
        scores[hand.index(h)] = 0
        sorted_items = sorted(h, key=lambda x: x == 'A')
        for card in sorted_items:
            if card == "A":
                if scores[hand.index(h)] + card_value[card][1] > 21:
                    scores[hand.index(h)] += card_value[card][0]
                else:
                    scores[hand.index(h)] += card_value[card][1]
            else:
                scores[hand.index(h)] += card_value[card]

def calc_card(card):
    return card_value[card]

def clear():
    player_hand.clear()
    computer_hand.clear()

def new_round():
    d_amount[0] = 0
    if balance[0] < 10:
        input("You don't have enough balance to play again, press 'ENTER' to exit ")
    else:
        ask = input("If you'd like to start a new turn enter your deal amount or press 'Enter' to end game: ").lower()
        if ask != '':
            if int(ask) > 0:
                d_amount[0] += int(ask)
                deal_cards()
        else:
            return

def start_game():
    print(logo)

    print("Welcome to BlackJack!")
    print(f"Current Balance: ${balance[0]}")

    d_amount[0] = 0
    deal = int(input("Please enter your deal amount: "))
    d_amount[0] += deal

    deal_cards()

def deal_cards():
    clear()

    print(r"""**************************NEW TURN**************************""")

    balance[0] -= d_amount[0]

    print(f"Total deal value: ${d_amount[0]} - Current Balance: ${balance[0]}")

    draw_card([player_hand, computer_hand], cards=2)
    calc_scores([player_hand, computer_hand])

    print(f"Your cards: {player_hand}, (Current score: {scores[0]})")
    print(f"Dealer's first card: {computer_hand[0]}, (Current score: {calc_card(computer_hand[0])})")

    if blackjack(player_hand) and not blackjack(computer_hand):
        result(1, "BlackJack")
        return
    elif blackjack(player_hand) and blackjack(computer_hand):
        result(0, "Push")
        return

    if computer_hand[0] == "A" and len(computer_hand) == 2:
        insurance()
        return

    round_options()

def result(winner, reason, insu = False):
    print(r"""***************************RESULT***************************""")
    if winner == 1:
        if reason == "BlackJack":
            balance[0] += d_amount[0] * 2
            print(f"You got a {reason}! You win this round.")
            print(f"Your current balance is: {balance[0]}")
            new_round()
        elif reason == "Bust":
            balance[0] += d_amount[0] * 2
            print(f"Dealer got a {reason}! You win this round.")
            print(f"Your current balance is: {balance[0]}")
            new_round()
        elif reason == "GoodHand":
            balance[0] += d_amount[0] * 2
            print(f"You got a {reason}! You win this round.")
            print(f"Your current balance is: {balance[0]}")
            new_round()

    elif winner == 0:
        if reason == "Push":
            balance[0] += d_amount[0]
            print(f"You got a {reason}! the round ends in a draw.")
            print(f"Dealer's hand: {computer_hand}, Score: {scores[1]}")
            print(f"Your current balance is: {balance[0]}")
            new_round()

    elif winner == 2:
        if reason == "BlackJack":
            if insu:
                balance[0] += d_amount[0]
                print(f"Dealer got a {reason}! You get your deal amount + insurance back.")
                print(f"Dealer's hand: {computer_hand}, Score: {scores[1]}")
                print(f"Your current balance is: {balance[0]}")
                new_round()
            else:
                print(f"Dealer got a {reason}! Dealer wins this round.")
                print(f"Dealer's hand: {computer_hand}, Score: {scores[1]}")
                print(f"Your current balance is: {balance[0]}")
                new_round()
        elif reason == "Bust":
            print(f"You got a {reason}! Dealer wins this round.")
            print(f"Dealer's hand: {computer_hand}, Score: {scores[1]}")
            print(f"Your current balance is: {balance[0]}")
            new_round()
        elif reason == "GoodHand":
            print(f"Dealer got a {reason}! Dealer wins this round.")
            print(f"Your current balance is: {balance[0]}")
            new_round()

def insurance():
    insure = input("Enter 'y' if you would like to make an insurance or 'n' to continue: ").lower()

    if insure == "y":
        amount = d_amount[0] / 2
        balance[0] -= amount
        d_amount[0] += amount
        print(f"Insurance fee has been deducted, Total deal value: ${d_amount[0]} - Current Balance: ${balance[0]}")
        dealer_blackjack(True)
    elif insure == "n":
        dealer_blackjack(False)
    else:
        print("Invalid action!")
        insurance()

def dealer_blackjack(ins):
    if blackjack(computer_hand):
        result(2, "BlackJack", ins)
    else:
        d_amount[0] -= d_amount[0] / 3
        round_options()

def blackjack(hand):
    who = 0

    if hand == computer_hand:
        who = 1
    elif hand == player_hand:
        who = 0

    if len(hand) == 2 and scores[who] == 21:
        return True

    return False

def round_options(skipped_double = False):
    print(r"""***************************ACTION***************************""")
    if skipped_double:
        option = int(input("Please choose an action: (1)Hit - (3)Stand: "))
    else:
        option = int(input("Please choose an action: (1)Hit - (2)Double - (3)Stand: "))

    if option == 1:
        hit()
    elif option == 2 and not skipped_double:
        double()
    elif option == 3:
        dealer_turn()
    else:
        print("Invalid action!")
        round_options(skipped_double)

def hit():
    print(f"Total deal value: ${d_amount[0]} - Current Balance: ${balance[0]}")

    draw_card([player_hand], 1)
    calc_scores([player_hand, computer_hand])

    if scores[0] > 21:
        print(f"Your cards: {player_hand}, (Current score: {scores[0]})")
        result(2, "Bust")
    else:
        print(f"Your cards: {player_hand}, (Current score: {scores[0]})")
        print(f"Dealer's first card: {computer_hand[0]}, (Current score: {calc_card(computer_hand[0])})")
        round_options(True)

def double():
    balance[0] -= d_amount[0]
    d_amount[0] += d_amount[0]

    print(f"Total deal value: ${d_amount[0]} - Current Balance: ${balance[0]}")

    draw_card([player_hand], 1)
    calc_scores([player_hand, computer_hand])

    if scores[0] > 21:
        print(f"Your cards: {player_hand}, (Current score: {scores[0]})")
        result(2, "Bust")
    else:
        print(f"Your cards: {player_hand}, (Current score: {scores[0]})")
        dealer_turn()

def dealer_turn():
    print(r"""**************************Dealer Hits***********************""")
    draw_card([computer_hand], 1)
    calc_scores([player_hand, computer_hand])

    print(f"Dealer's cards: {computer_hand}, (Current score: {scores[1]})")

    if scores[1] > 21:
        result(1, "Bust")
    elif scores[1] < 17:
        dealer_turn()
    else:
        compare_hands()

def compare_hands():
    if scores[0] > scores[1]:
        result(1, "GoodHand")
    elif scores[1] > scores[0]:
        result(2, "GoodHand")
    elif scores[0] == scores[1]:
        result(0, "Push")

start_game()