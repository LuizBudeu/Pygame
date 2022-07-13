import csv
import random 
import pygame
import sys
import time
from player import Player
from card import Card
from ai import Ai
from settings import *
from ui_utils import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)    
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Little Alchemist")
        icon = pygame.transform.scale(pygame.image.load("imgs/wolf_icon.png"), (64, 64))
        pygame.display.set_icon(icon)

        self.show_main_menu()
    
    def show_main_menu(self):
        while True:
            self.screen.fill(SELECTEDGREENISH)

            write_text(self.screen, text="LITTLE ALCHEMIST", font_size=100, color=(196, 190, 0), center_pos=[WINDOW_SIZE[0]//2, 200])

            play_button = Button(self.screen, text="PLAY", font_size=40, dim=(500, 100), center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 100))
            play_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if play_button.hovering():
                            self.show_game()
                
            pygame.display.update()
            self.clock.tick(60) 

    def show_game(self):
        self.init_cards()
        p1 = self.players[0]
        ai = self.players[1]

        confirm_button = None
        player1_card = None
        first_time = True

        while True:
            self.screen_update()

            back_menu_button = Button(self.screen, text="Back to menu", font_size=15, dim=(120, 50), center_pos=(WINDOW_SIZE[0]//2, 35))
            back_menu_button.draw()

            if len(p1.selected_cards_index) >= 1:
                confirm_button = Button(self.screen, text='Play', font_size=30,  dim=(130, 80), center_pos=((WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2+70)))
                confirm_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_menu_button.hovering():
                            self.show_main_menu()

                        for card in p1.hand:
                            if card.hovering():
                                if not card.selected:
                                    p1.select_card(card)
                                else:
                                    p1.deselect_card(card)

                        if confirm_button:
                            if confirm_button.hovering():
                                player1_card, player1_n_used = p1.play_card()
                                p1.selected_cards_index = []
                
            # Battle cards
            if player1_card:    
                if first_time:
                    start = time.time()
                    first_time = False
                    ai_card, ai_n_used = ai.play_card()

                self.show_battle(player1_card, ai_card)

                stop = time.time()
                if stop - start >= 1.5:   # Number of seconds
                    self.calculate_damages(player1_card, ai_card)
                    self.hand_new_cards(self.players[0], player1_n_used)
                    self.hand_new_cards(self.players[1], ai_n_used)

                    player1_card = None
                    first_time = True
                    confirm_button = None

            if self.check_winner():
                self.show_winner()

            pygame.display.update()
            self.clock.tick(60) 

    def check_winner(self):
        if self.players[0].health <= 0:
            return True
        elif self.players[1].health <= 0:
            return True
        else:
            return False

    def show_battle(self, player1_card, ai_card): 
        write_text(self.screen, text='vs', font_size=60, center_pos=(WINDOW_SIZE[0]//2, 285))
        player1_card.draw(self.screen, center_pos=(500, 285))
        ai_card.draw(self.screen, center_pos=(WINDOW_SIZE[0]//2+220, 285))
        
    def screen_update(self):
        self.screen.fill(SELECTEDGREENISH)
        self.players[0].show_hand(self.screen)
        
        for player in self.players:
            player.show_healthbar(self.screen)

    def init_cards(self):
        self.players = [Player(1), Ai(2)]
        self.decks = [self.get_deck(), self.get_deck()]
        self.shuffle_decks()
        self.hand_players_cards()

    def show_winner(self):
        if not self.players[0].is_alive() and not self.players[1].is_alive():
            winner = 'Draw'
        elif not self.players[1].is_alive():
            winner = 'Player 1 wins'
        elif not self.players[0].is_alive():
            winner = 'Player 2 wins'
        else:
            winner = 'Error'

        while True:
            write_text(self.screen, text=winner, font_size=100, center_pos=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2+70))
            back_menu_button = Button(self.screen, text="Back to menu", font_size=15, dim=(120, 50), center_pos=(WINDOW_SIZE[0]//2, 35))
            back_menu_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back_menu_button.hovering():
                            self.show_main_menu()

            pygame.display.update()
            self.clock.tick(60) 

    def calculate_damages(self, player_card, ai_card):
        player_damage_taken, ai_damage_taken = self.calculate_damage_taken(player_card, ai_card)
        self.players[0].health -= player_damage_taken
        self.players[1].health -= ai_damage_taken

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
                        deck.append(Card(card['name'], int(card['level']), starting_deck_card['combo_type'], int(card['attack']), int(card['defense']), int(card['tier']), all_card_images[card['name']]))
        return deck

    def read_csv(self, file):
        deck = []
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                deck.append(row)
        return deck
    