# Shlomi Ben-Shushan 311408264


from random import random, randint, shuffle, sample, choice
from copy import deepcopy
from matplotlib import pyplot as plt

fitness_calls = 0


class Futoshiki:

    def __init__(self, mat_size, given_digits, relations):
        self.dim = mat_size
        self.matrix = [[0 for j in range(mat_size)] for i in range(mat_size)]
        self.given_digits = {(i - 1, j - 1): v for i, j, v in given_digits}
        for i, j in self.given_digits.keys():
            self.matrix[i][j] = self.given_digits[(i, j)]
        self.sol_size = mat_size * mat_size - len(given_digits)
        self.relations = [(a - 1, b - 1, c - 1, d - 1) for (a, b, c, d) in relations]
        self.n_constraints = 2 * mat_size * mat_size + len(relations)

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
                for a, b, c, d in self.relations:
                    if (x, y) == (a, b) and self.matrix[x][y] <= self.matrix[c][d]:
                        return False
        return True

    def reset(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if (i, j) not in self.given_digits.keys():
                    self.matrix[i][j] = 0


def mutate(solution, rate, dim):
    indexes = [i for i in range(len(solution))]
    chosen = sample(indexes, int(rate * len(solution)))
    for i in chosen:
        solution[i] = randint(1, dim)
    return solution


def cross_over(solution1, solution2):
    sep = randint(0, len(solution1) - 1)
    return solution1[:sep] + solution2[sep:]


def fitness(game, solution):
    global fitness_calls
    fitness_calls += 1
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


def genetic_solver(game, generations, pop_size, elitism, crossover, mutation):

    # Composition of the new population
    n_elite = int(elitism * pop_size)
    n_newborns = int(crossover * pop_size)
    n_survivors = pop_size - n_elite - n_newborns

    # Population
    population = []
    for i in range(pop_size):
        population.append([randint(1, game.dim) for j in range(game.sol_size)])

    # Statistics
    min_fitness = []
    avg_fitness = []
    max_fitness = []
    min_since_converged = []
    global fitness_calls
    fitness_calls = 0

    # Evolution
    chosen = None
    for g in range(1, generations + 1):

        # Evaluation
        fitness_values = [fitness(game, s) for s in population]
        maximum = max(fitness_values)
        minimum = min(fitness_values)
        average = sum(fitness_values) / pop_size
        min_fitness.append(minimum)
        min_since_converged.append(minimum)
        max_fitness.append(maximum)
        avg_fitness.append(average)
        if g % 10 == 0:
            print(f'Generation {g}: Best fitness: {maximum} | Worst fitness: '
                  f'{minimum} | Average fitness: {average} | Fitness calls: '
                  f'{fitness_calls}')

        # Sort solutions according to fitness and mark chosen one.
        tuples = [(s, f) for s, f in zip(population, fitness_values)]
        tuples.sort(key=lambda tup: tup[1], reverse=True)
        chosen = deepcopy(tuples[0])

        # Convergence test and handling
        if maximum == game.n_constraints:
            break
        if maximum == minimum:
            print('CONVERGED!')
            min_since_converged.clear()
            indexes = sample(list(range(1, pop_size)), int(0.75 * pop_size))
            for i in indexes:
                ns = [randint(1, game.dim) for j in range(game.sol_size)]
                tuples[i] = (ns, fitness(game, ns))

        # Make bias array
        bias_array = []
        for i, (s, f) in zip(range(len(tuples)), tuples):
            for j in range(f):
                bias_array.append(i)
        shuffle(bias_array)

        # Elitism
        elites = [s.copy() for s, f in tuples[:n_elite]]

        # Cross-over
        newborns = []
        while len(newborns) < n_newborns:
            i, j = sample(bias_array, 2)
            (si, fi), (sj, fj) = tuples[i], tuples[j]
            s = cross_over(si, sj)
            f = fitness(game, s)
            if maximum == minimum or f > max(min_since_converged):
                newborns.append((s, f))

        # Replication
        survivors = []
        while len(survivors) < n_survivors:
            i = choice(bias_array)
            survivors.append(tuples[i])
            bias_array = list(filter(lambda k: k != i, bias_array))

        # Mutation
        non_elites = survivors + newborns
        mutated = []
        for s, fs in non_elites:
            m = mutate(s.copy(), mutation[0], game.dim)
            if fitness(game, m) > fs:
                mutated.append(m)
            else:
                mutated.append(m if random() < mutation[1] else s)

        # Create next generation
        population = elites + mutated

    # Plot
    # plt.figure()
    # plt.title('Fitness per generation')
    # plt.xlabel('Generation')
    # plt.ylabel('Fitness')
    # x = list(range(len(min_fitness)))
    # plt.plot(x, min_fitness, label='Minimal fitness')
    # plt.plot(x, max_fitness, label='Maximal fitness')
    # plt.plot(x, avg_fitness, label='Average fitness')
    # plt.legend()
    # plt.show()

    return chosen


def calibrate(game):
    elitism = [0.0, 0.01, 0.03, 0.05]
    crossover = [i * 0.1 for i in range(1, 10)]
    mutation = [(r, p * 0.01) for r in [0.05, 0.10] for p in range(1, 20, 2)]
    params = []
    for a in elitism:
        for b in crossover:
            for c in mutation:
                s, f = genetic_solver(game, 10000, 100, a, b, c)
                params.append(((a, b, c), f))
    return max(params, key=lambda tup: tup[1])


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
                          generations=10000,
                          pop_size=100,
                          elitism=0.01,
                          crossover=0.8,
                          mutation=(0.05, 0.05))  # tuple of (rate, prob)

    print(s)
    print(f'Validation: {game.validate(s)}, fitness: {fitness(game, s)}')

    true_solution = [5, 1, 2, 3, 2, 5, 3, 1, 4, 4, 3, 5, 1, 3, 1, 5, 4, 2, 1, 2, 4, 3, 5]
    print(f'Validation: {game.validate(true_solution)}, fitness: {fitness(game, true_solution)}')


    # print(calibrate(game))


if __name__ == '__main__':
    main()
