def count_paths(begin_point, end_point):
    return count_all([(begin_point, '')], end_point)


def count_all(begin_points, end_point):
    ended_num = 0
    next_points = []
    for point, last_step in begin_points:
        if point == end_point:
            ended_num += 1
        else:
            next_points += move_step(point, last_step, end_point)
    if next_points:
        return ended_num + count_all(next_points, end_point)
    return ended_num


def move_step(begin_point, last_step, end_point):
    next_points = []
    for direction in ['u', 'r', 'd']:
        if not (direction == 'r' and last_step == 'u' or direction == 'u' and last_step == 'r'):
            new_point = move_direction(begin_point, direction)
            if new_point[0] <= end_point[0] and new_point[1] <= end_point[1]:
                next_points.append((new_point, direction))
    return next_points


def move_direction(begin_point, direction):
    x, y = begin_point
    if direction == 'u':
        return x, y + 1
    if direction == 'r':
        return x + 1, y
    return x + 1, y + 1

