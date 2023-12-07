from sortedcontainers import SortedDict

cards = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    **{str(i): i for i in range(9, 1, -1)}
}

JOKER = 11

with open('07.txt', 'r') as in_file:
    sorted_hands_1 = SortedDict()
    sorted_hands_2 = SortedDict()
    for line in in_file:
        hand, score = line.split()
        card_counts = {JOKER: 0}
        card_counts_counts_1 = [0] * (len(hand) + 1)
        card_counts_counts_2 = [0] * (len(hand) + 1)
        ordered_hand_1 = []
        ordered_hand_2 = []
        for c in hand:
            if (idx := cards[c]) not in card_counts:
                card_counts[idx] = 0
            card_counts[idx] = new_count = card_counts[idx] + 1
            card_counts_counts_1[new_count] += 1
            card_counts_counts_1[new_count - 1] -= 1
            ordered_hand_1.append(idx)
            if idx == JOKER:
                ordered_hand_2.append(1)
            else:
                card_counts_counts_2[new_count] += 1
                card_counts_counts_2[new_count - 1] -= 1
                ordered_hand_2.append(idx)
        if jokers := card_counts[JOKER]:
            max_idx = max((0, *(i for i, x in enumerate(card_counts_counts_2) if x > 0)))
            card_counts_counts_2[max_idx + card_counts[JOKER]] += 1
            card_counts_counts_2[max_idx] -= 1
        hand_value = [0, 0]
        for i, ccc in enumerate((card_counts_counts_1, card_counts_counts_2)):
            match ccc:
                case [_, _, _, _, _, 1]:  # Five of a kind
                    hand_value[i] = 6
                case [_, _, _, _, 1, _]:  # Four of a kind
                    hand_value[i] = 5
                case [_, _, 1, 1, _, _]:  # Full house
                    hand_value[i] = 4
                case [_, _, _, 1, _, _]:  # Three of a kind
                    hand_value[i] = 3
                case [_, _, 2, _, _, _]:  # Two pair
                    hand_value[i] = 2
                case [_, _, 1, _, _, _]:  # One pair
                    hand_value[i] = 1
                case _:                   # High card
                    hand_value[i] = 0
        sorted_hands_1[(hand_value[0], *ordered_hand_1)] = score
        sorted_hands_2[(hand_value[1], *ordered_hand_2)] = score
    sum_1 = sum_2 = 0
    for i, (score_1, score_2) in enumerate(zip(sorted_hands_1.values(), sorted_hands_2.values())):
        sum_1 += int(score_1) * (i + 1)
        sum_2 += int(score_2) * (i + 1)

print(sum_1)
print(sum_2)
