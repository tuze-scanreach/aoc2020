from copy import deepcopy


def vf(array):
    return array[::-1]


def hf(array):
    return [i[::-1] for i in array]


def rotate90(array):
    return list(zip(*array[::-1]))


def rotate180(array):
    array = rotate90(array)
    return rotate90(array)


def rotate270(array):
    array = rotate180(array)
    return rotate90(array)


def match_l(tile1, tile2):
    try:
        return all(tile2[i][len(tile2[0]) - 1] == tile1[i][0]
                   for i in range(len(tile1)))
    except:
        print(f"{len(tile2)}, {len(tile1)}")
        raise Exception


def match_r(tile1, tile2):
    try:
        return all(tile2[i][0] == tile1[i][len(tile1[0]) - 1]
                   for i in range(len(tile1)))
    except:
        print(f"{len(tile2)}, {len(tile1)}, {i}")
        raise Exception


def match_u(tile1, tile2):
    return tile2[len(tile2) - 1][:] == tile1[0][:]


def match_d(tile1, tile2):
    return tile2[0][:] == tile1[len(tile1) - 1][:]


def match_puzzle_piece(piece, array_of_puzzle_pieces):
    for next_piece in array_of_puzzle_pieces:
        if next_piece.id != piece.id:
            if piece.b_val == next_piece.u_val:
                piece.below = tile_id
            elif piece.u_val == next_piece.b_val:
                piece.above = tile_id
            elif piece.l_val == next_piece.r_val:
                piece.left = tile_id
            elif piece.r_val == next_piece.l_val:
                piece.right = tile_id


def match_puzzles(array_of_puzzle_pieces, tile_array):
    for piece in array_of_puzzle_pieces:
        match_puzzle_piece(piece, array_of_puzzle_pieces)


class PuzzlePiece:
    def __init__(self, piece_id, r_val, l_val, u_val, b_val):
        self.id = piece_id
        self.r_val = r_val
        self.l_val = l_val
        self.u_val = u_val
        self.b_val = b_val
        self.above = None
        self.below = None
        self.left = None
        self.right = None

    def __repr__(self):
        return f'Id:{self.id}, a:{self.above}, b:{self.below}, l:{self.left}, r:{self.right}'

    def get_score(self):
        return (int(self.above != None) + int(self.below != None) +
                int(self.left != None) + int(self.right != None))

    def rotate90(self):
        new_l = self.b_val
        new_r = self.u_val
        self.b_val = self.r_val
        self.u_val = self.l_val
        self.l_val = new_l
        self.r_val = new_r

    def hf(self):
        new_l = self.r_val
        self.r_val = self.l_val
        self.l_val = new_l
        self.u_val = int('{0:10b}'.format(self.u_val)[:1:-1], 2)
        self.b_val = int('{0:10b}'.format(self.b_val)[:1:-1], 2)

    def vf(self):
        new_u = self.b_val
        self.b_val = self.u_val
        self.u_val = new_u
        self.r_val = int('{0:10b}'.format(self.r_val)[:1:-1], 2)
        self.l_val = int('{0:10b}'.format(self.l_val)[:1:-1], 2)

    def __lt__(self, other):
        return self.get_score() < other.get_score()


tiles = {}
with open('aoc20.txt') as f:
    input_txt = f.readlines()

current_tile_no = None
current_line_no = 0
for line in input_txt:
    if "Tile " in line:
        current_tile_no = int(line[len("Tile "):len(line) - 2])
        tiles[current_tile_no] = list()
        current_line_no = 0
    elif line != "\n":
        tiles[current_tile_no].append(line[:10].replace('.',
                                                        '0').replace('#', '1'))

puzzle_dim = len(tiles)**0.5
assert puzzle_dim == int(puzzle_dim), "not a square"

puzzle_dim = int(puzzle_dim)
puzzle_solution = [[-1] * puzzle_dim] * puzzle_dim

puzzle_pieced = list()

for tile_id in tiles.keys():
    lval = int("".join([i[0] for i in tiles[tile_id]]), 2)
    rval = int("".join([i[len(i) - 1] for i in tiles[tile_id]]), 2)
    puzzle_pieced.append(
        PuzzlePiece(tile_id, rval, lval, int(tiles[tile_id][0], 2),
                    int(tiles[tile_id][9], 2)))
    assert len(tiles[tile_id]) == len(
        tiles[tile_id][9]), f"not the same length"

possible_mutations = [
    vf, rotate90, rotate90, rotate90, rotate90, vf, hf, rotate90, rotate90,
    rotate90, rotate90, hf
]
done = False
while not done:
    match_puzzles(puzzle_pieced, tiles)
    puzzle_pieced.sort()
    piece_index = 0
    mass_mutate_index = 0
    tries = 0
    tile_score = puzzle_pieced[piece_index].get_score()
    if tile_score > 1:
        break
    while tile_score >= puzzle_pieced[piece_index].get_score():
        tile_idx = puzzle_pieced[piece_index].id
        for mutate in possible_mutations:
            tiles[tile_idx] = mutate(tiles[tile_idx])
            match_puzzle_piece(puzzle_pieced[piece_index], tiles)
            if tile_score < puzzle_pieced[piece_index].get_score():
                break
        tries += 1
        if tries == len(possible_mutations):
            tries = 0
            for piece in puzzle_pieced:
                if piece.get_score() > 2:
                    tiles[piece.id] = possible_mutations[mass_mutate_index](
                        tiles[piece.id])
                mass_mutate_index = (mass_mutate_index +
                                     1) % len(possible_mutations)

match_puzzles(puzzle_pieced, tiles)
puzzle_pieced.sort()
print(puzzle_pieced)

multip = 1
for piece in puzzle_pieced:
    if piece.get_score() == 2:
        multip *= piece.id

print(multip)

# for i in range(puzzle_dim):
#     start_idx = i * puzzle_dim
#     puzzle_solution.append([])
#     for id_idx in range(puzzle_dim):
#         puzzle_solution[i].append(list(tiles.keys())[start_idx + id_idx])

# print(tiles.keys())
# print(puzzle_solution)
