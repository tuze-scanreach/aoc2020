from collections import defaultdict
# with open('aoc19.txt') as f:
with open('aoc19-p2test.txt') as f:
    input_txt = f.read().splitlines()

# input_txt = """0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"

# ababbb
# ababbababab
# bababa
# abbbab
# aaabbb
# aaaabbb
# """.splitlines()

rulebook = defaultdict(list)
messages = list()
for line in input_txt:
    if ":" in line:
        rule_no = int(line.split(': ')[0])
        rules = line.split(': ')[1].split(' ')
        rule_desc = list()
        for rule in rules:
            if rule.isdecimal():
                if int(rule) == rule_no:
                    rule = -1
                rule_desc.append(int(rule))
            elif rule == "|":
                rulebook[rule_no].append(tuple(rule_desc))
                rule_desc.clear()
            else:
                rulebook[rule_no].append(rule[1])
        if len(rule_desc) > 0:
            rulebook[rule_no].append(tuple(rule_desc))
    elif line == "":
        continue
    else:
        messages.append(line)

print(f"{rulebook[11]}, {rulebook[11][1][1] == -1}")
print(f"{rulebook[8]}, {rulebook[8][1][1] == -1}")


def validate_repeater(message, current_rule, no_repetitions):
    rule_idx = 0
    found_precond = 0
    found_postcond = -1
    valid_chars = 0
    while True:
        if valid_chars >= len(message):
            new_valid_chars = 0
        else:
            new_valid_chars = validate_message(
                message[valid_chars:], rulebook[current_rule[0][rule_idx]])
        if new_valid_chars > 0:
            if rule_idx == 0:
                found_precond += 1
                if no_repetitions == found_precond + 1:
                    if len(current_rule[0]) == 3:
                        rule_idx = 2
                        found_postcond = 0
                    else:
                        return valid_chars + new_valid_chars

            else:
                found_postcond += 1
                if no_repetitions == found_postcond:
                    return valid_chars + new_valid_chars
            valid_chars += new_valid_chars
            new_valid_chars = 0
        elif (found_precond + 1) == no_repetitions and rule_idx == 0 and len(
                current_rule[0]) == 3:
            rule_idx = 2
            found_postcond = 0
        elif (found_postcond == (found_precond + 1)) or (
            (found_precond + 1 >= no_repetitions) and (found_postcond == -1)):
            return valid_chars
        else:
            return 0


#314 is too low
#442 is too high
def validate_message(message, current_rule):
    if len(current_rule) > 1:
        for rule in current_rule:
            valid_chars = validate_message(message, [rule])
            if valid_chars > 0:
                return valid_chars
        return 0
    elif type(current_rule[0]) is tuple:
        valid_chars = 0
        # if -1 in current_rule[0]:
        #     print(current_rule)
        for rule_no in current_rule[0]:
            if len(message) <= valid_chars:
                return 0
            # if -1 in current_rule[0]:
            #     print(rule_no)
            #     print(current_rule)
            if rule_no == -1:
                #print(current_rule)
                for i in range(2, 10):
                    new_valid_chars = validate_repeater(
                        message[valid_chars:], current_rule, 10 - i)
                    if new_valid_chars > 0:
                        print(f"Validated {message} at {i}")
                        return valid_chars + new_valid_chars

                return 0
            else:
                new_valid_chars = validate_message(message[valid_chars:],
                                                   rulebook[rule_no])
                if new_valid_chars > 0:
                    valid_chars += new_valid_chars
                else:
                    return 0
        return valid_chars
    elif current_rule[0] == message[0]:
        return 1
    else:
        return 0


no_valid_messages = 0
valid_message_list = list()
for message in messages:
    current_rule = rulebook[0]
    current_rule_option = 0
    if validate_message(message, current_rule) == len(message):
        no_valid_messages += 1
        valid_message_list.append(message)

print(no_valid_messages)
#print(valid_message_list)
# print(rulebook)
#print(messages)
