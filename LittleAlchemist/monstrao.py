import csv
import random 
from recipes.combos import get_all_combos


class Card:
    def __init__(self, name, level, combo_type, attack, defense):
        self.name = name
        self.level = level
        self.combo_type = combo_type
        self.attack = attack
        self.defense = defense


class Player:
    def __init__(self, num):
        self.num = num
        self.deck = []
        self.hand = []
        self.used_cards = []

    def show_hand(self):
        print(f"-----------------------------Player {self.num} Hand---------------------------------")
        for i, card in enumerate(self.hand):
            print(f"Card {i+1}: {card.name.upper()}")
            print(f"\tLevel: {card.level}\tAttack: {card.attack}\tDefense: {card.defense}\tCombo Type: {card.combo_type}\n")

    def show_and_choose_options(self):
        decided = False
        play_card_name = None
        play_card_combo_type = None
        while not decided:

            self.show_hand()
            choice = input("Select a card: ")
            if choice not in ['1', '2', '3', '4', '5']:
                print("ERROR: Wrong input in combo decision.\n")
                continue
                
            choice = int(choice)
            print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            selected_card = self.hand[choice-1]
            temp_hand = self.get_temp_hand(choice)
            temp_hand_indices = self.get_temp_hand_indices(temp_hand)

            if selected_card.combo_type == 'c':
                choice = self.show_and_choose_possible_combos(selected_card, temp_hand)
                if choice:
                    card_to_combo_with = self.hand[int(choice)-1]

                if choice in temp_hand_indices and choice in self.combable_cards_indexes and card_to_combo_with.combo_type == 'c':
                    result_card_name = all_combos[selected_card.name][card_to_combo_with.name]
                    confirm_choice = self.confirm_choice(result_card_name, 'C').lower()
                    if confirm_choice == 'y':
                        print("")
                        decided = True
                        play_card_name = result_card_name
                        play_card_combo_type = 'C'
                    elif confirm_choice == 'n':
                        print("")
                    else:
                        print("ERROR: Wrong input in combo decision.\n")
            
            elif selected_card.combo_type == 'f':
                confirm_choice = self.confirm_choice(selected_card.name, 'f').lower()
                if confirm_choice == 'y':
                    decided = True
                    play_card_name = selected_card.name
                    play_card_combo_type = 'f'
                elif confirm_choice == 'n':
                    self.start_round()
                else:
                    print("ERROR: Wrong input in combo decision.\n")

        return play_card_name, play_card_combo_type

    def get_temp_hand(self, choice):
        temp_hand = self.hand.copy()
        temp_hand.pop(choice-1)
        return temp_hand

    def get_temp_hand_indices(self, temp_hand):
        return [str(self.hand.index(card)+1) for card in temp_hand]

    def show_and_choose_possible_combos(self, selected_card, temp_hand):
        print("Possible combos:")
        possible_combo_cards = self.get_possible_combo_cards(selected_card, temp_hand)
        possible_combo_cards_indices = self.get_possible_combo_cards_indices(possible_combo_cards)

        self.combable_cards_indexes = []
        for card in possible_combo_cards:
            result_card_name = all_combos[selected_card.name][card.name]
            self.combable_cards_indexes.append(str(self.hand.index(card)+1))
            print(f"{self.hand.index(card)+1}: Combo with {card.name.upper()} --> {self.display_card_with_stats(result_card_name)})")
        
        choice = input(f"Choose card number {possible_combo_cards_indices} to combo or press 'C' to cancel: ")
        print("")

        if choice.lower() == 'c':
            return
        elif choice in self.get_temp_hand_indices(temp_hand):
            return choice
        else:
            print("ERROR: Wrong input in combo decision.\n")
            return

    def get_possible_combo_cards(self, card, temp_hand):
        return [c for c in temp_hand if c.name in all_combos[card.name].keys()]
    
    def get_possible_combo_cards_indices(self, possible_combo_cards):
        return [str(self.hand.index(card)+1) for card in possible_combo_cards]

    def display_card_with_stats(self, card_name):
        return (f"{card_name.upper()} (Level: {all_cards_stats[card_name]['level']},  Attack: {all_cards_stats[card_name]['attack']}, Defense: {all_cards_stats[card_name]['defense']})")

    def confirm_choice(self, card_name, combo_type):
        return input(f"Play card: {self.display_card_with_stats(card_name)}, combo type: {combo_type} ? (y/n)\n")
        


class Ai(Player):
    def __init__(self, num):
        super().__init__(num)




class Game:
    def __init__(self):
        global all_cards_stats
        global all_combos
        all_cards_stats = self.get_all_cards_stats()
        all_combos = get_all_combos()

        self.players = [Player(1), Ai(2)]
        self.decks = [self.get_deck(), self.get_deck()]
        self.shuffle_decks()
        self.hand_player_cards()
        self.game()

    def game(self):
        player_card_name, player_combo_type = self.players[0].show_and_choose_options()
        print(self.get_card_from_name(player_card_name, player_combo_type))

    def get_card_from_name(self, card_name, combo_type):
        return Card(card_name, 1, combo_type, all_cards_stats[card_name]['attack'], all_cards_stats[card_name]['defense'])

    def hand_player_cards(self):
        for i, player in enumerate(self.players):
            player.deck = self.decks[i]
            player.hand = player.deck[:5]
            player.deck = player.deck[5:]

    def shuffle_decks(self):
        for deck in self.decks:
            random.shuffle(deck)

    def get_all_cards_stats(self):
        with open('cards/cards_stats.csv') as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
            lines = lines[1:]
            l = []
            for s in lines:
                l.append(s.split(','))
            return {line[0]: {"level": line[1], "attack": line[2], "defense": line[3]} for line in l}

    def get_deck(self):
        deck = []
        cards_stats = self.read_csv('cards/cards_stats.csv')
        starting_deck = self.read_csv('cards/starting_deck.csv')
        for starting_deck_card in starting_deck:
            for i in range(int(starting_deck_card['number'])):
                for card in cards_stats:
                    if starting_deck_card['name'] == card['name']:
                        deck.append(Card(card['name'], int(card['level']), starting_deck_card['combo_type'], int(card['attack']), int(card['defense'])))
        return deck

    def read_csv(self, file):
        deck = []
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                deck.append(row)
        return deck




if __name__=='__main__':

    all_cards_stats = {}
    all_combos = {}
    game = Game()
