from player import Player
from settings import all_cards_stats, all_combos


class Ai(Player):
    def __init__(self, num):
        super().__init__(num)
        
    def play_card(self, show=True):
        if show:
            self.show_hand()

        all_possible_combos = {}
        i = 0
        for card in self.hand: # TODO
            if card.combo_type == 'c':
                temp_hand = self.get_temp_hand(self.get_card_hand_index(card))
                possible_combo_cards = self.get_possible_combo_cards(card, temp_hand)

                for pcc in possible_combo_cards:
                    all_possible_combos[card] = {pcc: self.get_combo_result_name(card, pcc)}
        

        print(all_possible_combos)
        return all_possible_combos, 1


""" {
    card1: {card2: "coiso", card4: "a", card5: "b"},
    card2: {}
} """


