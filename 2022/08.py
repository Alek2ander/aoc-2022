with open('08.txt', 'r') as in_file:
    arr = [line for line in in_file.read().split('\n') if len(line) > 0]

h, w = len(arr), len(arr[0])
counter_part1 = 0
max_part2 = 0
vision = {(x, y): {'n': 0, 's': 0, 'e': 0, 'w': 0, 'v': 0} for x in range(w) for y in range(h)}

for y in range(h):
    height_indices = {}
    for x in range(w):
        blocked = -1
        for key in height_indices:
            if key >= arr[x][y] and height_indices[key] > blocked:
                blocked = height_indices[key]
        height_indices[arr[x][y]] = x
        if blocked == -1:
            vision[x, y]['v'] = 1
            blocked = 0
        vision[x, y]['w'] = x - blocked
    height_indices = {}
    for x in range(w - 1, -1, -1):
        blocked = w
        for key in height_indices:
            if key >= arr[x][y] and height_indices[key] < blocked:
                blocked = height_indices[key]
        height_indices[arr[x][y]] = x
        if blocked == w:
            vision[x, y]['v'] = 1
            blocked = w - 1
        vision[x, y]['e'] = blocked - x
for x in range(w):
    height_indices = {}
    for y in range(h):
        blocked = -1
        for key in height_indices:
            if key >= arr[x][y] and height_indices[key] > blocked:
                blocked = height_indices[key]
        height_indices[arr[x][y]] = y
        if blocked == -1:
            vision[x, y]['v'] = 1
            blocked = 0
        vision[x, y]['n'] = y - blocked
    height_indices = {}
    for y in range(w - 1, -1, -1):
        blocked = h
        for key in height_indices:
            if key >= arr[x][y] and height_indices[key] < blocked:
                blocked = height_indices[key]
        height_indices[arr[x][y]] = y
        if blocked == h:
            vision[x, y]['v'] = 1
            blocked = h - 1
        vision[x, y]['s'] = blocked - y

        counter_part1 += vision[x, y]['v']
        if (p := vision[x, y]['n'] * vision[x, y]['s'] * vision[x, y]['e'] * vision[x, y]['w']) > max_part2:
            max_part2 = p

print(counter_part1)
print(max_part2)
