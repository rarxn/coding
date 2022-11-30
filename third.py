from second import *


def change_g_h(g, h):
    buff = np.zeros((g.shape[0], 1), dtype=int)
    for i in range(g.shape[0]):
        buff[i] = np.sum(g[i]) % 2
    g = np.concatenate((g, buff), axis=1)
    h = np.concatenate((h, np.zeros((1, h.shape[1]), dtype=int)), axis=0)
    h = np.concatenate((h, np.ones((h.shape[0], 1), dtype=int)), axis=1)
    return g, h


def ybuths_gbljhs(matrix, flag):
    G = first(matrix.shape[0], matrix)
    # print(f"\nПорождающая матрица:\n{G}")
    H = second(G)
    # print(f"\nПроверочная матрица:\n{H}")
    n = 4
    if flag:
        G, H = change_g_h(G, H)
        n = 5
    synd_table = syndrome_table_one(H)

    w = np.random.randint(2, size=matrix.shape[0])
    print(f"\nкодовое слово:\n{w}")
    w = w @ G % 2
    # print(f"\nкодовое слово:\n{w}")

    for kol_vo_oshibok in range(1, n):
        word = np.copy(w)
        print(f"\nКоличество ошибок:{kol_vo_oshibok}")
        print(f"\nкодовое слово:\n{word}")
        for i in np.random.choice(word.size, kol_vo_oshibok, replace=False):
            word[i] ^= 1
        print(f"кодовое слово с {kol_vo_oshibok} ошибок:\n{word}")
        syndrome = word @ H % 2
        isprav = fix_error(word, syndrome, synd_table)
        print(f"исправлено:{np.array_equal(w, isprav)}, исправленное слово:{isprav}")
        # print(f"синдром:\n{syndrome}")
        # print(f"исправленное кодовое слово:\n{fix_error(word, syndrome, synd_table)}")


def main():
    print('==================\n3.1, 3.2\n==================')
    for r in [2, 3, 4]:
        n = 2 ** r - 1
        k = 2 ** r - r - 1
        matrix = ыродип_ырегин_create_x(n, k, 3)
        ybuths_gbljhs(matrix, False)
    print('==================\n3.3, 3.4\n==================')
    for r in [2, 3, 4]:
        n = 2 ** r
        k = 2 ** r - r - 1
        matrix = ыродип_ырегин_create_x(n, k, 3)
        ybuths_gbljhs(matrix, True)


if __name__ == '__main__':
    main()