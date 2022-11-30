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


def first(k, m):
    return np.concatenate((np.eye(k, dtype=int), m), axis=1)


def second(m):
    k, n = m.shape
    return np.concatenate((m[:, k:n], np.eye(n - k, dtype=int)), axis=0)


def ыродип_ырегин_create_x(n, k, d):
    x = None
    buff = list(itertools.product([0, 1], repeat=n - k))
    buff = np.array([row for row in buff if not sum(row) < d - 1])
    if buff.shape[0] < k:
        return x

    for c in itertools.combinations(range(buff.shape[0]), k):
        flag = True
        for i in range(2, d):
            if flag:
                for c_i in itertools.combinations(c, i):
                    if np.sum(np.sum([buff[c_i[j]] for j in range(i)], axis=0) % 2) < d - i:
                        flag = False
                        break

        if flag:
            x = np.array([buff[i] for i in c])
            break
    print(x)
    return x


def syndrome_table(H, mistakes):
    s = dict()
    I = np.eye(H.shape[0], dtype=int)
    if mistakes != 1:
        for k in range(2, mistakes + 1):
            combs = itertools.combinations(range(H.shape[0]), k)
            for c in combs:
                I = np.vstack((I, np.sum([I[c[j]] for j in range(k)], axis=0) % 2))
    for i in I:
        s[np.array2string(i @ H % 2)] = i
    return s


def syndrome_table_one(H):
    s = dict()
    I = np.eye(H.shape[0], dtype=int)
    for i in I:
        s[np.array2string(i @ H % 2)] = i
    return s


def syndrome_table_two(H):
    s = dict()
    I = np.eye(H.shape[0], dtype=int)
    combs = itertools.combinations(range(H.shape[0]), 2)
    for i, j in combs:
        I = np.vstack((I, I[i] ^ I[j]))
    for i in I:
        s[np.array2string(i @ H % 2)] = i
    return s


def fix_error(word, syndrome, table):
    synd = np.array2string(syndrome)
    res = None
    if synd in table:
        res = table[synd] ^ word
    return res


def print_dict(dct):
    for d in dct.items():
        print(f"{d[0]}:  {d[1]}")


def main():
    print('==================\n1часть\n==================')
    G = first(4, a1)
    print(f"\nПорождающая матрица:\n{G}")
    H = second(G)
    print(f"\nПроверочная матрица:\n{H}")
    synd_table = syndrome_table_one(H)

    word = [1, 0, 0, 0]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    print(f"кодовое слово с ошибкой:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")

    word = [1, 0, 0, 0]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    word[4] ^= 1
    print(f"кодовое слово с 2 ошибками:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")

    print('==================\n2часть\n==================')
    n, k = 12, 4
    x = ыродип_ырегин_create_x(n, k, 5)
    G = first(k, x)
    print(f"\nПорождающая матрица:\n{G}")
    H = second(G)
    print(f"\nПроверочная матрица:\n{H}")
    synd_table = syndrome_table_two(H)
    # print_dict(synd_table)
    word = [1, 0, 1, 1]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    print(f"кодовое слово с 1 ошибкой:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")

    word = [1, 0, 1, 1]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    word[4] ^= 1
    print(f"кодовое слово с 2 ошибками:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")

    word = [1, 0, 1, 1]
    word = word @ G % 2
    print(f"\nкодовое слово:\n{word}")
    word[3] ^= 1
    word[4] ^= 1
    word[5] ^= 1
    print(f"кодовое слово с 3 ошибками:\n{word}")
    syndrome = word @ H % 2
    print(f"синдром:\n{syndrome}")
    print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")


if __name__ == '__main__':
    main()
