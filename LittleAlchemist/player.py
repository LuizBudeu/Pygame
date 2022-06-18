from settings import all_cards_stats, all_combos
from card import Card


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
                            play_card = self.get_card_from_name(selected_card.name, 'c')
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

        for card in just_used_cards:
            self.hand.remove(card)
            self.used_cards.append(card)

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
        
        choice = input(f"Choose card number {possible_combo_cards_indices} to combo, [{self.get_card_hand_index(selected_card)}] to play selected card without comboing, or press 'C' to cancel: ")
        print("")

        if choice.lower() == 'c':
            return
        elif choice in self.get_temp_hand_indices(temp_hand) or int(choice) == self.get_card_hand_index(selected_card):
            return choice
        else:
            print("ERROR: Wrong input in combo decision.\n")
            return

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