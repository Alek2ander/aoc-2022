ASCENDING = 0
DESCENDING = 1
NO_REMOVE = 0
REMOVE_LEFT = 1
REMOVE_RIGHT = 2

def is_safe_value(last, cur, direction):
    if last is None or cur is None:
        return True
    if ((cur < last and direction == ASCENDING) or (cur > last and direction == DESCENDING)
            or cur == last or cur > last + 3 or cur < last - 3):
        return False
    return True

with (open('02.txt', 'r') as in_file):
    safe_lines = dampener_lines = 0
    for line in in_file.readlines():
        left_value = mid_value = None
        fully_safe = [True, True]
        dampener_safe = [True, True]
        dampener_zone = [NO_REMOVE, NO_REMOVE]
        dampener_used = [False, False]
        for i, right_value in enumerate((*map(int, line.split()), None)):
            for direction in (ASCENDING, DESCENDING):
                if not dampener_safe[direction]:
                    continue
                if dampener_zone[direction] == NO_REMOVE and is_safe_value(mid_value, right_value, direction):
                    continue
                fully_safe[direction] = False
                if dampener_used[direction]:
                    dampener_safe[direction] = False
                    continue
                if dampener_zone[direction] == NO_REMOVE:
                    if is_safe_value(left_value, right_value, direction):
                        dampener_zone[direction] = REMOVE_LEFT  # value left of the error can be removed
                    else:
                        dampener_zone[direction] = REMOVE_RIGHT # only the value right of the error can be removed
                    continue
                else:
                    if not is_safe_value(left_value, right_value, direction) and (   # if we can safely remove the right value - always safe
                            dampener_zone[direction] == REMOVE_RIGHT or (            # if we can't but can only remove the right value - sequence can't be made safe by 1 removal
                            dampener_zone[direction] == REMOVE_LEFT
                            and not is_safe_value(mid_value, right_value, direction) # if we can remove the left value - safe only if the next step is safe
                            )):
                        dampener_safe[direction] = False
                        continue
                    dampener_used[direction] = True
                    dampener_zone[direction] = NO_REMOVE
            if not any(dampener_safe):
                break
            left_value, mid_value = mid_value, right_value
        if any(fully_safe):
            safe_lines += 1
        if any(dampener_safe):
            dampener_lines += 1

print(safe_lines)
print(dampener_lines)