# Shlomi Ben-Shushan 311408264


from prettytable import PrettyTable
from matplotlib import pyplot as plt


class Statistics:

    def __init__(self):
        self.solution = None
        self.fitness = 0
        self.runtime = 0
        self.max_fitness = []
        self.avg_fitness = []
        self.min_fitness = []
        self.fitness_calls = 0
        self.mutate_calls = 0
        self.cross_over_calls = 0
        self.restarts = 0
        self.generations = 0
        self.params = {}

    def print_stats(self, correctness, solution):
        print()
        stats = PrettyTable(['Item', 'Value(s)'])
        stats.align = 'l'
        solution_str = ''
        for row in solution:
            solution_str += f'{row}\n'
        stats.add_row(['Solution:', solution_str[:-1]])
        stats.add_row(['Correctness:', correctness])
        stats.add_row(['Sol. Fitness:', self.fitness])
        stats.add_row(['Avg. Fitness:', self.avg_fitness[-1]])
        stats.add_row(['Runtime:', self.runtime])
        stats.add_row(['Generations:', self.generations])
        stats.add_row(['Fitness Calls:', self.fitness_calls])
        stats.add_row(['Mutate Calls:', self.mutate_calls])
        stats.add_row(['X-Over Calls:', self.cross_over_calls])
        stats.add_row(['Restarts:', self.restarts])
        print(stats, end='\n\n')
        params = PrettyTable(['Parameter', 'Value'])
        params.align = 'l'
        for k in self.params.keys():
            params.add_row([f'{k}:', self.params[k]])
        print(params, end='\n\n')

    def plot(self):
        plt.figure()
        title = 'Fitness per generation\n'
        title += f'Attempt: {self.restarts + 1} | '
        title += f'Fitness calls: {self.fitness_calls} | '
        title += f'Runtime: {str(self.runtime).split(".")[0]}'
        plt.title(title)
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        x = list(range(len(self.min_fitness)))
        plt.plot(x, self.min_fitness, label='Minimal fitness')
        plt.plot(x, self.max_fitness, label='Maximal fitness')
        plt.plot(x, self.avg_fitness, label='Average fitness')
        plt.legend()
        plt.show()

    def reset(self):
        self.solution = None
        self.fitness = 0
        self.runtime = 0
        self.max_fitness.clear()
        self.avg_fitness.clear()
        self.min_fitness.clear()
        self.fitness_calls = 0
        self.mutate_calls = 0
        self.cross_over_calls = 0
        self.restarts = 0
        self.generations = 0
        self.params.clear()

