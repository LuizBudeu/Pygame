import csv
import random 
from player import Player
from card import Card
from ai import Ai


class Game:
    def __init__(self):
        self.players = [Player(1), Ai(2)]
        self.decks = [self.get_deck(), self.get_deck()]
        self.shuffle_decks()
        self.hand_players_cards()
        self.game()

    def game(self):
        player_card, player_n_used = self.players[0].play_card()
        ai_card, ai_n_used = self.players[1].play_card()

        self.battle(player_card, ai_card)

        self.hand_new_cards(self.players[0], player_n_used)
        self.hand_new_cards(self.players[1], ai_n_used)

    def battle(self, player_card, ai_card):
        print(f"Player Card: {player_card.name.upper()}")
        print(f"Enemy Card: {ai_card.name.upper()}")

    def hand_new_cards(self, player, n_used):
        player.hand.append(player.deck[:n_used])
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
    