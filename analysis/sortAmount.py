data = []
for i in range(6, 11):
    with open('AmountStatis' + str(i), 'r') as f:
        data.extend(list(map(lambda x: int(float(x)), f.readlines())))
data.sort()
with open('AmountSort', 'w') as f:
    f.writelines(list(map(lambda x: str(x) + '\n', data)))