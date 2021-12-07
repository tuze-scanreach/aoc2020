from copy import deepcopy
rules = {}
unrolled_rule_keys = list()


def has_numbers(inputString):
    for char in inputString.split(';'):
        if char.isdigit():
            return True
    return False


def unroll_rules(rules):
    with open('result.txt', 'w') as f:
        while len(unrolled_rule_keys) != len(rules):
            for rule in rules:
                if rule not in unrolled_rule_keys:
                    f.write("Rule " + str(rule) + "\n")
                    f.write("Before: ")
                    f.write(str(rules[rule]) + '\n')
                    for known_rule in unrolled_rule_keys:
                        known_rule_w_delimiters = ';' + known_rule + ';'
                        if type(rules[known_rule]) is list:
                            new_rules = list()
                            for val_combo in rules[rule]:
                                if known_rule_w_delimiters in val_combo:
                                    for rule_opt in rules[known_rule]:
                                        new_rules.append(
                                            val_combo.replace(
                                                known_rule_w_delimiters,
                                                rule_opt))
                                else:
                                    new_rules.append(val_combo)
                            rules[rule] = deepcopy(new_rules)
                        else:
                            rules[rule] = [
                                val_combo.replace(known_rule_w_delimiters,
                                                  rules[known_rule])
                                for val_combo in rules[rule]
                            ]
                    f.write("After: ")
                    f.write(str(rules[rule]) + "\n\n")
                    # if len(unrolled_rule_keys) == (len(rules) - 1):
                    #     unrolled_rule_keys.append(rule)
                    #     break
                    if not any(has_numbers(s) for s in rules[rule]):
                        unrolled_rule_keys.append(rule)
            #if last_print_count == len(unrolled_rule_keys):
            #    last_print_count += 1


def has_numbers2(inputString):
    for char in inputString:
        if char.isdigit():
            return True
    return False


with open('aoc19.txt') as f:
    input_txt = f.readlines()

for index, rule in enumerate(input_txt):
    rule_array = rule.rstrip().split(' ')
    #print(rule_array)
    rule_no = rule_array[0][:len(rule_array[0]) - 1]
    if len(rule_array) <= 1:
        break
    elif '"' in rule_array[1]:
        rules[rule_no] = rule_array[1][1]
        unrolled_rule_keys.append(rule_no)
    else:
        rules[rule_no] = list()

        rules[rule_no].append('')
        for no in rule_array[1:]:
            if no == '|':
                rules[rule_no].append('')
            else:
                rules[rule_no][len(rules[rule_no]) - 1] += ';' + no + ';'

unroll_rules(rules)

length_of_valid_str = len(rules['0'][0])
for s in rules['0']:
    assert length_of_valid_str == len(s), "Not all strings are same length"
    assert not has_numbers(s), 'oops'

print("unroll done")

print(length_of_valid_str)
print(len(rules['0']))
print(input_txt[len(input_txt) - 1])

txt_found = list()
no_valid_entries = 0
for i in range(index, len(input_txt)):
    txt_to_check = input_txt[i].rstrip()
    if len(txt_to_check) != length_of_valid_str:
        continue

    if txt_to_check in rules['0']:
        no_valid_entries += 1

print("done")
print(no_valid_entries)