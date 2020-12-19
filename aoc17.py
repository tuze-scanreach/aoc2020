from cellular_automaton import *
from typing import Sequence
from math import ceil

with open('aoc17.txt') as f:
    INIT_STATE = f.readlines()

Y_LEN = len(INIT_STATE)
X_LEN = len(INIT_STATE[Y_LEN - 1])
MAX_SIZE = 35
CENTRE_COORD = ceil(MAX_SIZE / 2)
ALIVE = '#'
DEAD = '.'


def is_in_centre(coordinate):
    x_is_centre = (coordinate[0] <=
                   (CENTRE_COORD + int(ceil(X_LEN / 2) - 1))) and (
                       coordinate[0] >= (CENTRE_COORD - (int(X_LEN / 2))))
    y_is_centre = (coordinate[1] <=
                   (CENTRE_COORD + int(ceil(Y_LEN / 2) - 1))) and (
                       coordinate[1] >= (CENTRE_COORD - (int(Y_LEN / 2))))

    z_is_centre = coordinate[2] == CENTRE_COORD
    w_is_centre = coordinate[3] == CENTRE_COORD

    return (x_is_centre and y_is_centre and z_is_centre and w_is_centre)


class MyCellularAutomaton(CellularAutomaton):
    def init_cell_state(self, coordinate: tuple) -> Sequence:
        if is_in_centre(coordinate):
            return INIT_STATE[coordinate[1] - (CENTRE_COORD - int(Y_LEN / 2))][
                coordinate[0] - (CENTRE_COORD - int(X_LEN / 2))]
        return DEAD

    def evolve_rule(self, last_cell_state: tuple,
                    neighbors_last_states: Sequence) -> Sequence:
        new_cell_state = last_cell_state
        alive_neighbours = self.__count_alive_neighbours(neighbors_last_states)
        if last_cell_state == DEAD:
            if alive_neighbours == 3:
                new_cell_state = ALIVE
        else:
            if alive_neighbours < 2 or alive_neighbours > 3:
                new_cell_state = DEAD
            else:
                new_cell_state = ALIVE
        #print(new_cell_state)
        return new_cell_state

    @staticmethod
    def __count_alive_neighbours(neighbours):
        alive_neighbors = []
        for n in neighbours:
            if n == ALIVE:
                alive_neighbors.append(1)
        return len(alive_neighbors)

    def count_alive_cells(self, state):
        no_alive_cells = 0
        for cell in list(state.values()):
            if cell.state == ALIVE:
                no_alive_cells += 1
        return no_alive_cells


neighborhood = MooreNeighborhood(EdgeRule.IGNORE_EDGE_CELLS)
ca = MyCellularAutomaton(dimension=[MAX_SIZE, MAX_SIZE, MAX_SIZE, MAX_SIZE],
                         neighborhood=neighborhood)
ca.evolve(6)
print(ca.count_alive_cells(ca._current_state))
