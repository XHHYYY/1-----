import random
txt = ''
m = 50
max_arrive = 0
for i in range(1, m+1):
        max_arrive = max_arrive + random.randint(1, 3)
        require_time = random.randint(1, 20)
        txt += '{} {} {}\n'.format(*list(map(str, [i, max_arrive, require_time])))
print(txt)
with open('./codes/sequence.txt', 'w') as f:
    f.write(txt)
