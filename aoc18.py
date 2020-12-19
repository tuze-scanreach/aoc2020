def execute_op(value1, value2, operation):
    if operation == '+':
        value1 += value2
    elif operation == '*':
        value1 *= value2
    else:
        assert False, f'operation is not a valid value {operation}'
    return value1


with open('aoc18.txt') as f:
    equations = f.readlines()

sum_of_all_results = 0
for eq in equations:
    result = 0
    stashed_results = list()
    stashed_ops = list()
    stashed_multiplications = list()
    stashed_multiplications_in_parantheses = list()
    next_op = '+'
    for op in eq:
        if op.isdigit():
            result = execute_op(result, int(op), next_op)
            next_op = None
        elif op == '(':
            stashed_ops.append(next_op)
            stashed_multiplications_in_parantheses.append(0)
            stashed_results.append(result)
            result = 0
            next_op = '+'
        elif op == ')':
            if (len(stashed_multiplications_in_parantheses) >= 1):
                no_multip_todo = stashed_multiplications_in_parantheses.pop()
                for i in range(no_multip_todo):
                    result *= int(stashed_multiplications.pop())
            next_op = stashed_ops.pop()
            result = execute_op(result, stashed_results.pop(), next_op)

            next_op = None
        elif op == '\n':
            for multip in stashed_multiplications:
                result *= int(multip)
            break
        elif op == ' ':
            continue
        elif op == '*':
            assert next_op is None, f'op is {op} but next_op already has a value, {next_op}'
            if (len(stashed_multiplications_in_parantheses) >= 1):

                stashed_multiplications_in_parantheses[
                    len(stashed_multiplications_in_parantheses) - 1] += 1

            stashed_multiplications.append(result)
            result = 0
            next_op = '+'
        else:
            assert next_op is None, f'op is {op} but next_op already has a value, {next_op}'
            next_op = op
    sum_of_all_results += result

print(sum_of_all_results)
