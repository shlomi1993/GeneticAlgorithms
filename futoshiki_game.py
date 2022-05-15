# # Shlomi Ben-Shushan 311408264
#
#
# from random import shuffle, choice, randint
# from copy import deepcopy
#
# class Futoshiki:
#
#     def __init__(self, mat_size, given_digits, relations):
#         self.dim = mat_size
#         self.matrix = [[0 for j in range(mat_size)] for i in range(mat_size)]
#         self.given_digits = {(i - 1, j - 1): v for i, j, v in given_digits}
#         for i, j in self.given_digits.keys():
#             self.matrix[i][j] = self.given_digits[(i, j)]
#         self.sol_size = mat_size * mat_size - len(given_digits)
#         self.relations = [(a - 1, b - 1, c - 1, d - 1) for (a, b, c, d) in relations]
#         self.n_constraints = 2 * (mat_size * mat_size - len(given_digits)) + len(relations)
#
#     def set(self, solution):
#         k = 0
#         for i in range(self.dim):
#             for j in range(self.dim):
#                 if (i, j) not in self.given_digits.keys():
#                     self.matrix[i][j] = solution[k]
#                     k += 1
#
#     def validate(self, solution):
#         self.set(solution)
#         for x in range(self.dim):
#             for y in range(self.dim):
#                 v = self.matrix[x][y]
#                 for i in range(self.dim):
#                     if i != x and self.matrix[i][y] == v:
#                         return False
#                 for j in range(self.dim):
#                     if j != y and self.matrix[x][j] == v:
#                         return False
#                 for a, b, c, d in self.relations:
#                     if (x, y) == (a, b) and self.matrix[x][y] <= self.matrix[c][d]:
#                         return False
#         return True
#
#     def reset(self):
#         for i in range(self.dim):
#             for j in range(self.dim):
#                 if (i, j) not in self.given_digits.keys():
#                     self.matrix[i][j] = 0
#
#
# def create_futoshiki(dim, n_given, n_relations):
#     matrix = [[0 for j in range(dim)] for i in range(dim)]
#     for i in range(dim):
#         for j in range(dim):
#             allowed = list(range(1, dim + 1))
#             for ii in range(dim):
#                 if matrix[ii][j] in allowed:
#                     idx = allowed.index(matrix[ii][j])
#                     del allowed[idx]
#             for jj in range(dim):
#                 if matrix[i][jj] in allowed:
#                     idx = allowed.index(matrix[i][jj])
#                     del allowed[idx]
#             n = choice(allowed)
#             matrix[i][j] = n
#     solution = deepcopy(matrix)
#
#     relations = []
#     while len(relations) < n_relations:
#         i, j = randint(0, dim - 1), randint(0, dim - 1)
#         potentials = []
#         try:
#             if matrix[i + 1][j] > matrix[i][j]:
#                 potentials.append((i + 1, j))
#         except IndexError:
#             pass
#         try:
#             if matrix[i - 1][j] > matrix[i][j]:
#                 potentials.append((i - 1, j))
#         except IndexError:
#             pass
#         try:
#             if matrix[i][j + 1] > matrix[i][j]:
#                 potentials.append((i, j + 1))
#         except IndexError:
#             pass
#         try:
#             if matrix[i][j - 1] > matrix[i][j]:
#                 potentials.append((i, j - 1))
#         except IndexError:
#             pass
#         if len(potentials) > 0:
#             idx = randint(0, len(potentials) - 1)
#             (x, y) = potentials[idx]
#             relations.append((x, y, i, j))
#
#     # allowed = [list(range(1, dim + 1)) for i in range(dim)]
#     # matrix = []
#     # for i in range(dim):
#     #     row = []
#     #     for j in range(dim):
#     #         k = randint(0, len(allowed[j]) - 1)
#     #         row.append(allowed[j][k])
#     #         del allowed[j][k]
#     #     matrix.append(row)
#     for r in matrix:
#         print(r)
#     print(relations)
#
# create_futoshiki(3, 2, 2)
