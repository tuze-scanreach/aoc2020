from collections import defaultdict
from copy import deepcopy


def add_and_check_lists(deck_cache, player1, player2):
    p1_hash = hash(tuple(player1))
    p2_hash = hash(tuple(player2))
    recursion = False
    if (p1_hash, p2_hash) in deck_cache:
        recursion = True
    deck_cache.add((p1_hash, p2_hash))
    return recursion


def play_game(player1, player2):
    deck_cache = set()
    done = False
    while not done:
        if add_and_check_lists(deck_cache, player1, player2):
            return True
        p1_hand = player1[0]
        player1.remove(p1_hand)
        p2_hand = player2[0]
        player2.remove(p2_hand)
        p1_won = True
        if (len(player1) >= p1_hand and len(player2) >= p2_hand):
            player1_subgame = deepcopy(player1[:p1_hand])
            player2_subgame = deepcopy(player2[:p2_hand])
            p1_won = play_game(player1_subgame, player2_subgame)
        elif p1_hand < p2_hand:
            p1_won = False
        elif p1_hand == p2_hand:
            assert False, "unhandled"

        if p1_won:
            player1.append(p1_hand)
            player1.append(p2_hand)
        else:
            player2.append(p2_hand)
            player2.append(p1_hand)

        done = (len(player1) == 0) or (len(player2) == 0)
    return (len(player1) > 0)


decks = defaultdict(list)
with open('aoc22.txt') as f:
    input_txt = f.readlines()

current_player = None
for line in input_txt:
    if "Player" in line:
        current_player = line.rstrip()
    elif line != '\n':
        decks[current_player].append(int(line.rstrip()))

p1_won = play_game(decks["Player 1:"], decks["Player 2:"])

winning_deck = decks["Player 1:"]
if len(decks["Player 1:"]) == 0:
    winning_deck = decks["Player 2:"]

score = 0
print(winning_deck)
for counter, val in enumerate(winning_deck[::-1]):
    score += (counter + 1) * val

print(score)