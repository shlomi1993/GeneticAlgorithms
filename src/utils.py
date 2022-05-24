# Shlomi Ben-Shushan 311408264


from random import randint, shuffle, sample


class Solution:
    def __init__(self, game, array=None):
        if array:
            self.array = array
        else:
            self.array = [randint(1, game.dim) for _ in range(game.solution_size)]
        self.fitness = fitness(game, self.array)


def gather_info(population):
    total = 0
    maximum = 0
    minimum = float('inf')
    for s in population:
        total += s.fitness
        if s.fitness > maximum:
            maximum = s.fitness
        if s.fitness < minimum:
            minimum = s.fitness
    return maximum, minimum, round(total / len(population), 2)


def make_bias_array(population):
    bias_array = []
    for i, s in zip(range(len(population)), population):
        for j in range(s.fitness):
            bias_array.append(i)
    shuffle(bias_array)
    return bias_array


def mutate(game, solution):
    game.stats.mutate_calls += 1
    coin = randint(1, 3)
    if coin == 1:
        indexes = [i for i in range(len(solution))]
        i, j = sample(indexes, 2)
        array = solution.copy()
        temp = array[i]
        array[i] = array[j]
        array[j] = temp
    elif coin == 2:
        i = randint(1, len(solution) - 1)
        j = i - 1
        array = solution.copy()
        temp = array[i]
        array[i] = array[j]
        array[j] = temp
    else:
        array = solution.copy()
        array[randint(0, len(solution) - 1)] = randint(1, game.dim)
    return Solution(game, array)


def cross_over(game, solution1, solution2):
    game.stats.cross_over_calls += 1
    sep = randint(0, len(solution1) - 1)
    array = solution1[:sep] + solution2[sep:]
    return Solution(game, array)


def fitness(game, solution):
    game.stats.fitness_calls += 1
    game.set(solution)
    score = game.n_constraints
    for x in range(game.dim):
        for y in range(game.dim):
            v = game.matrix[x][y]
            for i in range(game.dim):
                if i != x and game.matrix[i][y] == v:
                    score -= 1
                    break
            for j in range(game.dim):
                if j != y and game.matrix[x][j] == v:
                    score -= 1
                    break
    for a, b, c, d in game.relations:
        if game.matrix[a][b] <= game.matrix[c][d]:
            score -= 1
    return score
