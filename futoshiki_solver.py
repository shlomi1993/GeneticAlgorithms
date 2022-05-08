# Shlomi Ben-Shushan 311408264


from random import randint, shuffle
from matplotlib import pyplot as plt


class Futoshiki:

    def __init__(self, mat_size, given_digits, relations):
        self.dim = mat_size
        self.matrix = [[0 for j in range(mat_size)] for i in range(mat_size)]
        self.given_digits = {}
        for (i1, j1, v) in given_digits:
            i, j = i1 - 1, j1 - 1
            self.given_digits[(i, j)] = v
            self.matrix[i][j] = v
        self.sol_size = mat_size * mat_size - len(given_digits)
        self.relations = [(a - 1, b - 1, c - 1, d - 1) for (a, b, c, d) in relations]

    def set(self, solution):
        k = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) not in self.given_digits.keys():
                    self.matrix[i][j] = solution[k]
                    k += 1

    def validate(self, solution):
        self.set(solution)
        for x in range(self.dim):
            for y in range(self.dim):
                v = self.matrix[x][y]
                for i in range(self.dim):
                    if i != x and self.matrix[i][y] == v:
                        return False
                for j in range(self.dim):
                    if j != y and self.matrix[x][j] == v:
                        return False
                for i1, j1, i2, j2 in self.relations:
                    if (x, y) == (i1, j1) and self.matrix[x][y] <= self.matrix[i2][j2]:
                        return False
        return True

    def reset(self):
        dim = len(self.matrix)
        for i in range(dim):
            for j in range(dim):
                if (i, j) not in self.given_digits.keys():
                    self.matrix[i][j] = 0


def mutate(solution, rate, dim):
    indexes = [i for i in range(len(solution))]
    shuffle(indexes)
    indexes = indexes[:int(rate * len(solution))]
    for i in indexes:
        solution[i] = randint(1, dim)
    return solution


def cross_over(solution1, solution2):
    sep = randint(0, len(solution1) - 1)
    co1 = solution1[:sep] + solution2[sep:]
    co2 = solution2[:sep] + solution1[sep:]
    return co1, co2


def check(game, x, y):
    v = game.matrix[x][y]
    for i in range(game.dim):
        if i != x and game.matrix[i][y] == v:
            return False
    for j in range(game.dim):
        if j != y and game.matrix[x][j] == v:
            return False
    for i1, j1, i2, j2 in game.relations:
        if (x, y) == (i1, j1) and game.matrix[x][y] <= game.matrix[i2][j2]:
            return False
    return True


def fitness(game, solution):
    game.set(solution)
    score = 0
    for x in range(game.dim):
        for y in range(game.dim):
            v = game.matrix[x][y]
            score += 2
            for i in range(game.dim):
                if i != x and game.matrix[i][y] == v:
                    score -= 1
                    break
            for j in range(game.dim):
                if j != y and game.matrix[x][j] == v:
                    score -= 1
                    break
    for a, b, c, d in game.relations:
        if game.matrix[a][b] > game.matrix[c][d]:
            score += 2
    return score


def genetic_solver(game, generations, pop_size, mut_rate, pco, threshold):

    population = []
    for i in range(pop_size):
        population.append([randint(1, game.dim) for j in range(game.sol_size)])
    min_fitness = []
    avg_fitness = []
    max_fitness = []
    fitness_calls = 0
    highest_score = game.dim * game.dim * 2 + len(game.relations) * 2

    n_good = int(pco * len(population)) - 1
    if n_good % 2 == 1:
        n_good -= 1
    n_bad = len(population) - n_good - 1

    elite = None
    for g in range(generations):

        # Calculate fitness
        fitness_values = [fitness(game, s) for s in population]
        minimum = min(fitness_values)
        average = sum(fitness_values) / len(population)
        maximum = max(fitness_values)
        min_fitness.append(minimum)
        avg_fitness.append(average)
        max_fitness.append(maximum)
        fitness_calls += len(population)

        # Tuple togather each solution and its fitness value.
        population_f = [(s, f) for s, f in zip(population, fitness_values)]

        # Divide solutions
        population_f.sort(key=lambda tup: tup[1], reverse=True)
        elite = population_f[0][0]
        good = [s[0] for s in population_f[1:n_good + 1]]

        # Convergence test
        if maximum == highest_score or maximum - minimum < threshold:
            print(maximum - minimum, '<', threshold)
            break


        # Cross-over
        shuffle(good)
        group1, group2 = good[0::2], good[1::2]
        new_solutions = []
        while len(new_solutions) < n_bad:
            i, j = randint(0, len(group1) - 1), randint(0, len(group1) - 1)
            s, _ = cross_over(group1[i], group2[j])
            new_solutions.append(s)

        # Mutate
        temp = good + new_solutions
        population = [mutate(s, mut_rate, game.dim) for s in temp] + [elite]

    plt.figure()
    plt.title('Fitness per generation')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')

    x = list(range(len(min_fitness)))
    plt.plot(x, min_fitness, label='Minimal fitness')
    plt.plot(x, max_fitness, label='Maximal fitness')
    plt.plot(x, avg_fitness, label='Average fitness')
    plt.legend()
    plt.show()

    return elite, fitness_calls


def calibrate(game):
    generations = list(range(10, 1000, 10))
    pop_sizes = list(range(10, 500, 10))
    mut_percents = [i * 0.05 for i in range(20)]
    mut_rate = mut_percents.copy()
    co_percents = mut_percents.copy()
    thresholds = [i * 0.05 for i in range(20)]
    params = []
    for a in generations:
        for b in pop_sizes:
            for c in mut_percents:
                for d in mut_rate:
                    for e in co_percents:
                        for f in thresholds:
                            _, fitness_calls = genetic_solver(game, a, b, c, d, e, f)
                            params.append(((a, b, c, d, e, f), fitness_calls))
    return min(params, key=lambda tup: tup[1])[0]


def handle_convergence(game, generations, pop_size, p_mut, r_mut, p_co, threshold):
    solutions = []
    for i in range(10):
        s, f = genetic_solver(game, generations, pop_size, p_mut, r_mut, p_co, threshold)
        solutions.append((s, f))
    return min(solutions, key=lambda tup: tup[1])[0]


def main():
    game = Futoshiki(mat_size=5,
                     given_digits=[(1, 2, 4),
                                   (3, 3, 2)],
                     relations=[(1, 1, 1, 2),
                                (1, 4, 2, 4),
                                (2, 2, 2, 3),
                                (3, 4, 4, 4),
                                (4, 5, 3, 5),
                                (4, 4, 5, 4),
                                (5, 5, 4, 5),
                                (5, 2, 5, 1)])

    s, f = genetic_solver(game=game,
                          generations=300,
                          pop_size=100,
                          mut_rate=0.05,
                          pco=0.05,
                          threshold=1)


    print(s)
    print(f'Validation: {game.validate(s)}, fitness: {fitness(game, s)}')

    true_solution = [5, 1, 2, 3, 2, 5, 3, 1, 4, 4, 3, 5, 1, 3, 1, 5, 4, 2, 1, 2, 4, 3, 5]
    print(f'Validation: {game.validate(true_solution)}, fitness: {fitness(game, true_solution)}')


if __name__ == '__main__':
    main()
