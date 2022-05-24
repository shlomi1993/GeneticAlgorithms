# Shlomi Ben-Shushan 311408264


from random import choice
from datetime import datetime
from src.utils import *
from src.optim import optimize
from src.stats import Statistics


def genetic_solver(game, generations, pop_size, elitism, crossover, optim=None):

    # Timer & Statistics
    start = datetime.now()
    game.stats = Statistics()

    # Composition of the new population
    n_elite = int(elitism * pop_size)
    n_newborns = int(crossover * pop_size)
    n_survivors = pop_size - n_elite - n_newborns

    # Population
    population = [Solution(game) for i in range(pop_size)]

    # Evolution
    best_solution = ''
    best_fitness = 0
    for g in range(1, generations + 1):

        # Gather information
        game.stats.generations += 1
        maximum, minimum, average = gather_info(population)
        game.stats.min_fitness.append(minimum)
        game.stats.max_fitness.append(maximum)
        game.stats.avg_fitness.append(average)

        # Show information
        if g % 10 == 0:
            average_str = str(average)
            if len(average_str.split('.')[1]) == 1:
                average_str += '0'
            print(f'Generation {g}:  '
                  f'Worst fitness: {minimum}  |  '
                  f'Average fitness: {average_str}  |  '
                  f'Best fitness: {maximum}  |  '
                  f'Chosen fitness: {best_fitness}  |  '
                  f'Fitness calls: {game.stats.fitness_calls}')

        # Optimization
        if optim == 'lamark':
            indexes = list(range(pop_size))
            shuffle(indexes)
            indexes = indexes[:int(0.5 * pop_size)]
            for i in indexes:
                population[i] = optimize(game, population[i])
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
            print(f'Generation {g}:  A legal solution has been found!')
            break
        if maximum == minimum:
            print(f'Generation {g}:  CONVERGED! Restart calculations...')
            game.stats.restarts += 1
            game.stats.min_fitness.clear()
            game.stats.max_fitness.clear()
            game.stats.avg_fitness.clear()
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

    game.stats.solution = best_solution
    game.stats.fitness = best_fitness
    game.stats.runtime = str(datetime.now() - start).split(".")[0]
    return game.stats
