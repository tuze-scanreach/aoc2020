from copy import deepcopy
from random import randint
from math import sqrt


def vf(array):
    return array[::-1]


def hf(array):
    return [i[::-1] for i in array]


def rotate90(array):
    list_of_tuples = list(zip(*array[::-1]))
    return [list(elem) for elem in list_of_tuples]


def rotate180(array):
    array = rotate90(array)
    return rotate90(array)


def rotate270(array):
    array = rotate180(array)
    return rotate90(array)


def match_l(tile1, tile2):
    return all(tile2[i][len(tile2[0]) - 1] == tile1[i][0]
               for i in range(len(tile1)))


def match_r(tile1, tile2):
    return all(tile2[i][0] == tile1[i][len(tile1[0]) - 1]
               for i in range(len(tile1)))


def match_u(tile1, tile2):
    return tile2[len(tile2) - 1][:] == tile1[0][:]


def match_d(tile1, tile2):
    return tile2[0][:] == tile1[len(tile1) - 1][:]


def match_puzzle_piece(piece, tile_array):
    piece.below = None
    piece.above = None
    piece.left = None
    piece.right = None
    for tile_id in tile_array:
        if tile_id != piece.id:
            if match_d(tile_array[piece.id], tile_array[tile_id]):
                piece.below = tile_id
            elif match_u(tile_array[piece.id], tile_array[tile_id]):
                piece.above = tile_id
            elif match_l(tile_array[piece.id], tile_array[tile_id]):
                piece.left = tile_id
            elif match_r(tile_array[piece.id], tile_array[tile_id]):
                piece.right = tile_id


def match_l_all(tile1, row):
    return all(row[i] == tile1[i][0]
               for i in range(len(tile1))) or all(row[::-1][i] == tile1[i][0]
                                                  for i in range(len(tile1)))


def match_r_all(tile1, row):
    return all(row[i] == tile1[i][len(tile1[0]) - 1]
               for i in range(len(tile1))) or all(
                   row[::-1][i] == tile1[i][len(tile1[0]) - 1]
                   for i in range(len(tile1)))


def match_u_all(tile1, row):
    return (row == tile1[0][:]) or (row[::-1] == tile1[0][:])


def match_d_all(tile1, row):
    return (row == tile1[len(tile1) - 1][:]) or (row[::-1]
                                                 == tile1[len(tile1) - 1][:])


def match_puzzle_piece_in_any_orientation(piece, tile_array):
    for tile_id in tile_array:
        if tile_id != piece.id:
            up = tile_array[tile_id][0]
            bottom = tile_array[tile_id][9]
            left = [i[0] for i in tile_array[tile_id]]
            right = [i[9] for i in tile_array[tile_id]]
            if (match_d_all(tile_array[piece.id], up)
                    or match_d_all(tile_array[piece.id], bottom)
                    or match_d_all(tile_array[piece.id], right) or match_d_all(
                        tile_array[piece.id], left)) and piece.below is None:
                piece.match_count += 1
                assert piece.below is None
                piece.below = tile_id
            elif (match_u_all(tile_array[piece.id], up)
                  or match_u_all(tile_array[piece.id], bottom)
                  or match_u_all(tile_array[piece.id], right) or match_u_all(
                      tile_array[piece.id], left)) and piece.above is None:
                piece.match_count += 1
                assert piece.above is None
                piece.above = tile_id
            elif (match_l_all(tile_array[piece.id], up)
                  or match_l_all(tile_array[piece.id], bottom)
                  or match_l_all(tile_array[piece.id], right) or match_l_all(
                      tile_array[piece.id], left)) and piece.left is None:
                piece.match_count += 1
                assert piece.left is None
                piece.left = tile_id
            elif (match_r_all(tile_array[piece.id], up)
                  or match_r_all(tile_array[piece.id], bottom)
                  or match_r_all(tile_array[piece.id], right) or match_r_all(
                      tile_array[piece.id], left)) and piece.right is None:
                assert piece.right is None
                piece.right = tile_id
                piece.match_count += 1


def get_required_mutation(piece, tile_array):
    up = tile_array[piece.id][0]
    bottom = tile_array[piece.id][9]
    left = [i[0] for i in tile_array[piece.id]]
    right = [i[9] for i in tile_array[piece.id]]
    for tile_id in tile_array:
        if tile_id != piece.id:
            if (right == [i[9] for i in tile_array[tile_id]
                          ]) or (left == [i[0] for i in tile_array[tile_id]]):
                return hf

            if (up == tile_array[tile_id][0]) or (bottom
                                                  == tile_array[tile_id][9]):
                return vf

            # two topside or two bottomside matches
            if (up[::-1] == tile_array[tile_id][0]) or (
                    bottom[::-1]
                    == tile_array[tile_id][9]) or (right[::-1] == [
                        i[9] for i in tile_array[tile_id]
                    ]) or (left[::-1] == [i[0] for i in tile_array[tile_id]]):
                return rotate180

            if (left == tile_array[tile_id][0]) or (
                    right == tile_array[tile_id][9]) or (up[::-1] == [
                        i[9] for i in tile_array[tile_id]
                    ]) or (bottom[::-1] == [i[0]
                                            for i in tile_array[tile_id]]):
                return rotate270

            if (right[::-1] == tile_array[tile_id][0]) or (
                    left[::-1] == tile_array[tile_id][9]) or (bottom == [
                        i[9] for i in tile_array[tile_id]
                    ]) or (up == [i[0] for i in tile_array[tile_id]]):
                return rotate90

    return None


def match_puzzles(array_of_puzzle_pieces, tile_array):
    for piece in array_of_puzzle_pieces:
        match_puzzle_piece(piece, tile_array)


def populate_match_count(array_of_puzzle_pieces, tile_array):
    for piece in array_of_puzzle_pieces:
        match_puzzle_piece_in_any_orientation(array_of_puzzle_pieces[piece],
                                              tile_array)


def remove_tile_borders(tile_array):
    for tile_id in tile_array:
        tile_array[tile_id] = tile_array[tile_id][1:len(tile_array[tile_id]) -
                                                  1]
        tile_array[tile_id] = rotate90(tile_array[tile_id])
        tile_array[tile_id] = tile_array[tile_id][1:len(tile_array[tile_id]) -
                                                  1]
        tile_array[tile_id] = rotate270(tile_array[tile_id])


def extend_right(tile1, tile2):
    [tile1[i].extend(tile2[i]) for i in range(len(tile1))]


def extend_below(tile1, tile2):
    tile1.extend(tile2)


class PuzzlePiece:
    def __init__(self, piece_id):
        self.id = piece_id
        self.above = None
        self.below = None
        self.left = None
        self.right = None
        self.match_count = 0
        self.corner_piece = 0

    def __repr__(self):
        return f'Id:{self.id}, a:{self.above}, b:{self.below}, l:{self.left}, r:{self.right}'

    def get_score(self):
        return (int(self.above is not None) + int(self.below is not None) +
                int(self.left is not None) + int(self.right is not None) +
                self.corner_piece * 0.5)

    def __lt__(self, other):
        return self.get_score() < other.get_score()


tiles = {}
with open('aoc20_test.txt') as f:
    input_txt = f.readlines()

current_tile_no = None
current_line_no = 0
for line in input_txt:
    if "Tile " in line:
        current_tile_no = int(line[len("Tile "):len(line) - 2])
        tiles[current_tile_no] = list()
        tiles[current_tile_no].append([])
        current_line_no = 0
    elif line != "\n":
        for c in line[:10]:
            tiles[current_tile_no][current_line_no].append(c)
        current_line_no += 1
        tiles[current_tile_no].append(list())
    else:
        tiles[current_tile_no].pop()

tiles[current_tile_no].pop()
puzzle_dim = len(tiles)**0.5
assert puzzle_dim == int(puzzle_dim), "not a square"

puzzle_dim = int(puzzle_dim)
puzzle_solution = [[-1] * puzzle_dim] * puzzle_dim

puzzle_pieced = dict()

for tile_id in tiles.keys():
    puzzle_pieced[tile_id] = PuzzlePiece(tile_id)
    assert len(tiles[tile_id]) == len(
        tiles[tile_id][9]), f"not the same length"

possible_mutations = [
    rotate90, rotate90, rotate90, rotate90, hf, rotate90, rotate90, rotate90,
    rotate90, hf
]

possible_mass_mutations = [rotate90, vf, hf]
done = False
len_good_tiles = 0

populate_match_count(puzzle_pieced, tiles)

corner_pieces = list()
multip = 1
top_left_corner = None
for tile_id in puzzle_pieced:
    piece = puzzle_pieced[tile_id]
    #print(piece.match_count)
    if piece.match_count == 2:
        if piece.below is not None and piece.right is not None:
            top_left_corner = piece
        corner_pieces.append(piece.id)
        print(piece)
        multip *= piece.id
print(multip)

assert top_left_corner is not None
puzzle_matrix = list()
puzzle_dimension = int(sqrt(len(puzzle_pieced)))
assert puzzle_dimension**2 == len(puzzle_pieced)

next_piece = top_left_corner
for y in range(puzzle_dimension):
    puzzle_matrix.append(list())
    for x in range(puzzle_dimension):
        puzzle_matrix[y].append(next_piece.id)
        #print(next_piece)
        if y > 0:
            for mutate in possible_mutations:
                if match_u(tiles[next_piece.id],
                           tiles[puzzle_matrix[y - 1][x]]):
                    break
                tiles[next_piece.id] = mutate(tiles[next_piece.id])
            assert match_u(tiles[next_piece.id],
                           tiles[puzzle_matrix[y - 1][x]])
        if x > 0:
            for mutate in possible_mutations:
                if match_l(tiles[next_piece.id],
                           tiles[puzzle_matrix[y][x - 1]]):
                    break
                tiles[next_piece.id] = mutate(tiles[next_piece.id])
            assert match_l(tiles[next_piece.id],
                           tiles[puzzle_matrix[y][x - 1]])
        next_piece.above = None
        next_piece.below = None
        next_piece.left = None
        next_piece.right = None
        match_puzzle_piece_in_any_orientation(next_piece, tiles)
        #print(next_piece)
        if x + 1 < puzzle_dimension:
            next_piece = puzzle_pieced[next_piece.right]
    if y + 1 < puzzle_dimension:
        next_piece = puzzle_pieced[puzzle_pieced[puzzle_matrix[y][0]].below]

#print(puzzle_matrix)

# print(tiles[top_left_corner.id])
remove_tile_borders(tiles)
# print(tiles[top_left_corner.id])
master_tile = tiles[top_left_corner.id]
cur_piece = top_left_corner
for y in range(puzzle_dimension):
    for x in range(1, puzzle_dimension):
        cur_piece = puzzle_pieced[cur_piece.right]
        extend_right(master_tile, tiles[cur_piece.id])
    if y > 0:
        extend_below(tiles[top_left_corner.id], master_tile)
    if y + 1 < puzzle_dimension:
        cur_piece = puzzle_pieced[puzzle_pieced[puzzle_matrix[y][0]].below]
        master_tile = tiles[cur_piece.id]
q
# print(tiles[top_left_corner.id])
tiles[top_left_corner.id] = vf(tiles[top_left_corner.id])
picture = [''.join(txt) for txt in tiles[top_left_corner.id]]
sea_monster = [
    "                  # ", "#    ##    ##    ###", " #  #  #  #  #  #   "
]
print(picture)
no_of_hashes = 0
no_of_rough_seas = 0

for line_no, line in enumerate(picture):
    index = 0
    no_of_hashes += picture[line_no].count('#')
    while True:
        index_offset = line[index:].find(sea_monster[0])
        if index_offset < 0:
            break
        index += index_offset
        if sea_monster[1] == picture[line_no + 1][index:index +
                                                  len(sea_monster[1])]:
            if sea_monster[2] == picture[line_no + 1][index:index +
                                                      len(sea_monster[2])]:
                picture[line_no] = picture[line_no][:index:index] + picture[
                    line_no][index:index + len(sea_monster[0])].replace(
                        '#',
                        '0') + picture[line_no][index + len(sea_monster[0]):]

                picture[line_no +
                        1] = picture[line_no + 1][:index:index] + picture[
                            line_no +
                            1][index:index + len(sea_monster[1])].replace(
                                '#',
                                '0') + picture[line_no +
                                               1][index + len(sea_monster[1]):]

                picture[line_no +
                        2] = picture[line_no + 2][:index:index] + picture[
                            line_no +
                            2][index:index + len(sea_monster[2])].replace(
                                '#',
                                '0') + picture[line_no +
                                               2][index + len(sea_monster[2]):]
                break
    no_of_rough_seas += picture[line_no].count('#')

#2638 is too high
print(no_of_hashes)
print(no_of_rough_seas)
#sea_monster = [[character for character in txt] for txt in sea_monster]

exit(0)
puzzle_pieced = list()

for tile_id in tiles.keys():
    puzzle_pieced.append(PuzzlePiece(tile_id))
    # if tile_id in corner_pieces:
    #     puzzle_pieced[len(puzzle_pieced) - 1].corner_piece = 1
    assert len(tiles[tile_id]) == len(
        tiles[tile_id][9]), f"not the same length"

while not done:
    match_puzzles(puzzle_pieced, tiles)
    puzzle_pieced.sort()
    prev_len_good_tiles = len_good_tiles
    len_good_tiles = 0
    for piece in puzzle_pieced:
        if piece.get_score() > 2:
            len_good_tiles += 1
        elif piece.id in corner_pieces and piece.get_score() == 2:
            len_good_tiles += 1

    if len_good_tiles == 143:
        print(puzzle_pieced[piece_index].id)
    puzzle_pieced.sort()
    #print(len_good_tiles)
    piece_index = 0
    mass_mutate_index = 0
    tries = 0
    tile_score = puzzle_pieced[piece_index].get_score()
    if tile_score > 2:
        break
    if puzzle_pieced[piece_index].id in corner_pieces and tile_score == 2:
        puzzle_pieced[piece_index].corner_piece = 1
    while tile_score >= puzzle_pieced[piece_index].get_score():
        tile_idx = puzzle_pieced[piece_index].id
        required_mutation = get_required_mutation(puzzle_pieced[piece_index],
                                                  tiles)
        if required_mutation is not None and len_good_tiles != prev_len_good_tiles:
            tiles[tile_idx] = required_mutation(tiles[tile_idx])
            if len_good_tiles == 143:
                print(puzzle_pieced[piece_index])
                print(required_mutation)
                match_puzzles(puzzle_pieced, tiles)
                print(puzzle_pieced[piece_index])
                required_mutation = get_required_mutation(
                    puzzle_pieced[piece_index], tiles)
                #tiles[tile_idx] = required_mutation(tiles[tile_idx])
                print(required_mutation)
                #match_puzzles(puzzle_pieced, tiles)
                #print(puzzle_pieced[piece_index])
            else:
                break
            # if get_required_mutation(puzzle_pieced[piece_index],
            #                          tiles) is None:
            #     break
        for mutate in possible_mutations:
            tiles[tile_idx] = mutate(tiles[tile_idx])
            match_puzzle_piece(puzzle_pieced[piece_index], tiles)
            if tile_score < puzzle_pieced[piece_index].get_score():
                break
        tries += 1
        if tries == len(possible_mutations):
            tries = 0
            len_good_tiles = 0
            for piece in puzzle_pieced:
                if piece.get_score() > 2:
                    len_good_tiles += 1
            if len_good_tiles == 143:
                print(puzzle_pieced[piece_index])
            len_good_tiles = 0
            for piece in puzzle_pieced:
                if piece.get_score() > tile_score:
                    len_good_tiles += 1
                    tiles[
                        piece.id] = possible_mass_mutations[mass_mutate_index](
                            tiles[piece.id])
                elif piece.get_score == tile_score and randint(0, 10) > 7:
                    piece_index = piece.id
                    tile_score = puzzle_pieced[piece_index].get_score()
            mass_mutate_index = (mass_mutate_index +
                                 1) % len(possible_mass_mutations)
            if len_good_tiles == 143:
                print(puzzle_pieced[piece_index])
            print(mass_mutate_index)
            print(len_good_tiles)
match_puzzles(puzzle_pieced, tiles)
puzzle_pieced.sort()
print(puzzle_pieced)

multip = 1
for piece in puzzle_pieced:
    if piece.get_score() == 2.5:
        print(piece.id)
        multip *= piece.id

print(multip)

# for i in range(puzzle_dim):
#     start_idx = i * puzzle_dim
#     puzzle_solution.append([])
#     for id_idx in range(puzzle_dim):
#         puzzle_solution[i].append(list(tiles.keys())[start_idx + id_idx])

# print(tiles.keys())
# print(puzzle_solution)
