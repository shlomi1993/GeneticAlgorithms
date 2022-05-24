# Shlomi Ben-Shushan 311408264


from os.path import exists
from prettytable import PrettyTable
from futoshiki_game import Futoshiki
from futoshiki_solver import genetic_solver


STOPPED = 0
RUNNING = 1


HELP = 'Help message:\n' \
       '* For each field k you can set the value v by assigning k=v.' \
       ' e.g., g=1000.\n' \
       '* You must provide an input file in to the input field.\n' \
       '* The other fields are set to default values.\n' \
       '* Once the fields are set you can run the program by typing \'r\'.\n' \
       '* At any time you can view this help message by typing \'h\'.\n' \
       '* At any time you can end the program by typing \'q\'.'


class Command:
    def __init__(self, description, action):
        self.description = description
        self.action = action


class FutoshikiCli:

    def __init__(self):
        self.state = STOPPED
        self.game = None
        self.generations = 10000
        self.pop_size = 100
        self.elitism = 0.01
        self.crossover = 0.8
        self.mutate_prob = 0.05
        self.mutate_rate = 0.05
        self.optim = None
        self.commands = {
            'i': Command(
                description='Set the path to a game input file (REQUIRED).',
                action=self.__parse_game),
            'g': Command(
                description='Set the number of generations to run (a positive integer).',
                action=self.__set_generations),
            'p': Command(
                description='Set the size of solution population (a positive integer).',
                action=self.__set_pop_size),
            'e': Command(
                description='Set the percentage of elite solutions in the next generation (a fraction from 0 to 1).',
                action=self.__set_elitism),
            'c': Command(
                description='Set the percentage of newborns in the next generation (a fraction from 0 to 1).',
                action=self.__set_crossover),
            'mp': Command(
                description='Set the probability of a solution to be mutated (a fraction from 0 to 1).',
                action=self.__set_mutate_prob),
            'mr': Command(
                description='Set the mutation rate on a single solution (a fraction from 0 to 1).',
                action=self.__set_mutate_rate),
            'o': Command(
                description='Set an optimization method (\"Lamark\" or \"Darwin\").',
                action=self.__set_optim),
            'r': Command(
                description='Run genetic solution (input required)',
                action=None),
            'h': Command(
                description='Show this help message.',
                action=None),
            'q': Command(
                description='Finish the program.',
                action=None),
        }
        self.mapper = {
            'input': 'i',
            'generations': 'g',
            'population': 'p',
            'elitism': 'e',
            'crossover': 'c',
            'mutate_prob': 'mp',
            'mutate_rate': 'mr',
            'optimization': 'o',
            'run': 'r',
            'help': 'h',
            'quit': 'q'
        }
        self.inv_mapper = {self.mapper[k]: k for k in self.mapper.keys()}

    def __parse_game(self, input_file):
        if not exists(input_file):
            print('File not found. Please provide an input file.')
            return
        try:
            with open(input_file, 'r') as file:
                lines = file.readlines()
        except OSError:
            print('Could not read file.  Please provide a valid input file.')
            return
        offset = 0
        mat_size = int(lines[offset])
        offset += 1
        n_given = int(lines[offset])
        offset += 1
        given_digits = []
        for i in range(n_given):
            given_row = lines[offset].split(' ')
            given_tup = int(given_row[0]), int(given_row[1]), int(given_row[2])
            for x in given_tup:
                if x < 1 or x > mat_size:
                    print('Invalid input. Please provide a valid input file.')
                    return
            given_digits.append(given_tup)
            offset += 1
        n_relations = int(lines[offset])
        offset += 1
        relations = []
        for i in range(n_relations):
            relation_row = lines[offset].split(' ')
            relation_tup = (int(relation_row[0]), int(relation_row[1]),
                            int(relation_row[2]), int(relation_row[3]))
            for x in relation_tup:
                if x < 1 or x > mat_size:
                    print('Invalid input. Please provide a valid input file.')
                    return
            relations.append(relation_tup)
            offset += 1
        print('Game input file successfully parsed.')
        self.game = Futoshiki(mat_size, given_digits, relations)

    def __set_generations(self, x):
        try:
            xi = int(x)
            if xi < 1:
                raise ValueError
            self.generations = xi
            print(f'Generation parameter set to {xi}.')
        except ValueError:
            print('Number of generations should be a positive integer.')

    def __set_pop_size(self, x):
        try:
            xi = int(x)
            if xi < 1:
                raise ValueError
            self.pop_size = xi
            print(f'Population size parameter set to {xi}')
        except ValueError:
            print('Population size should be a positive integer')

    def __set_elitism(self, x):
        try:
            xf = float(x)
            if xf < 0 or xf > 1:
                raise ValueError
            self.elitism = xf
            print(f'Elitism parameter set to {xf}.')
        except ValueError:
            print('Elitism should be a float between 0 and 1.')

    def __set_crossover(self, x):
        try:
            xf = float(x)
            if xf < 0 or xf > 1:
                raise ValueError
            self.crossover = xf
            print(f'Cross-over parameter to {xf}.')
        except ValueError:
            print('Cross-over should be a float between 0 and 1.')

    def __set_mutate_prob(self, x):
        try:
            xf = float(x)
            if xf < 0 or xf > 1:
                raise ValueError
            self.mutate_prob = xf
            print(f'Mutation probability parameter to {xf}.')
        except ValueError:
            print('Mutation probability should be a float between 0 and 1.')

    def __set_mutate_rate(self, x):
        try:
            xf = float(x)
            if xf < 0 or xf > 1:
                raise ValueError
            self.mutate_rate = xf
            print(f'Mutation rate parameter to {xf}.')
        except ValueError:
            print('Mutation rate should be a float between 0 and 1.')

    def __set_optim(self, x):
        xl = x.lower()
        if xl == 'lamark' or xl == 'darwin':
            self.optim = xl
            print(f'{x} optimization set.')
        else:
            print('Optimization should be \"Lamark\" or \"Darwin\".')

    def __run(self):
        if self.game:
            stats = genetic_solver(game=self.game,
                                   generations=self.generations,
                                   pop_size=self.pop_size,
                                   elitism=self.elitism,
                                   crossover=self.crossover,
                                   optim=self.optim)
            correctness = self.game.validate(stats.solution)
            stats.print_stats(correctness, self.game.matrix)
        else:
            print('Error! Please provide an input file and then try again.')

    def __show_help(self):
        table = PrettyTable(['Field', 'Input'])
        table.add_row(['-----', '-----'])
        table.align = 'l'
        table.border = False
        for k in self.commands.keys():
            if k == 'r':
                table.add_row(['', ''])
                table.add_row(['Operator', 'Operation'])
                table.add_row(['--------', '---------'])
            table.add_row([f'{k}, {self.inv_mapper[k]}', self.commands[k].description])
        print(HELP, end='\n\n')
        print(table, end='\n\n')

    def __quit(self):
        self.state = STOPPED
        print('Good Bye! ☻')

    def mainloop(self):
        print('\u001b[1mFutoshiki Solver CLI App\u001b[0m')
        print('Solves Futoshiki games using a genetic algorithm')
        print()
        self.state = RUNNING
        self.__show_help()
        while self.state == RUNNING:
            args = input('\u001b[32;1m>>> \u001b[0m')
            if args == 'r' or args == 'run':
                self.__run()
                continue
            if args == 'h' or args == 'help' or args == '?':
                self.__show_help()
                continue
            if args == 'q' or args == 'quit':
                self.__quit()
                break
            args = args.split()
            for arg in args:
                kv = arg.split('=')
                if len(kv) != 2 or len(kv[0]) == 0 or len(kv[1]) == 0:
                    print('Invalid input. Use key=value pairs or and operator.')
                    break
                k, v = kv
                if k not in self.commands.keys() and k not in self.mapper.keys():
                    print('Invalid input. Type help for help message.')
                    break
                if k in self.mapper.keys():
                    k = self.mapper[k]
                self.commands[k].action(v)
