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
        self.selected_cards_index = []
        self.combable_cards_indexes = []

    def show_hand(self, screen):
        # Draw at default positions if not selected
        for card in self.hand:
            i = self.get_index_from_card(card)
            default_pos = player_1_default_cards_pos[i]

            if i not in self.selected_cards_index:
                card.draw(screen, player_1_default_cards_pos[i])
        
        # When there is >= 1 cards selected
        if len(self.selected_cards_index) >= 1:
            c1 = self.get_card_from_index(self.selected_cards_index[0])
            c1.draw(screen, topleft_pos=(180, 150))
            write_text(screen, text='+', font_size=100, center_pos=(507, 285))
            write_text(screen, text='=', font_size=100, center_pos=(WINDOW_SIZE[0]//2+220, 285))
            
            if c1.combo_type == 'f':
                c1.draw(screen, topleft_pos=(1040, 150))
                write_text(screen, text='x', font_size=300, center_pos=((WINDOW_SIZE[0]//2, 285)), color=(117, 117, 117))

            # If combo_type == 'c'
            else: 
                temp_hand = self.get_temp_hand(c1)
                possible_combable_cards = self.get_possible_combable_cards(c1, temp_hand)

                if len(self.combable_cards_indexes) == 0:
                    for card in possible_combable_cards:
                        result_card_name = self.get_combo_result_name(c1, card)
                        self.combable_cards_indexes.append(str(self.get_card_hand_index(card)))

            # Logic for covering non combable cards with a transparent rect
            temp_hand = self.get_temp_hand(c1)
            temp_hand_indices = self.get_temp_hand_indices(temp_hand)
            for j, card in enumerate(temp_hand):
                i = temp_hand_indices[j]
                if i not in self.combable_cards_indexes:
                    default_pos = player_1_default_cards_pos[int(i)]
                    draw_transparent_rect(screen, topleft_pos=(default_pos[0]-110, default_pos[1]-135), dim=(220, 270))
                
            # If there are 2 selected cards
            if len(self.selected_cards_index) == 2:
                c2 = self.get_card_from_index(self.selected_cards_index[1])
                c2.draw(screen, center_pos=((WINDOW_SIZE[0]//2, 285)))
                
                self.show_possible_combo_card(screen, c1, c2)

    def play_card(self):
        if len(self.selected_cards_index) == 1:
            card = self.get_card_from_index(self.selected_cards_index[0])
            self.use_up_cards([card])
            return card, 1

        elif len(self.selected_cards_index) == 2:
            i, j = self.selected_cards_index[0], self.selected_cards_index[1]
            c1, c2 = self.get_card_from_index(i), self.get_card_from_index(j)
            result_card_name = self.get_combo_result_name(c1, c2)
            self.use_up_cards([c1])
            self.use_up_cards([c2])
            return self.create_card_from_name(result_card_name, 'C'), 2

    def show_possible_combo_card(self, screen, card1, card2):
        result_card_name = self.get_combo_result_name(card1, card2)
        result_card = self.create_card_from_name(result_card_name, 'C')
        result_card.draw(screen, topleft_pos=((1040, 150)))

    def show_healthbar(self, screen):  # TODO melhorar?
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
        write_text(screen, text=str(self.health), font_size=30, color=(0, 0, 0), center_pos=health_text_pos)
        write_text(screen, f"Player {self.num}", font_size=25, color=(0, 0, 0), topleft_pos=player_text_pos)

    def select_card(self, card):
        if len(self.selected_cards_index) == 0:
            self.combable_cards_indexes = []

            card.selected = True
            self.selected_cards_index.append(self.hand.index(card))
        
        elif len(self.selected_cards_index) == 1:
            if str(self.get_index_from_card(card)) in self.combable_cards_indexes:
                card.selected = True
                self.selected_cards_index.append(self.hand.index(card))

    def deselect_card(self, card):
        i = self.get_index_from_card(card)
        if len(self.selected_cards_index) == 2:
            if not i == self.selected_cards_index[0]:
                self.combable_cards_indexes = []
                card.selected = False
                self.selected_cards_index.remove(self.hand.index(card))
        else:
            card.selected = False
            self.selected_cards_index.remove(self.hand.index(card))

    def get_card_from_index(self, index):
        return self.hand[index]

    def get_index_from_card(self, card):
        return self.hand.index(card)

    def is_alive(self):
        return self.health > 0

    def use_up_cards(self, just_used_cards):
        for card in just_used_cards:
            self.hand.remove(card)
            self.used_cards.append(card)

    def get_card_hand_index(self, card):
        return self.hand.index(card)

    def create_card_from_name(self, card_name, combo_type): # TODO no futuro mudar o level?
        return Card(card_name, 1, combo_type, all_cards_stats[card_name]['attack'], all_cards_stats[card_name]['defense'], all_cards_stats[card_name]['tier'])

    def get_combo_result_name(self, card1, card2):
        return all_combos[card1.name][card2.name]

    def get_temp_hand(self, card):
        temp_hand = self.hand.copy()
        temp_hand.remove(card)
        return temp_hand

    def get_temp_hand_indices(self, temp_hand):
        return [str(self.get_card_hand_index(card)) for card in temp_hand]

    def get_possible_combable_cards(self, card, temp_hand):
        return [c for c in temp_hand if c.name in all_combos[card.name].keys()]
    
    def get_possible_combable_cards_indices(self, possible_combo_cards):
        return [str(self.get_card_hand_index(card)) for card in possible_combo_cards]
