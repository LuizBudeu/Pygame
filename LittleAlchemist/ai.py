from player import Player
from card import Card
from settings import *


class Ai(Player):
    def __init__(self, num):
        super().__init__(num)
        
    def play_card(self, show=True):
        if show:
            self.show_hand()

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



