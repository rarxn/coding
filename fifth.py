import numpy as np
import itertools


def swap(A, x, y, axis):
    if axis == 0:
        A[[x, y], :] = A[[y, x], :]
    if axis == 1:
        A[:, [x, y]] = A[:, [y, x]]


def Рид_Маллер_канон(r, m):
    bin = np.array([list(np.binary_repr(i, m)[::-1]) for i in range(2 ** m)], dtype=int)
    I = []
    [[I.append(list(j)) for j in itertools.combinations(range(m), k)] for k in range(m)]
    G = np.zeros((len(I), len(bin)), dtype=int)
    for i in range(G.shape[0]):
        for j in range(G.shape[1]):
            G[i, j] = np.prod([bin[j, k] ^ 1 for k in I[i]]) if len(I[i]) else 1
    for i in range(len(I)):
        for j in range(i + 1, len(I)):
            if len(I[i]) == len(I[j]):
                for k in reversed(range(1, G.shape[1])):
                    if G[i, k] == G[j, k] and G[i, k - 1] != G[j, k - 1]:
                        if G[i, k - 1] > G[j, k - 1]:
                            swap(G, i, j, 0)
                            break
                        else:
                            break
            else:
                break
    return G


def main():  # k-строки n-столбцы
    matrix = Рид_Маллер_канон(1, 4)
    print(matrix)
    pass


if __name__ == '__main__':
    main()
