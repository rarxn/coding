from first import *

a1 = np.array([[1, 1, 1],
               [1, 1, 0],
               [1, 0, 1],
               [0, 1, 1]])
# a1 = np.array([[1, 0, 0, 1, 0, 1, 1],
#                [1, 1, 0, 0, 0, 0, 1],
#                [0, 0, 1, 1, 0, 0, 1],
#                [1, 0, 1, 0, 1, 0, 1],
#                [0, 0, 1, 1, 1, 1, 0]])

a2 = np.array([[1, 1, 1, 1, 1, 0, 0, 0],
               [0, 0, 0, 1, 1, 1, 1, 1],
               [1, 1, 0, 0, 0, 0, 1, 1],
               [0, 1, 0, 1, 0, 1, 0, 1]])


# for i in range(a2.shape[0] - 2):
#     for k in range(a2.shape[0] - 1):
#         for j in range(k + 1, a2.shape[0]):
#             a = a2[i] ^ a2[k] ^ a2[j]
#             print(a)
# print('')
# for i in range(a2.shape[0] - 1):
#     for j in range(i + 1, a2.shape[0]):
#         a = a2[i] ^ a2[j]
#         print(a)


# def first(m):
#     matrix = np.copy(m)
#     matrix_size = matrix.shape
#     for i in range(matrix_size[0]):
#         for j in range(matrix_size[1]):
#             if matrix[i][j] == 1:
#                 if j != i:
#                     change(matrix, j, i, 'column')
#                 break
#     return matrix


def first(k, m):
    return np.concatenate((np.eye(k, dtype=int), m), axis=1)


def second(m):
    k, n = m.shape
    return np.concatenate((m[:, k:n], np.eye(n - k, dtype=int)), axis=0)


def words_with_one_error(m):
    matrix_size = m.shape
    matrix = np.zeros((matrix_size[1]), dtype=int)
    for i in range(matrix_size[0]):
        for j in range(matrix_size[1]):
            buf = np.copy(m[i])
            buf[j] ^= 1
            matrix = np.vstack((matrix, buf))
    return matrix[1:, :]


def fix_error(word, syndrome, H):
    res = None
    idx = -1
    for i in range(len(H)):
        if np.array_equal(syndrome, H[i]):
            idx = i
    if idx != -1:
        res = np.copy(word)
        res[idx] ^= 1
    return res


def main():
    print('==================\n1часть\n==================')
    G = first(4, a1)
    print(f"\nПорождающая матрица:\n{G}")
    H = second(G)
    print(f"\nПроверочная матрица:\n{H}")
    # words = words_with_one_error(G)

    word = [1, 0, 0, 0]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    print(f"кодовое слово с ошибкой:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, H)}")

    word = [1, 0, 0, 0]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    word[4] ^= 1
    print(f"кодовое слово с 2 ошибками:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, H)}")

    print('==================\n2часть\n==================')

    G = first(4, a2)
    print(f"\nПорождающая матрица:\n{G}")
    H = second(G)
    print(f"\nПроверочная матрица:\n{H}")


if __name__ == '__main__':
    main()
