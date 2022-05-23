# Shlomi Ben-Shushan 311408264


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
