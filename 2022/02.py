ROCK = 0
PAPER = 1
SCISSORS = 2
DRAW = 0
WIN = 1
LOSS = 2

labels_part1 = {
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS,
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS
}

labels_part2 = {
    'X': LOSS,
    'Y': DRAW,
    'Z': WIN,
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS
}

move_score = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

result_score = {
    LOSS: 0,
    DRAW: 3,
    WIN: 6
}

total_score_part1 = total_score_part2 = 0
with open('02.txt', 'r') as in_file:
    for line in in_file.read().split('\n'):
        if len(line) == 0:
            continue
        opp, player = (labels_part1[x] for x in line.split(' '))
        result = (player - opp) % 3
        total_score_part1 += move_score[player] + result_score[result]
        opp, result = (labels_part2[x] for x in line.split(' '))
        player = (opp + result) % 3
        total_score_part2 += move_score[player] + result_score[result]

print(total_score_part1)
print(total_score_part2)
