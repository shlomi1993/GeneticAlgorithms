# GeneticAlgorithms

Computational Biology - Assignment 2
Solved by: Shlomi Ben-Shushan (ID: 311408264).

## Description

In this ReadMe file, I will describe the programmatic implementation of a Genetic Algorithm that solves boards of Futoshiki game. Then, I will instruct the usage of a CLI-App I have implemented to test this algorithm.

## Requirements

There are no unique requirements to run the executable file (.exe).

But if there is a need to run the source code of the program, then the following requirements must be met first:
1. Please make sure that Python 3 is installed in your machine. The program was written using Python version 3.10 but was also tested on Python 3.8.
2. Use install the packages 'prettytable', 'matplotlib', and 'keyboard', using pip or any other python package manager.

## Instructions

### Starting the program

If you are using the executable, just double click on it (or execute it via terminal) and the program will start.
If you want to run the source code, make sure the requirements above met, and then navigate to the programs's main directory (where app.py file is located), and run the command "python app.py".

### Using the program

After the program starts a command-line interface console will appear on the screen and through this console you can operate the genetic algorithm Futoshiki game solver.

The commands you can insert to the console are divided to two types:

1. **Field-assignment** -- Write pairs of key and values to set the value of a key parameter using '=' character. For example, to set the experiment number of generations to 1000, you can insert the command 'generations=1000', or shortly 'g=1000'.

All fields except the input file field are filled with the following default values as follows:
Generations:     5000
Population size: 100
Elitism:         0.01
Cross-over:      0.8
Optimization:    None
Plot:            False

2. **Operators** -- Insert single-word operator to make the program do something, such as show the corrent program settings by inserting the command 'show', or shortly 's'.

There is a special operator 'run' or 'r' that not only run the algorithm in an attempt to find a solution, but also can be combined with field-assignments. For example, the command 'run input=easy5.txt o=lamark g=1234' will load the file easy5.txt, use lamark optimization, set the number of generations to 1234, and then run the solver.

The following table provides information about the avilable field-assignment and operators:

 Field            Input
 -----            -----
 i, input         Set the path to a game input file (REQUIRED).
 g, generations   Set the number of generations to run.
 p, population    Set the size of the population.
 e, elitism       Set the percentage of elites in the next generation.
 c, crossover     Set the percentage of newborns in the next generation.
 o, optimization  Set an optimization method ("Lamark", "Darwin" or "None").
 f, figure        Show figure in the end of the experiment (assign "true" or "false").

 Operator         Operation
 --------         ---------
 r, run           Run genetic solution (input required)
 s, settings      Show current parameters.
 h, help          Show this help message.
 q, quit          Finish the program.

To show this table in the app, simply type 'help', 'h' or '?'.


## Notes

1. 