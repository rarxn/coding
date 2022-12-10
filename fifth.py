from itertools import combinations, product
from statistics import mode
import numpy as np


def get_basis(cols):
    return [list(c)[::-1] for c in list(product([0, 1], repeat=cols))]


def f(indexes, u):
    if len(indexes) == 0 or np.all(np.asarray(u)[indexes] == 0):
        return 1
    else:
        return 0


def v(indexes, size):
    return [f(indexes, b) for b in get_basis(size)]


def get_g(r, m):
    return np.asarray([v(idx, m) for idx in get_all_indexes(r, m)])


def get_h(idx, m):
    return [u for u in get_basis(m) if f(idx, u) == 1]


def get_complementary(idx, m):
    return [i for i in range(m) if i not in idx]


def get_indexes(size, m):
    return [list(comb) for comb in list(combinations(range(m - 1, -1, -1), size))]


def get_all_indexes(r, m):
    index_array = []
    for i in range(0, r + 1):
        index_array.extend(get_indexes(i, m))
    return index_array


def f_with_t(idx, t, m):
    return [int(np.array_equal(np.asarray(b)[idx], np.asarray(t)[idx])) for b in get_basis(m)]


def major(w, h, idx, m):
    c = get_complementary(idx, m)
    v_array = [f_with_t(c, u, m) for u in h]
    ans = []
    for _v in v_array:
        ans.append(np.dot(np.asarray(_v), np.asarray(w)) % 2)
    return mode(ans)


def encoding(w, r, m, g):
    a = np.zeros((g.shape[0]), dtype=int)
    mas = get_all_indexes(r, m)
    for step in range(r, -1, -1):
        indexes = get_indexes(step, m)
        first = []
        for idx in indexes:
            H = get_h(idx, m)
            first.append(major(w, H, idx, 4))
        pos = mas.index(indexes[0])   # первая позиции в массиве
        for i in range(0, len(first)):
            a[i + pos] = first[i]
        if step != 0:
            w = (a.T @ np.asarray(g) + w) % 2
        else:
            w = a.T @ np.asarray(g) % 2
        # print(f'Слово после {abs(step - r - 1)} декодирований:{w}')
    return w


if __name__ == '__main__':
    G = get_g(2, 4)
    print('G:', G)
    # mes = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    # print('Message:', mes)
    # word_without_mistake = mes @ G % 2
    # print('Word without mistake: ', word_without_mistake)
    # E = np.eye(16, dtype=int)
    # print('Mistake: ', E[4])
    # word_with_mistake = (word_without_mistake + E[4]) % 2
    # print('Word with mistake: ', word_with_mistake)
    # word = encoding(word_with_mistake, 2, 4, G)

    w = np.random.randint(2, size=G.shape[0])
    w = w @ G % 2
    print(f"кодовое слово:\n{w}")
    w[np.random.randint(w.size)] ^= 1
    print(f"кодовое слово с ошибкой:\n{w}")
    # w = np.array([0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0])
    w = encoding(w, 2, 4, G)
    print(f"слово:\n{w}")


# import numpy as np
# import itertools
#
#
# def swap(A, x, y, axis):
#     if axis == 0:
#         A[[x, y], :] = A[[y, x], :]
#     if axis == 1:
#         A[:, [x, y]] = A[:, [y, x]]
#
#
# def Рид_Маллер_канон(r, m):
#     bin = np.array([list(np.binary_repr(i, m)[::-1]) for i in range(2 ** m)], dtype=int)
#     I = []
#     [[I.append(list(j)) for j in itertools.combinations(range(m), k)][::-1] for k in range(r + 1)]
#     G = np.zeros((len(I), len(bin)), dtype=int)
#     for i in range(G.shape[0]):
#         for j in range(G.shape[1]):
#             G[i, j] = np.prod([bin[j, k] ^ 1 for k in I[i]]) if len(I[i]) else 1
#     for i in range(len(I)):
#         for j in range(i + 1, len(I)):
#             if len(I[i]) == len(I[j]):
#                 for k in reversed(range(1, G.shape[1])):
#                     if G[i, k] == G[j, k] and G[i, k - 1] != G[j, k - 1]:
#                         if G[i, k - 1] > G[j, k - 1]:
#                             swap(G, i, j, 0)
#                             break
#                         else:
#                             break
#             else:
#                 break
#     return G
#
# def декодирование(w, r, m, g):
#
#     i = r
#     w_2 = np.copy(w)
#     bin = np.array([list(np.binary_repr(i, m)[::-1]) for i in range(2 ** m)], dtype=int)
#
#     J = []
#     [J.append(list(j)) for j in itertools.combinations(range(m), i)]
#     # print(J)
#
#     J_c = []
#     for j in J:
#         J_c.append(get_complementary(j, m))
#     # print(J_c)
#     m_arr = []
#     for j1, j2 in zip(J, J_c):
#         H_j = []
#         for b in bin:
#             if np.sum([b[k] for k in j1]) == 0:
#                 H_j.append(b)
#         # print(H_j)
#         count_1 = 0
#         for k in H_j:
#             v = np.array([np.array_equal(b[j2], k[j2]) for b in bin], dtype=int)
#             count_1 += v @ w_2 % 2
#         buff = None
#         if count_1 == m / 2:
#             return
#         if count_1 > m / 2:
#             buff = 1
#         else:
#             buff = 0
#         m_arr.append(buff)
#     # result = np.zeros(5,dtype=int)
#     result = np.array(m_arr)
#     print(f'======\n{m_arr}')
#     return np.append(result,np.zeros(5,dtype=int))
#
#
# def get_complementary(J, m):
#     return [i for i in range(m) if i not in J]
#
#
# def main():
#     G = Рид_Маллер_канон(2, 4)
#     print(f"\nПорождающая матрица:\n{G}")
#
#     w = np.random.randint(2, size=G.shape[0])
#     w = w @ G % 2
#     print(f"кодовое слово:\n{w}")
#     w[np.random.randint(w.size)] ^= 1
#     print(f"кодовое слово с ошибкой:\n{w}")
#     # w = np.array([0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0])
#     w = декодирование(w, 2, 4, G)
#
#     print(f"слово:\n{w}")
#     w = w @ G % 2
#     print(f"слово:\n{w}")