from collections import Counter


def find_non_repeating(s, n):
    counter = Counter(s[:n])
    for i, l in enumerate(s[n:]):
        if len(counter) == n:
            return i + n
        else:
            if l not in counter:
                counter[l] = 0
            counter[l] += 1
            if counter[s[i]] == 1:
                del counter[s[i]]
            else:
                counter[s[i]] -= 1
    return None


with open('06.txt', 'r') as in_file:
    s = in_file.read()
    print(find_non_repeating(s, 4))
    print(find_non_repeating(s, 14))
