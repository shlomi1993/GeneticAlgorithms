# Shlomi Ben-Shushan 311408264


from random import random, randint, shuffle, sample, choice
from futoshiki_stats import Statistics


stats = Statistics()


class Solution:
    def __init__(self, game, array=None):
        if array:
            self.array = array
        else:
            self.array = [randint(1, game.dim) for j in range(game.sol_size)]
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


def mutate(game, solution, rate):
    global stats
    stats.mutate_calls += 1
    indexes = [i for i in range(len(solution))]
    chosen_indexes = sample(indexes, int(rate * len(solution)))
    array = solution.copy()
    for i in chosen_indexes:
        array[i] = randint(1, game.dim)
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
    start_fitness = solution.fitness
    array = solution.array.copy()
    i = randint(0, len(array) - 1)
    j = randint(1, game.dim)
    while array[i] == j:
        j = randint(1, game.dim)
    array[i] = j
    ns = Solution(game, array)
    if ns.fitness > start_fitness:
        return ns
    return solution


def genetic_solver(game, generations, pop_size, elitism, crossover, mutation,
                   optim=None):

    # Composition of the new population
    n_elite = int(elitism * pop_size)
    n_newborns = int(crossover * pop_size)
    n_survivors = pop_size - n_elite - n_newborns

    # Population
    population = [Solution(game) for i in range(pop_size)]

    # Statistics
    global stats
    stats = Statistics()
    stats.params = {
        'generations': generations,
        'population': pop_size,
        'elitism': elitism,
        'crossover': crossover,
        'mutation_prob': mutation[1],
        'mutation_rate': mutation[0],
        'optimization': optim
    }
    min_since_converged = []

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
        min_since_converged.append(minimum)

        # Optimization
        # if optim == 'lamark':
        #     tuples = [optimize(game, s) for s in population]
        # elif optim == 'darwin':
        #     darwin_tuples = [optimize(game, s) for s in population]
        #     darwin_chosen = max(darwin_tuples, key=lambda tup: tup[1])
        #     if chosen[1] < darwin_chosen[1]:
        #         chosen = deepcopy(darwin_chosen)

        # Sort solutions according to fitness and mark chosen one.
        population.sort(key=lambda _s: _s.fitness, reverse=True)
        if best_fitness < population[0].fitness:
            best_solution = population[0].array.copy()
            best_fitness = population[0].fitness

        # Show information
        if g % 10 == 0:
            print(f'Generation {g}: '
                  f'Worst fitness: {minimum} | '
                  f'Average fitness: {average} | '
                  f'Best fitness: {maximum} | '
                  f'Chosen fitness: {best_fitness} | '
                  f'Fitness calls: {stats.fitness_calls}')

        # Convergence test and handling
        if best_fitness == game.n_constraints:
            print(f'Generation {g}: A legal solution has been found!')
            break
        if maximum == minimum:
            print(f'Generation {g}: CONVERGED! Restart calculations...')
            stats.restarts += 1
            min_since_converged.clear()
            population = [Solution(game) for i in range(pop_size)]
            continue

        # Make bias array
        bias_array = []
        for i, sol in zip(range(len(population)), population):
            for j in range(sol.fitness):
                bias_array.append(i)
        shuffle(bias_array)

        # Elitism
        elites = [sol for sol in population[:n_elite]]

        # Cross-over
        newborns = []
        trials = 0
        while len(newborns) < n_newborns:
            i, j = sample(bias_array, 2)
            s = cross_over(game, population[i].array, population[j].array)
            trials += 1
            if s.fitness > max(min_since_converged) or trials == 100:
                trials = 0
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
            m = mutate(game, s.array, 0.05)
            # if m.fitness > s.fitness:
            mutated.append(m)
            # else:
            #     mutated.append(s)

        # Create next generation
        population = elites + mutated

    stats.solution = best_solution
    stats.fitness = best_fitness
    return stats


def calibrate(game):
    elitism = [0.0, 0.01, 0.03, 0.05]
    crossover = [i * 0.1 for i in range(1, 10)]
    mutation = [(r, p * 0.01) for r in [0.05, 0.10] for p in range(1, 20, 2)]
    optim = [None, 'lamark', 'darwin']
    params = []
    for a in elitism:
        for b in crossover:
            for c in mutation:
                for d in optim:
                    st = genetic_solver(game, 3000, 100, a, b, c, d)
                    params.append(st)

    best = max(params, key=lambda s: s.fitness)
    corr = True if best.fitness == 58 else False
    best.print_stats(corr, game.matrix)
    return best


def debug():
    from futoshiki_game import Futoshiki
    game = Futoshiki(mat_size=5,
                     given_digits=[(1, 2, 4), (3, 3, 2)],
                     relations=[(1, 1, 1, 2), (1, 4, 2, 4), (2, 2, 2, 3),
                                (3, 4, 4, 4), (4, 5, 3, 5), (4, 4, 5, 4),
                                (5, 5, 4, 5), (5, 2, 5, 1)])

    st = genetic_solver(game=game,
                        generations=10000,
                        pop_size=100,
                        elitism=0.01,
                        crossover=1.0,
                        mutation=('err', 0.05),  # tuple of (rate, prob)
                        optim='')

    print(st.solution)
    print(f'Validation: {game.validate(st.solution)}, fitness: {st.fitness}')

    true_solution = [5, 1, 2, 3, 2, 5, 3, 1, 4, 4, 3, 5, 1, 3, 1, 5, 4, 2, 1, 2, 4, 3, 5]
    print(f'Validation: {game.validate(true_solution)}, fitness: {fitness(game, true_solution)}')


debug()
