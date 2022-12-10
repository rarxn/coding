import numpy as np

B = np.array([[1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
              [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
              [0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
              [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
              [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
              [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
              [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
              [0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
              [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1],
              [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
              [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])


def Голея(matrix):
    return np.concatenate((np.eye(matrix.shape[0], dtype=int), matrix), axis=1), np.concatenate(
        (np.eye(matrix.shape[1], dtype=int), matrix),
        axis=0)


def first():
    print('===========ЧАСТь 1=========')
    G, H = Голея(B)
    # print(f"\nПорождающая матрица:\n{G}")
    # print(f"\nПроверочная матрица:\n{H}")
    w = np.random.randint(2, size=G.shape[0])
    w = w @ G % 2
    errors = 4
    for kol_vo_oshibok in range(1, errors + 1):
        word = np.copy(w)
        print(f"\n\t\tКоличество ошибок:{kol_vo_oshibok}")
        print(f"кодовое слово:\n{word}")
        for i in np.random.choice(word.size, kol_vo_oshibok, replace=False):
            word[i] ^= 1
        print(f"кодовое слово с {kol_vo_oshibok} ошибок:\n{word}")
        syndrome = word @ H % 2
        fix = None
        n = len(syndrome)

        if np.sum(syndrome) <= 3:
            fix = np.append(syndrome, np.zeros(n, dtype=int))
        if fix is None:
            for k in range(B.shape[0]):
                if np.sum(syndrome ^ B[k]) <= 2:
                    buf = np.zeros(n, dtype=int)
                    buf[k] = 1
                    fix = np.append(syndrome ^ B[k], buf)
                if fix is not None:
                    break
        if fix is None and np.sum(syndrome @ B % 2) <= 3:
            buf = np.zeros(n, dtype=int)
            fix = np.append(buf, syndrome @ B % 2)
        if fix is None:
            for k in range(B.shape[0]):
                if np.sum((syndrome @ B % 2) ^ B[k]) <= 2:
                    buf = np.zeros(n, dtype=int)
                    buf[k] = 1
                    fix = np.append(buf, (syndrome @ B % 2) ^ B[k])
                if fix is not None:
                    break

        if fix is None:
            print('исправить не получылось')
        else:
            fixed = fix ^ word
            print(f"исправлено:{np.array_equal(w, fixed)}, исправленное слово:\n{fixed}")


def Рид_Маляр(r, m):
    if r == 0:
        return np.ones((1, 2 ** m), dtype=int)
    elif 0 < r < m:
        G1 = Рид_Маляр(r, m - 1)
        G2 = Рид_Маляр(r - 1, m - 1)
        part1 = np.concatenate((G1, np.zeros((G2.shape[0], G1.shape[1]), dtype=int)), axis=0)
        part2 = np.concatenate((G1, G2), axis=0)
        return np.concatenate((part1, part2), axis=1)
    elif r == m:
        up = Рид_Маляр(r - 1, m)
        down = np.zeros((1, 2 ** m), dtype=int)
        down[0, -1] = 1
        return np.concatenate((up, down), axis=0)


def h_i_m(H, i, m):
    matrix = np.kron(np.eye(2 ** (m - i), dtype=int), H)
    matrix = np.kron(matrix, np.eye(2 ** (i - 1), dtype=int))
    return matrix


def second(r, m, errors):
    G = Рид_Маляр(r, m)
    print(f"\nПорождающая матрица:\n{G}")
    H = np.array([[1, 1], [1, -1]])
    w = np.random.randint(2, size=G.shape[0])
    print(f'сообщение: {w}')
    w = w @ G % 2
    for kol_vo_oshibok in range(1, errors + 1):
        word = np.copy(w)
        print(f"\n\t\tКоличество ошибок:{kol_vo_oshibok}")
        print(f"кодовое слово:\n{word}")
        for i in np.random.choice(word.size, kol_vo_oshibok, replace=False):
            word[i] ^= 1
        print(f"кодовое слово с {kol_vo_oshibok} ошибками:\n{word}")
        word[word == 0] = -1
        for i in range(1, m + 1):
            word = word @ h_i_m(H, i, m)
        index = np.argmax(np.abs(word))
        bin = np.binary_repr(index, m)[::-1]
        bin = ('1' if word[index] > 0 else '0') + bin
        print(f"w_{m} = {word}")
        word = np.array(list(bin), dtype=int)
        print(f"декодированное сообщение:{word}")
        word = word @ G % 2
        print(f"исправлено:{np.array_equal(w, word)}, исправленное слово:\n{word}")


def main():  # k-строки n-столбцы
    first()
    # second(1, 3, 2)
    # print('============')
    # second(2, 4, 4)


if __name__ == '__main__':
    main()
