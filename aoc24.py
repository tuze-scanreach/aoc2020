with open('aoc24.txt') as f:
    input_txt = f.readlines()

valid_instructions = {
    "e": (1, 0),
    "se": (0.5, -0.5),
    "sw": (-0.5, -0.5),
    "w": (-1, 0),
    "ne": (0.5, 0.5),
    "nw": (-0.5, 0.5)
}


def get_no_black_neighbours(black_tiles_list, current_location):
    no_black_neighbours = 0
    for instruction in valid_instructions:
        neighbour_location = (current_location[0] +
                              valid_instructions[instruction][0],
                              current_location[1] +
                              valid_instructions[instruction][1])
        if neighbour_location in black_tiles_list:
            no_black_neighbours += 1
    return no_black_neighbours


flipped_tile_locations = set()
for instruction_set in input_txt:
    current_location = [0, 0]
    instruction_set = instruction_set.rstrip()
    instruction = ""
    for c in instruction_set:
        instruction += c
        if instruction in valid_instructions:
            current_location[0] += valid_instructions[instruction][0]
            current_location[1] += valid_instructions[instruction][1]
            instruction = ""
    current_location = tuple(current_location)
    if current_location in flipped_tile_locations:
        flipped_tile_locations.remove(current_location)
    else:
        flipped_tile_locations.add(current_location)

print(len(flipped_tile_locations))

no_days = 100
for day in range(no_days):
    new_flips = set()
    for location in flipped_tile_locations:
        no_black_neighbours = get_no_black_neighbours(flipped_tile_locations,
                                                      location)
        if (no_black_neighbours == 0 or no_black_neighbours > 2):
            new_flips.add(location)
        for instruction in valid_instructions:
            neighbour_location = (location[0] +
                                  valid_instructions[instruction][0],
                                  location[1] +
                                  valid_instructions[instruction][1])
            if neighbour_location in new_flips or neighbour_location in flipped_tile_locations:
                continue
            no_black_neighbours = get_no_black_neighbours(
                flipped_tile_locations, neighbour_location)
            if (no_black_neighbours == 2):
                new_flips.add(neighbour_location)
    for flip in new_flips:
        if flip in flipped_tile_locations:
            flipped_tile_locations.remove(flip)
        else:
            flipped_tile_locations.add(flip)

print(len(flipped_tile_locations))
