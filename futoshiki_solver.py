# Shlomi Ben-Shushan 311408264


from random import randint, shuffle, sample, choice
from datetime import datetime
from futoshiki_stats import Statistics


stats = Statistics()


class Solution:
    def __init__(self, game, array=None):
        if array:
            self.array = array
        else:
            self.array = [randint(1, game.dim) for _ in range(game.sol_size)]
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
    global stats
    stats.mutate_calls += 1

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
    global stats
    stats.cross_over_calls += 1
    sep = randint(0, len(solution1) - 1)
    array = solution1[:sep] + solution2[sep:]
    return Solution(game, array)


def fitness(game, solution):
    global stats
    stats.fitness_calls += 1
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


def optimize(game, solution):

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

    not_satisfied_val = 0
    not_satisfied_cells = []
    for x in range(game.dim):
        for y in range(game.dim):
            if truth_matrix[x][y] == not_satisfied_val:
                not_satisfied_cells.append((x, y, truth_matrix[x][y]))
            if truth_matrix[x][y] > not_satisfied_val:
                not_satisfied_val = truth_matrix[x][y]
                not_satisfied_cells.clear()
                not_satisfied_cells.append((x, y, truth_matrix[x][y]))

    for i, j, v in not_satisfied_cells:
        if (i, j) in game.given_digits.keys():
            not_satisfied_cells.remove((i, j, v))

    if len(not_satisfied_cells) == 0:
        return solution

    x, y, v = choice(not_satisfied_cells)

    allowed_values = [i for i in range(game.dim)]
    for i in range(game.dim):
        if i != x and game.matrix[i][y] in allowed_values:
            allowed_values.remove(game.matrix[i][y])
    for j in range(game.dim):
        if j != y and game.matrix[x][j] in allowed_values:
            allowed_values.remove(game.matrix[x][j])
    for a, b, c, d in game.relations:
        u = game.matrix[c][d]
        if (x, y) == (a, b) and v <= u:
            for allowed in allowed_values:
                if allowed <= u:
                    allowed_values.remove(allowed)

    if len(allowed_values) == 0:
        return Solution(game)

    allowed = choice(allowed_values)

    array = solution.array.copy()
    k = 0
    for i in range(game.dim):
        for j in range(game.dim):
            if (i, j) not in game.given_digits.keys():
                if (x, y) == (i, j):
                    array[k] = allowed
                k += 1

    return Solution(game, array)


def genetic_solver(game, generations, pop_size, elitism, crossover, optim=None):

    # Timer
    start = datetime.now()

    # Composition of the new population
    n_elite = int(elitism * pop_size)
    n_newborns = int(crossover * pop_size)
    n_survivors = pop_size - n_elite - n_newborns

    # Statistics
    global stats
    stats.reset()
    stats.params = {
        'generations': generations,
        'population': pop_size,
        'elitism': elitism,
        'crossover': crossover,
        'optimization': optim
    }

    # Population
    population = [Solution(game) for i in range(pop_size)]

    # Evolution
    best_solution = ''
    best_fitness = 0
    for g in range(1, generations + 1):

        # Gather information
        stats.generations += 1
        maximum, minimum, average = gather_info(population)
        stats.min_fitness.append(minimum)
        stats.max_fitness.append(maximum)
        stats.avg_fitness.append(average)

        # Show information
        if g % 10 == 0:
            average_str = str(average)
            if len(average_str.split('.')[1]) == 1:
                average_str += '0'
            print(f'Generation {g}:  \t'
                  f'Worst fitness: {minimum}  |  '
                  f'Average fitness: {average_str}  |  '
                  f'Best fitness: {maximum}  |  '
                  f'Chosen fitness: {best_fitness}  |  '
                  f'Fitness calls: {stats.fitness_calls}')

        # Optimization
        if optim == 'lamark':
            population = [optimize(game, s) for s in population]
        elif optim == 'darwin':
            darwin_population = [optimize(game, s) for s in population]
            darwin = max(darwin_population, key=lambda s: s.fitness)
            if best_fitness < darwin.fitness:
                best_solution = darwin.array.copy()
                best_fitness = darwin.fitness

        # Sort solutions and mark the best one.
        population.sort(key=lambda s: s.fitness, reverse=True)
        if best_fitness < population[0].fitness:
            best_solution = population[0].array.copy()
            best_fitness = population[0].fitness

        # Convergence handling
        if best_fitness == game.n_constraints:
            print(f'Generation {g}:  \tA legal solution has been found!')
            break
        if maximum == minimum:
            print(f'Generation {g}:  \tCONVERGED! Restart calculations...')
            stats.restarts += 1
            stats.min_fitness.clear()
            stats.max_fitness.clear()
            stats.avg_fitness.clear()
            for i in range(pop_size):
                population[i] = Solution(game)
            continue

        # Bias Selection
        bias_array = make_bias_array(population)

        # Elitism
        elites = [sol for sol in population[:n_elite]]

        # Cross-over
        newborns = []
        while len(newborns) < n_newborns:
            i, j = sample(bias_array, 2)
            s = cross_over(game, population[i].array, population[j].array)
            newborns.append(s)

        # Replication
        survivors = []
        while len(survivors) < n_survivors:
            i = choice(bias_array)
            survivors.append(population[i])
            bias_array = list(filter(lambda k: k != i, bias_array))

        # Mutation
        non_elites = survivors + newborns
        mutated = []
        for s in non_elites:
            m = mutate(game, s.array)
            mutated.append(m if m.fitness > s.fitness else s)

        # Create next generation
        population = elites + mutated

    stats.solution = best_solution
    stats.fitness = best_fitness
    stats.runtime = datetime.now() - start
    stats.plot()
    return stats


# def calibrate(game):
#     elitism = [0.0, 0.01, 0.03, 0.05]
#     crossover = [i * 0.1 for i in range(1, 10)]
#     # optim = [None, 'lamark', 'darwin']
#     params = []
#     for a in elitism:
#         for b in crossover:
#             try:
#                 st = genetic_solver(game, 100000, 100, a, b)
#                 params.append(st)
#             except Exception:
#                 pass
#     best1 = min(params, key=lambda s: s.fitness)
#     best2 = min(params, key=lambda s: s.generations)
#     corr1 = True if best1.fitness == 58 else False
#     corr2 = True if best2.fitness == 58 else False
#     best1.print_stats(corr1, game.matrix)
#     best2.print_stats(corr2, game.matrix)
#     return best1


# def parallel_search(game, generations, pop_size, elitism, crossover, optim=None):
#     pros = []
#     for i in range(5):
#         print('Thread Started')
#         p = Process(target=genetic_solver, args=(game, generations, pop_size,
#                                                  elitism, crossover))
#         pros.append(p)
#         p.start()
#
#     for t in pros:
#         t.join()


# def debug():
#     from futoshiki_game import Futoshiki
#     game = Futoshiki(mat_size=5,
#                      given_digits=[(1, 2, 4), (3, 3, 2)],
#                      relations=[(1, 1, 1, 2), (1, 4, 2, 4), (2, 2, 2, 3),
#                                 (3, 4, 4, 4), (4, 5, 3, 5), (4, 4, 5, 4),
#                                 (5, 5, 4, 5), (5, 2, 5, 1)])
#
#     st = genetic_solver(game=game, generations=100000, pop_size=100,
#                         elitism=0.01, crossover=0.8, optim='Lamark')
#
#     print(st.solution)
#     print(f'Validation: {game.validate(st.solution)}, fitness: {st.fitness}')
#
#     true_solution = [5, 1, 2, 3, 2, 5, 3, 1, 4, 4, 3, 5, 1, 3, 1, 5, 4, 2, 1, 2, 4, 3, 5]
#     print(f'Validation: {game.validate(true_solution)}, fitness: {fitness(game, true_solution)}')
#     # calibrate(game)
#
#
# debug()
