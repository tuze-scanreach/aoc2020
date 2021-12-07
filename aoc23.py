import time


def move_cups(cups, no_moves, min_cup_val, max_cup_val):
    for i in range(no_moves):
        cups_to_move = cups[1:4]
        cups_on_the_floor = [cups[0], *cups[4:]]
        dest_cup = cups[0] - 1
        while dest_cup not in cups_on_the_floor:
            dest_cup -= 1
            if dest_cup < min_cup_val:
                dest_cup = max_cup_val
        dest_cup_index = cups_on_the_floor.index(dest_cup)
        cups_on_the_floor[dest_cup_index + 1:dest_cup_index + 1] = cups_to_move
        cups_on_the_floor.append(cups_on_the_floor[0])
        cups = cups_on_the_floor[1:]
    return cups


class CupsLink:
    def __init__(self, prev_cup, next_cup):
        self.prev_cup = prev_cup
        self.next_cup = next_cup

    def update_next(self, next_cup):
        self.next_cup = next_cup

    def update_prev(self, prev_cup):
        self.prev_cup = prev_cup


def move_cups_ll(cups, no_moves, min_cup_val, max_cup_val):
    cups_ll = dict()
    prev_index = len(cups) - 1
    for i in range(len(cups)):
        cups_ll[cups[i]] = CupsLink(cups[prev_index],
                                    cups[(i + 1) % len(cups)])
        prev_index = i

    current_cup = cups[0]
    for i in range(no_moves):
        ctm = []
        ctm.append(cups_ll[current_cup].next_cup)
        ctm.append(cups_ll[ctm[0]].next_cup)
        ctm.append(cups_ll[ctm[1]].next_cup)
        cups_ll[current_cup].next_cup = cups_ll[ctm[2]].next_cup
        cups_ll[cups_ll[ctm[2]].next_cup].prev_cup = current_cup

        dc = current_cup - 1
        if dc < min_cup_val:
            dc = max_cup_val
        while dc in ctm:
            dc -= 1
            if dc < min_cup_val:
                dc = max_cup_val
        cups_ll[ctm[2]].next_cup = cups_ll[dc].next_cup
        cups_ll[cups_ll[dc].next_cup].prev_cup = ctm[2]
        cups_ll[dc].next_cup = ctm[0]
        current_cup = cups_ll[current_cup].next_cup
        if i % 1e6 == 0:
            print(i)

    return cups_ll


#cups = [3, 8, 9, 1, 2, 5, 4, 6, 7]
cups = [6, 5, 3, 4, 2, 7, 9, 1, 8]

min_cup_val = min(cups)
max_cup_val = max(cups)
# PART 1:
t1 = time.perf_counter_ns()
cups_shuffled = move_cups(cups, 999, min_cup_val, max_cup_val)
result1 = ""
index = (cups_shuffled.index(1) + 1) % len(cups_shuffled)
for _ in range(len(cups_shuffled) - 1):
    result1 += str(cups_shuffled[index])
    index = (index + 1) % len(cups_shuffled)
print(result1)
t2 = time.perf_counter_ns()
print(f"Part 1, method 1 took {t2 - t1} nanoseconds")

t1 = time.perf_counter_ns()
result2 = ""
cups_ll = move_cups_ll(cups, int(999), min_cup_val, max_cup_val)
prev_cup = 1
for _ in range(len(cups_ll) - 1):
    result2 += str(cups_ll[prev_cup].next_cup)
    prev_cup = cups_ll[prev_cup].next_cup
print(result2)
t2 = time.perf_counter_ns()
print(f"Part 1, method 2 took {t2 - t1} nanoseconds")

assert result1 == result2, "not equal"

# PART 2
for val in range(max_cup_val + 1, int(1e6) + 1):
    cups.append(val)
max_cup_val = max(cups)
assert min_cup_val == min(cups), "ooops"
assert max_cup_val == int(1e6), "ooops"

t1 = time.perf_counter_ns()
cups_ll = move_cups_ll(cups, int(10e6), min_cup_val, max_cup_val)

print(
    f"{cups_ll[1].next_cup} * {cups_ll[cups_ll[1].next_cup].next_cup} = {cups_ll[1].next_cup * cups_ll[cups_ll[1].next_cup].next_cup}"
)
t2 = time.perf_counter_ns()
print(f"Part 2, method 2 took {t2 - t1} nanoseconds")

# cups_shuffled = move_cups(cups, int(10e6), min_cup_val, max_cup_val)
# index = (cups_shuffled.index(1) + 1) % len(cups_shuffled)
# print(f"{cups_shuffled[index]} and {cups_shuffled[index+1]}")
