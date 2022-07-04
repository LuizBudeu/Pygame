import csv
import random 
from recipes.combos import get_all_combos



# Funções Globais
def get_all_cards_stats():
    with open('cards/cards_stats.csv') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        lines = lines[1:]
        l = []
        for s in lines:
            l.append(s.split(','))
        return {line[0]: {"level": line[1], "attack": line[2], "defense": line[3]} for line in l}

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key
    return "key doesn't exist"



# Classes
class Card:
    def __init__(self, name, level, combo_type, attack, defense):
        self.name = name
        self.level = int(level)
        self.combo_type = combo_type
        self.attack = int(attack)
        self.defense = int(defense)


class Player:
    def __init__(self, num, health=30):
        self.num = num
        self.deck = []
        self.hand = []
        self.used_cards = []
        self.health = health

    def show_hand(self):
        print(f"-------------------------- Player {self.num} Hand -----------------------------")
        for i, card in enumerate(self.hand):
            print(f"Card {i+1}: {card.name.upper()}")
            print(f"\tLevel: {card.level}\tAttack: {card.attack}\tDefense: {card.defense}\tCombo Type: {card.combo_type}\n")

    def play_card(self):
        decided = False
        play_card = None
        just_used_cards = []

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
                        result_card_name = self.get_combo_result_name(selected_card, card_to_combo_with)
                        confirm_choice = self.confirm_choice(result_card_name, 'C').lower()
                        if confirm_choice == 'y':
                            print("")
                            decided = True
                            just_used_cards.append(selected_card)
                            just_used_cards.append(card_to_combo_with)
                            play_card = self.get_card_from_name(result_card_name, 'C')
                        elif confirm_choice == 'n':
                            print("")
                        else:
                            print("ERROR: Wrong input in combo decision.\n")
                    
                    elif int(choice) == self.get_card_hand_index(selected_card):
                        confirm_choice = self.confirm_choice(selected_card.name, 'c').lower()
                        if confirm_choice == 'y':
                            print("")
                            decided = True
                            just_used_cards.append(selected_card)
                            play_card = self.hand[self.hand.index(selected_card)]
                        elif confirm_choice == 'n':
                            print("")
                        else:
                            print("ERROR: Wrong input in combo decision.\n")
            
            elif selected_card.combo_type == 'f':
                confirm_choice = self.confirm_choice(selected_card.name, 'f').lower()
                if confirm_choice == 'y':
                    decided = True
                    just_used_cards.append(selected_card)
                    play_card = self.get_card_from_name(selected_card.name, 'f')
                elif confirm_choice == 'n':
                    print("")
                else:
                    print("ERROR: Wrong input in combo decision.\n")

        self.use_up_cards(just_used_cards)

        return play_card, len(just_used_cards)

    def show_and_choose_possible_combos(self, selected_card, temp_hand):
        print("Possible combos:")
        possible_combo_cards = self.get_possible_combo_cards(selected_card, temp_hand)
        possible_combo_cards_indices = self.get_possible_combo_cards_indices(possible_combo_cards)

        self.combable_cards_indexes = []
        for card in possible_combo_cards:
            result_card_name = self.get_combo_result_name(selected_card, card)
            self.combable_cards_indexes.append(str(self.get_card_hand_index(card)))
            print(f"{self.get_card_hand_index(card)}: Combo with {card.name.upper()} --> {self.display_card_with_stats(result_card_name)})")
        
        choice = input(f"Choose card number {possible_combo_cards_indices} to combo, [{self.get_card_hand_index(selected_card)}] to play selected card without comboing, or press anything else to cancel: ")
        print("")

        if choice not in ['1', '2', '3', '4', '5']:
            return
        """ elif choice in self.get_temp_hand_indices(temp_hand) or int(choice) == self.get_card_hand_index(selected_card): 
            return choice
        else:
            print("ERROR: Wrong input in combo decision.\n")
            return """
        return choice

    def isAlive(self):
        return self.health > 0

    def show_health(self):
        print(f"Player {self.num} health: {self.health}")

    def show_chosen_card_stats(self, chosen_card):
        print(f"Player {self.num} Card: {chosen_card.name.upper()} --- Attack: {chosen_card.attack}\tDefense: {chosen_card.defense}")

    def use_up_cards(self, just_used_cards):
        for card in just_used_cards:
            self.hand.remove(card)
            self.used_cards.append(card)

    def get_card_hand_index(self, card):
        return self.hand.index(card)+1

    def get_card_from_name(self, card_name, combo_type):
        return Card(card_name, 1, combo_type, all_cards_stats[card_name]['attack'], all_cards_stats[card_name]['defense'])

    def get_combo_result_name(self, card1, card2):
        return all_combos[card1.name][card2.name]

    def get_temp_hand(self, choice):
        temp_hand = self.hand.copy()
        temp_hand.pop(choice-1)
        return temp_hand

    def get_temp_hand_indices(self, temp_hand):
        return [str(self.get_card_hand_index(card)) for card in temp_hand]

    def get_possible_combo_cards(self, card, temp_hand):
        return [c for c in temp_hand if c.name in all_combos[card.name].keys()]
    
    def get_possible_combo_cards_indices(self, possible_combo_cards):
        return [str(self.get_card_hand_index(card)) for card in possible_combo_cards]

    def display_card_with_stats(self, card_name):
        return (f"{card_name.upper()} (Level: {all_cards_stats[card_name]['level']},  Attack: {all_cards_stats[card_name]['attack']}, Defense: {all_cards_stats[card_name]['defense']})")

    def confirm_choice(self, card_name, combo_type):
        return input(f"Play card: {self.display_card_with_stats(card_name)}, combo type: {combo_type} ? (y/n)\n")
        

class Ai(Player):
    def __init__(self, num):
        super().__init__(num)
        
    def play_card(self, show=True):
        if show:
            self.show_hand()

        best_combo_card = None
        all_possible_combos = self.get_all_possible_combos()
        if all_possible_combos:
            best_combo_card, card1, card2 = self.get_best_combo_card(all_possible_combos) 
        
        for card in self.hand: # Can be better
            if card.combo_type == 'f':
                if self.card1_better_than_card2(card, best_combo_card):
                    self.use_up_cards([card])
                    return card, 1

        if best_combo_card:
            self.use_up_cards([card1, card2])
            return best_combo_card, 2

        random_card = random.choice(self.hand)
        self.use_up_cards([random_card])
        return random_card, 1

    def get_all_possible_combos(self):
        all_possible_combos = {}
        for card in self.hand: 
            if card.combo_type == 'c':
                temp_hand = self.get_temp_hand(self.get_card_hand_index(card))
                possible_combo_cards = self.get_possible_combo_cards(card, temp_hand)

                card_combos = {}
                for pcc in possible_combo_cards:
                    card_combos[pcc] = self.get_combo_result_name(card, pcc)
                    all_possible_combos[card] = card_combos

        return all_possible_combos

    def get_best_combo_card(self, all_possible_combos):
        best_total = 0
        best_card = None
        card1, card2 = None, None
        for combo in all_possible_combos.values():
            for card_name in combo.values():
                combo_card = self.get_card_from_name(card_name, 'C')
                total = combo_card.attack + combo_card.defense
                if total > best_total:
                    card1 = get_key(all_possible_combos, combo)
                    card2 = get_key(combo, card_name)
                    best_total = total
                    best_card = combo_card

        return best_card, card1, card2

    def card1_better_than_card2(self, card1, card2):
        if not card1:
            return False
        if not card2:
            return True
        if card1.attack + card1.defense > card2.attack + card2.defense:
            return True
        return False




class Game:
    def __init__(self):
        self.players = [Player(1), Ai(2)]
        self.decks = [self.get_deck(), self.get_deck()]
        self.shuffle_decks()
        self.hand_players_cards()
        self.game()

    def game(self):
        while self.players[0].isAlive() and self.players[1].isAlive():
            self.show_healths()

            player_card, player_n_used = self.players[0].play_card()
            ai_card, ai_n_used = self.players[1].play_card()

            self.battle(player_card, ai_card)

            self.hand_new_cards(self.players[0], player_n_used)
            self.hand_new_cards(self.players[1], ai_n_used)

        self.show_winner()
        a = input("\nPress ENTER to close program.")

    def battle(self, player_card, ai_card):
        print(f"\n----------------------------- Battle ---------------------------------")
        self.players[0].show_chosen_card_stats(player_card)
        self.players[1].show_chosen_card_stats(ai_card)

        self.show_damages(player_card, ai_card)

    def show_winner(self):
        if not self.players[0].isAlive():
            print(f"\nPlayer 2 wins!")
        elif not self.players[1].isAlive():
            print(f"\nPlayer 1 wins!")
        elif not self.players[0].isAlive() and not self.players[1].isAlive():
            print(f"\nDraw!")
        else:
            print("ERROR")
        

    def show_healths(self):
        print(f"\n----------------------------------------------------------------------")
        for player in self.players:
            player.show_health()
        print("")

    def show_damages(self, player_card, ai_card):
        player_damage_taken, ai_damage_taken = self.calculate_damage_taken(player_card, ai_card)
        self.players[0].health -= player_damage_taken
        self.players[1].health -= ai_damage_taken
        print(f"\nPlayer 1 damage taken: {player_damage_taken}")
        print(f"Player 2 damage taken: {ai_damage_taken}")

    def calculate_damage_taken(self, card1, card2):
        card2_damage_taken = card1.attack - card2.defense 
        if card2_damage_taken < 0:
            card2_damage_taken = 0

        card1_damage_taken = card2.attack - card1.defense
        if card1_damage_taken < 0:
            card1_damage_taken = 0
        
        return card1_damage_taken, card2_damage_taken

    def hand_new_cards(self, player, n_used):
        get_cards = player.deck[:n_used]
        for card in get_cards:
            player.hand.append(card)
        player.deck = player.deck[n_used:]

    def hand_players_cards(self):
        for i, player in enumerate(self.players):
            player.deck = self.decks[i]
            player.hand = player.deck[:5]
            player.deck = player.deck[5:]

    def shuffle_decks(self):
        for deck in self.decks:
            random.shuffle(deck)

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




# Variáveis globais
all_cards_stats = get_all_cards_stats()
all_combos = get_all_combos()



# Inicializa
if __name__=='__main__':
    game = Game()
