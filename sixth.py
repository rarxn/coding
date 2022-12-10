import numpy as np


def set_error(w, kol_vo_oshibok, пакет):
    word = np.copy(w)
    idx = []
    if пакет:
        buff = np.random.randint(2, size=kol_vo_oshibok)
        if np.any(buff) == 0:
            buff[np.random.randint(kol_vo_oshibok)] ^= 1
        index = np.random.randint(word.size)
        j = index
        for i in range(len(buff)):
            idx.append(j)
            word[j] ^= buff[i]
            j = j + 1 if j + 1 < len(word) else 0
    else:
        for i in np.random.choice(word.size, kol_vo_oshibok, replace=False):
            idx.append(i)
            word[i] ^= 1
    print(f'индексы ошибок: {idx}')
    return word


def is_error(x, t):
    buff = np.trim_zeros(np.copy(x))
    return len(buff) <= t and len(buff) != 0


def декодирование(w, g, n, t, пакет):
    synd = np.int_(np.polydiv(w, g)[1] % 2)
    print(f"синдром:\n{synd}")
    for i in range(n):
        s_i = np.int_(np.polydiv(np.polymul(np.eye(1, i + 1, dtype=int)[0], synd) % 2, g)[1] % 2)
        if (пакет and is_error(s_i, t)) or (not пакет and np.sum(s_i) <= t):
            return np.polyadd(np.polymul(np.eye(1, n - i + 1, dtype=int)[0], s_i) % 2, w) % 2 if i != 0 \
                else np.polyadd(s_i, w) % 2
        # else:
        #     if np.sum(s_i) <= t:
        #         return np.polyadd(np.polymul(np.eye(1, n - i + 1, dtype=int)[0], s_i) % 2, w) % 2 if i != 0 \
        #             else np.polyadd(s_i, w) % 2
    return None


def исследование(n, k, t, g, errors, пакет):
    w = np.random.randint(2, size=k)
    w = np.polymul(w, g) % 2
    for kol_vo_oshibok in range(1, errors + 1):
        word = np.copy(w)
        print(f"\n\t\tКоличество ошибок:{kol_vo_oshibok}")
        print(f"закодированное слово:\n{word}")
        word = set_error(word, kol_vo_oshibok, пакет)
        print(f"слово с {kol_vo_oshibok} ошибками:\n{word}")
        word = декодирование(word, g, n, t, пакет)
        print(f"исправлено:{np.array_equal(w, word)}, исправленное слово:\n{word}")


def main():
    # print(f"\ng(x)=1 + x^2 + x^3")
    # исследование(7, 4, 1, np.array([1, 1, 0, 1]), 3, False)
    # print('====================================')
    print(f"\ng(x)=1 + x^3 + x^4 + x^5 + x^6")
    исследование(15, 9, 3, np.array([1, 1, 1, 1, 0, 0, 1]), 4, True)


if __name__ == '__main__':
    main()
