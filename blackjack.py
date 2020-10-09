# Blackjack game in python
import random
import reading_from_user

money = 1000
bet = 0


def load_stats():
    global money
    file = open('save.txt', 'r')
    money = int(file.read())
    file.close()


def save_stats():
    global money
    file = open('save.txt', 'w')
    file.write(str(money))
    file.close()


def create_deck():
    class Card:
        def __init__(self, value, suit):
            self.value = value
            self.suit = suit

        def __str__(self):
            return "{0}  {1}".format(self.suit, self.value)

    suits = ['heart', 'diamonds', 'spades', 'clubs']
    deck = [Card(value, suit) for value in range(1, 11) for suit in suits]
    deck += [Card(value, suit) for value in range(1, 11) for suit in suits]
    deck += [Card(value, suit) for value in range(1, 11) for suit in suits]
    random.shuffle(deck)

    return deck


deck = create_deck()


def deal_cards():
    global money, x
    global bet
    dealer_hand = []
    dealer_total = 0
    player_hand = []
    player_total = 0
    i = 0
    ace_p = False
    ace_d = False

    while i < 1:
        dealer_hand.append(str(deck[random.randint(0, 119)]))
        if int(dealer_hand[len(dealer_hand) - 1].split("  ")[1]) == 1 and dealer_total + 11 <= 21:
            dealer_total += 11
            ace_d = True
        else:
            dealer_total += int(dealer_hand[len(dealer_hand) - 1].split("  ")[1])
        i += 1

    i = 0

    while i < 2:
        player_hand.append(str(deck[random.randint(0, 119)]))
        if int(player_hand[len(player_hand) - 1].split("  ")[1]) == 1 and player_total + 11 <= 21:
            player_total += 11
            ace_p = True
        else:
            player_total += int(player_hand[len(player_hand) - 1].split("  ")[1])
        i += 1

    while True:
        print("Dealer has: " + str(dealer_hand))
        print(" Total: " + str(dealer_total))
        print("Player has: " + str(player_hand))
        print(" Total: " + str(player_total))

        if player_total == 21 and len(player_hand) == 2:
            print("Blackjack!")
            print("You won: " + str(bet * 1.5))
            money += int(bet * 1.5)
            break

        elif player_total == 21:
            x = 's'

        elif player_total < 21:
            print("Would you like to hit (h) or stand (s)?")
            x = input()

        if x == 'h':
            player_total, ace_p = hit(player_hand, player_total, ace_p)
            if player_total > 21:
                print("Player has: " + str(player_hand))
                print(" Total: " + str(player_total))
                print("PLAYER BUST -- DEALER WINS")
                money -= bet
                print("You lost: " + str(bet))
                break

        if x == 's':
            while dealer_total < 17:
                dealer_total, ace_d = stand(dealer_hand, dealer_total, ace_d)

            if 17 <= dealer_total <= 21:
                print("Dealer stands on: " + str(dealer_hand) + " Total: " + str(dealer_total))
                print("Player has: " + str(player_hand) + " Total: " + str(player_total))
                if dealer_total > player_total:
                    print("DEALER WINS")
                    money -= bet
                    print("You lost: " + str(bet))

                elif player_total > dealer_total:
                    print("PLAYER WINS")
                    money += bet
                    print("You won: " + str(bet))

                elif player_total == dealer_total:
                    print("PUSH")

                break

            elif dealer_total > 21:
                print("Dealer has: " + str(dealer_hand) + " " + str(dealer_total))
                print("DEALER BUST -- PLAYER WINS")
                money += bet
                print("You won: " + str(bet))
                break


def hit(player_hand, player_total, ace_p):
    player_hand.append(str(deck[random.randint(0, 119)]))
    if int(player_hand[len(player_hand) - 1].split("  ")[1]) == 1 and player_total + 11 <= 21:
        player_total += 10
        ace_p = True
    else:
        for card in player_hand:
            while ace_p:
                if card.lstrip("heartdiamondsspadesclubs  ") == '1' and player_total + int(
                        player_hand[len(player_hand) - 1].split("  ")[1]) > 21:
                    player_total -= 10
                    ace_p = False
                else:
                    break

    player_total += int(player_hand[len(player_hand) - 1].split("  ")[1])
    print("-------------------------------")
    return player_total, ace_p


def stand(dealer_hand, dealer_total, ace_d):
    dealer_hand.append(str(deck[random.randint(0, 119)]))
    if int(dealer_hand[len(dealer_hand) - 1].split("  ")[1]) == 1 and dealer_total + 11 <= 21:
        dealer_total += 10
        ace_d = True
    else:
        for card in dealer_hand:
            while ace_d:
                if card.lstrip("heartdiamondsspadesclubs  ") == '1' and dealer_total + int(
                        dealer_hand[len(dealer_hand) - 1].split("  ")[1]) > 21:
                    dealer_total -= 10
                    ace_d = False
                else:
                    break

    dealer_total += int(dealer_hand[len(dealer_hand) - 1].split("  ")[1])
    print("Dealer has: " + str(dealer_hand) + " Total: " + str(dealer_total))
    return dealer_total, ace_d


def handle_bet(bet):
    menu = "Please place a bet\n>> "
    bet = reading_from_user.read_positive_integer(menu)
    return bet


def show_menu():
    global bet, choice
    load_stats()
    menu = "Please select an option from below.\n1. Start game\n2. Quit + save game\n>> "
    while True:
        if money == 0:
            print("You ran out of money! Better luck next time.")
            file = open('save.txt', 'w')
            file.write('1000')
            file.close()
            break
        print("Current balance: " + str(money))
        choice = reading_from_user.read_positive_integer(menu)
        if choice == 1:
            print("Current balance: " + str(money))
            bet = handle_bet(bet)
            while bet > money:
                print("You cannot bet more than you have.")
                bet = handle_bet(bet)
            deal_cards()
        elif choice == 2:
            save_stats()
            break
    return choice

def main():
    show_menu()


main()
