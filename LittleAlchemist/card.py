class Card:
    def __init__(self, name, level, combo_type, attack, defense):
        self.name = name
        self.level = int(level)
        self.combo_type = combo_type
        self.attack = int(attack)
        self.defense = int(defense)
    