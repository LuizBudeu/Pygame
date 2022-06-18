from recipes.combos import get_all_combos


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



all_cards_stats = get_all_cards_stats()
all_combos = get_all_combos()

