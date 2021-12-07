def get_key(sub_no, loop_size):
    key = 1
    for _ in range(loop_size):
        key = (key * sub_no) % 20201227
    return key


#key1 = 5764801
key1 = 1717001
#key2 = 17807724
key2 = 523731
subject_number = 7

key = 1
for loop1 in range(1, int(1e9)):
    key = (key * subject_number) % 20201227
    if key1 == key:
        break
print(loop1)

key = 1
for loop2 in range(1, int(1e9)):
    key = (key * subject_number) % 20201227
    if key2 == key:
        break
print(loop2)

enc_key1 = get_key(key2, loop1)
enc_key2 = get_key(key1, loop2)

print(f"{enc_key1} - {enc_key2}")