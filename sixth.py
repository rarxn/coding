import numpy as np

def error_table(n):
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

def set_error(w, kol_vo_oshibok, пакет):
    word = np.copy(w)
    if пакет:
        buff = np.random.randint(2, size=kol_vo_oshibok)
        if np.any(buff) == 0:
            buff[np.random.randint(kol_vo_oshibok)] ^= 1
        index = np.random.randint(word.size)
        j = index
        for i in range(len(buff)):
            word[j] ^= buff[i]
            j = j + 1 if j + 1 < len(word) else 0
    else:
        for i in np.random.choice(word.size, kol_vo_oshibok, replace=False):
            word[i] ^= 1
    return word


def декодирование(w, g, n, t):
    synd = np.int_(np.polydiv(w, g)[1] % 2)
    print(f"синдром:\n{synd}")
    for i in range(n):
        s_i = np.int_(np.polydiv(np.polymul(np.eye(1, i + 1, dtype=int)[0], synd) % 2, g)[1] % 2)
        if np.sum(s_i) <= t:
            return np.polyadd(np.polymul(np.eye(1, n - i + 1, dtype=int)[0], s_i) % 2, w) % 2 if i != 0 else np.polyadd(
                s_i, w) % 2
    return None


def исследование(n, k, t, g, errors, пакет):
    w = np.random.randint(2, size=k)
    print(f"слово: {w}")
    w = np.polymul(w, g) % 2
    print(f"слово1: {w}")
    for kol_vo_oshibok in range(1, errors + 1):
        word = np.copy(w)
        print(f"\n\t\tКоличество ошибок:{kol_vo_oshibok}")
        print(f"закодированное слово:\n{word}")
        word = set_error(word, kol_vo_oshibok, пакет)
        print(f"слово с {kol_vo_oshibok} ошибками:\n{word}")
        word = декодирование(word, g, n, t)
        print(f"исправлено:{np.array_equal(w, word)}, исправленное слово:\n{word}")


def main():
    print(f"\ng(x)=1 + x^2 + x^3")
    исследование(7, 4, 1, np.array([1, 1, 0, 1]), 3, False)
    print('====================================')
    print(f"\ng(x)=1 + x^3 + x^4 + x^5 + x^6")
    # исследование(15, 9, 3, np.array([1, 1, 0, 1]), 4, True)


if __name__ == '__main__':
    main()
