import numpy as np
import itertools


class LinearCode:
    def __init__(self, A):
        self.matrix = np.copy(A)

    def __str__(self):
        return np.array2string(self.matrix)


def REF(m):
    matrix = np.copy(m)
    matrix_size = np.shape(matrix)
    k = 0
    for j in range(0, matrix_size[1]):
        for i in range(1 + k, matrix_size[0]):
            if matrix[i][j] == 1:
                if matrix[k][j] == 0:
                    change(matrix, i, k,'row')
                else:
                    matrix[i] ^= matrix[k]
        if k < (matrix_size[0]) and matrix[k][j] == 1:
            k += 1

    for i in reversed(range(matrix_size[0])):
        if np.sum(matrix[i]) == 0:
            matrix = np.delete(matrix, i, axis=0)
    return matrix


def RREF(m):
    matrix = np.copy(m)
    matrix_size = np.shape(matrix)
    for i in range(matrix_size[0]):
        for j in range(matrix_size[1]):
            if matrix[i][j] == 1:
                for k in range(i):
                    if matrix[k][j] == 1:
                        matrix[k] ^= matrix[i]
                break
    return matrix


def check(m):
    matrix = np.copy(m)

    lead = np.array([], dtype=int)
    matrix_size = np.shape(matrix)
    for i in range(matrix_size[0]):
        for j in range(matrix_size[1]):
            if matrix[i][j] == 1:
                lead = np.append(lead, j)
                break
    # print(f"Result:\nlead = {lead}")

    matrix = np.delete(matrix, lead, axis=1)
    matrix_size = np.shape(matrix)
    print(f"Result:\nX = \n{matrix}")

    I = np.eye(matrix_size[1], dtype=int)
    for i, row in zip(lead, matrix):
        I = np.insert(I, i, row, axis=0)
    return I


def Код_слова1(matrix):
    res = np.copy(matrix)
    res = np.insert(res, 0, np.zeros(matrix.shape[1], dtype=int), axis=0)
    n_old = 0
    while n_old != len(res):
        n_old = len(res)
        for i in range(n_old):
            for j in range(i + 1, n_old):
                res = np.vstack((res, res[i] ^ res[j]))
        res = np.unique(res, axis=0)
    return res


def Код_слова2(matrix):
    buff = [0, 1]
    res = list(itertools.product(buff, repeat=matrix.shape[0]))
    res2 = []
    for i in res:
        res2.append(i @ matrix % 2)
    return np.unique(res2, axis=0)


def Дистанс(matrix):
    matrix_size = np.shape(matrix)
    d = matrix_size[1]
    for i in range(0, matrix_size[0] - 1):
        for j in range(i + 1, matrix_size[0]):
            temp = np.sum(matrix[i] ^ matrix[j])
            if temp < d:
                d = temp
    return d, d - 1


def has_error(row):
    if np.any(row):
        print(f"{row}   -   error")
    else:
        print(f"{row}   -   no error")


def change(A, x, y, axis):
    if axis == 'row':
        A[[x, y], :] = A[[y, x], :]
    if axis == 'column':
        A[:, [x, y]] = A[:, [y, x]]


def main():
    a = np.array([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, ],
                  [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, ],
                  [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, ],
                  [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, ],
                  [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, ],
                  [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, ]])
    S = LinearCode(a)
    # print(f"Input:\nS =\n{S}")

    #   S
    S.matrix = REF(S.matrix)
    print(f"Result:\nS_REF =\n{S}")

    #   n,  k
    k, n = np.shape(S.matrix)
    print(f"n = {n}\nk = {k}")

    t1 = Код_слова1(S.matrix)
    t2 = Код_слова2(S.matrix)
    if np.array_equal(t1, t2):
        print("HELLO")

    #   G*
    S.matrix = RREF(S.matrix)
    print(f"Result:\nG* =\n{S}")
    #   H
    H = check(S.matrix)
    print(f"Result:\nH = \n{H}")

    # for i in range(len(t1)):
    #     print(t1[i] @ H % 2)

    print(Дистанс(S.matrix))

    v = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
    e1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    e2 = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0])

    has_error((v + e1) @ H % 2)
    has_error((v + e2) @ H % 2)


if __name__ == '__main__':
    main()
