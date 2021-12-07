from collections import defaultdict
with open('aoc19.txt') as f:
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
                if rule == rule_no:
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

no_valid_messages = 0
valid_message_list = list()
for message in messages:
    rules_stack = list()
    branch_stack = list()
    current_rule = rulebook[0]
    current_rule_option = 0
    rule_index = 0
    message_parse_done = False
    # while not message_parse_done:
    c_idx = 0
    while c_idx < len(message) and not message_parse_done:
        c = message[c_idx]
        while type(current_rule[current_rule_option]) is tuple:
            if len(current_rule[current_rule_option]) > rule_index + 1:
                rules_stack.append(
                    (current_rule, current_rule_option, rule_index, c_idx))
            if len(current_rule) > current_rule_option + 1:
                branch_stack.append(
                    (current_rule, current_rule_option + 1, rule_index, c_idx))
            current_rule = rulebook[current_rule[current_rule_option]
                                    [rule_index]]
            rule_index = 0
            current_rule_option = 0
        if current_rule[0][0] == c:
            if c_idx + 1 == len(message):
                no_valid_messages += 1
                valid_message_list.append(message)
                message_parse_done = True
                break
            elif len(rules_stack) == 0:
                message_parse_done = True
                break
            else:
                while (len(rules_stack) > 0):
                    current_rule, current_rule_option, rule_index, stored_idx = rules_stack.pop(
                    )
                    if len(current_rule[current_rule_option]) > rule_index + 1:
                        break
                if len(current_rule[current_rule_option]) <= rule_index + 1:
                    message_parse_done = True
                    break
                rule_index += 1
        else:
            message_parse_done = True
            #rules_stack.clear()
            if len(branch_stack) != 0:
                current_rule, current_rule_option, rule_index, stored_idx = branch_stack.pop(
                )
                message_parse_done = False
                c_idx = stored_idx - 1
                rule_index = 0
            # while len(branch_stack) != 0:
            #     current_rule, current_rule_option, rule_index, stored_idx = branch_stack.pop(
            #     )
            #     if len(current_rule) > current_rule_option + 1:
            #         current_rule_option += 1
            #         message_parse_done = False
            #         c_idx = stored_idx - 1
            #         rule_index = 0
            #         break
        c_idx += 1

print(no_valid_messages)
print(valid_message_list)
# print(rulebook)
#print(messages)
