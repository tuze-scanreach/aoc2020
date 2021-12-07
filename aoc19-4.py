from collections import defaultdict
import re
with open('aoc19-p2.txt') as f:
    #with open('aoc19-p2test.txt') as f:
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
                # if int(rule) == rule_no:
                #     rule = -1
                rule_desc.append(int(rule))
            elif rule == "|":
                rulebook[rule_no].append(tuple(rule_desc))
                rule_desc.clear()
            else:
                rulebook[rule_no] = rule[1]
        if len(rule_desc) > 0:
            rulebook[rule_no].append(tuple(rule_desc))
    elif line == "":
        continue
    else:
        messages.append(line)

for i in range(2, 10):
    rulebook[11].append(
        tuple([rulebook[11][1][0]] * i + [rulebook[11][1][2]] * i))
    rulebook[8].append(tuple([rulebook[8][1][0]] * i))
rulebook[11].remove(rulebook[11][1])
rulebook[8].remove(rulebook[8][1])


#314 is too low
#442 is too high
def validate_message(message, current_rule):
    results = []
    if len(current_rule) > 1:
        for rule in current_rule:
            valid_chars = validate_message(message, [rule])
            for chars in valid_chars:
                results.append(chars)
        return results
    elif type(current_rule[0]) is tuple:
        valid_chars = [0]
        for rule_no in current_rule[0]:
            new_valid_chars = []
            for i, chars in enumerate(valid_chars):
                if len(message) <= chars:
                    valid_chars[i] = len(message) + 1
                    continue
                new_valid_chars.extend(
                    validate_message(message[chars:], rulebook[rule_no]))
            incremented_valid_chars = list()
            for chars in new_valid_chars:
                incremented_valid_chars.extend(
                    [x + chars for x in valid_chars])
            valid_chars = incremented_valid_chars
        return valid_chars
    elif current_rule[0] == message[0]:
        return [1]
    else:
        return []


def build_regexp(rules, rule=0):
    rule = rules[rule]
    if type(rule) is str:
        return rule

    options = []
    for option in rule:
        option = ''.join(build_regexp(rules, r) for r in option)
        options.append(option)

    return '(' + '|'.join(options) + ')'


no_valid_messages = 0
no_valid_regex = 0
valid_message_list = list()
rexp = re.compile('^' + build_regexp(rulebook) + '$')

for message in messages:
    current_rule = rulebook[0]
    current_rule_option = 0

    if len(message) in validate_message(message, current_rule):
        no_valid_messages += 1
        valid_message_list.append(message)
    if rexp.match(message):
        no_valid_regex += 1

print(no_valid_regex)
print(no_valid_messages)
