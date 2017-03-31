from random import randint

LIMIT = 1000
given_list = []
for x in range(LIMIT):
    given_list.append(randint(0, 5))

print("Generated List: ", given_list)

table = [[0 for x in range(6)] for y in range(6)]
prev = 0
for x in range(len(given_list)):
    table[prev][given_list[x]] += 1
    prev = given_list[x]

for x in range(len(table)):
    print(table[x])

