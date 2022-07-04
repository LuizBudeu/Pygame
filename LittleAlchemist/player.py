import pygame
from settings import *
from card import Card
from ui_utils import *


class Player:
    def __init__(self, num, health=30):
        self.num = num
        self.deck = []
        self.hand = []
        self.used_cards = []
        self.health = health
        self.total_health = health

    def show_hand(self, screen):
        for i, card in enumerate(self.hand):
            if self.num == 1:
                card.draw(screen, (80 + 260*(i), 620))
            elif self.num == 2:
                pass                                      # TODO
    
    def show_healthbar(self, screen):
        if self.num == 1:
            rect_pos = (0, 0)
            health_text_pos = (175, 27)
            player_text_pos = (10, 60)
        elif self.num == 2:
            rect_pos = (1090, 0)
            health_text_pos = (1265, 27)
            player_text_pos = (1320, 60)

        red_rect = pygame.Rect(rect_pos[0], rect_pos[1], 350, 50)
        green_rect = pygame.Rect(rect_pos[0], rect_pos[1], round(self.health/self.total_health*350), 50)
        
        pygame.draw.rect(screen, REDDISHBROWN, red_rect)
        pygame.draw.rect(screen, GREEN, green_rect)
        pygame.draw.rect(screen, BROWN, red_rect, 3)
        write_text(screen, text=str(self.health), size=30, color=(0, 0, 0), center_pos=health_text_pos)
        write_text(screen, f"Player {self.num}", size=25, color=(0, 0, 0), topleft_pos=player_text_pos)

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