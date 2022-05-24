# Shlomi Ben-Shushan 311408264


from random import shuffle, choice, randint
from src.utils import Solution


def create_truth_matrix(game, solution):
    game.set(solution.array)
    truth_matrix = []
    for x in range(game.dim):
        row = []
        for y in range(game.dim):
            v = game.matrix[x][y]
            not_satisfied = 0
            for i in range(game.dim):
                if i != x and game.matrix[i][y] == v:
                    not_satisfied += 1
                    break
            for j in range(game.dim):
                if j != y and game.matrix[x][j] == v:
                    not_satisfied += 1
                    break
            for a, b, c, d in game.relations:
                if (x, y) == (a, b) and game.matrix[x][y] <= game.matrix[c][d]:
                    not_satisfied += 1
                    break
            row.append(not_satisfied)
        truth_matrix.append(row)
    return truth_matrix


def find_unsatisfied_cells(game, solution):
    truth_matrix = create_truth_matrix(game, solution)
    unsatisfied_cells = []
    for x in range(game.dim):
        for y in range(game.dim):
            if truth_matrix[x][y] > 0:
                unsatisfied_cells.append((x, y, truth_matrix[x][y]))
    for i, j, v in unsatisfied_cells:
        if (i, j) in game.given.keys():
            unsatisfied_cells.remove((i, j, v))
    return unsatisfied_cells


def find_optimizations(game, cells, limit):
    indexes = list(range(len(cells)))
    shuffle(indexes)
    optimizations = []
    count = 0
    for idx in indexes:
        if count == limit:
            break
        x, y, t = cells[idx]
        v = game.matrix[x][y]
        allowed = [i + 1 for i in range(game.dim)]
        for i in range(game.dim):
            if i != x and game.matrix[i][y] in allowed:
                allowed.remove(game.matrix[i][y])
        for j in range(game.dim):
            if j != y and game.matrix[x][j] in allowed:
                allowed.remove(game.matrix[x][j])
        for a, b, c, d in game.relations:
            u = game.matrix[c][d]
            if (x, y) == (a, b) and v <= u:
                for av in allowed:
                    if av <= u:
                        allowed.remove(av)
        if len(allowed) > 0:
            optimizations.append((x, y, allowed, t))
            count += 1
    return optimizations


def optimize(game, solution):

    unsatisfied_cells = find_unsatisfied_cells(game, solution)
    if len(unsatisfied_cells) == 0:
        return solution

    # lim = 1 if game.dim < 6 else game.dim - 4  # maybe lim = game.dim is better ?
    lim = randint(1, game.dim)
    available_optimizations = find_optimizations(game, unsatisfied_cells, lim)
    if len(available_optimizations) == 0:
        return solution
    available_optimizations.sort(key=lambda tup: tup[3], reverse=True)

    array = solution.array.copy()
    for x, y, allowed_values, _ in available_optimizations:
        allowed = choice(allowed_values)
        k = 0
        broken = False
        for i in range(game.dim):
            if broken:
                break
            for j in range(game.dim):
                if (i, j) not in game.given.keys():
                    if (i, j) == (x, y):
                        array[k] = allowed
                        broken = True
                        break
                    k += 1

    return Solution(game, array)
