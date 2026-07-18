import time
import random
import string
import matplotlib.pyplot as plt


def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    matches = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1

        if j == m:
            matches.append(i)

    return matches, comparisons


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m

    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)

    lps = compute_lps(pattern)
    matches = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:
        comparisons += 1

        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    n, m = len(text), len(pattern)

    d = 256
    h = pow(d, m - 1, q)

    p_hash = 0
    t_hash = 0

    matches = []
    comparisons = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):

        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1

                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (
                d * (t_hash - ord(text[s]) * h)
                + ord(text[s + m])
            ) % q

            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# ---------------- MAIN ----------------

text = "ABBAACCADAABACBA"
pattern = "AABA"

print("Text   :", text)
print("Pattern:", pattern)

m1, c1 = naive_search(text, pattern)
m2, c2 = kmp_search(text, pattern)
m3, c3 = rabin_karp(text, pattern)

print("\nNaive Search")
print("Matches:", m1)
print("Comparisons:", c1)

print("\nKMP Search")
print("Matches:", m2)
print("Comparisons:", c2)

print("\nRabin-Karp")
print("Matches:", m3)
print("Comparisons:", c3)


# ---------------- PERFORMANCE ANALYSIS ----------------

text_large = "".join(random.choices("ABCD", k=10000))

patterns = [
    "AB",
    "ABCD",
    "ABCDAB",
    "ABCDABCD"
]

naive_comp = []
kmp_comp = []
rk_comp = []

print("\n")
print(f'{"Pattern":>12} {"Naive":>12} {"KMP":>12} {"Rabin-Karp":>15}')
print("-" * 60)

for p in patterns:

    _, c1 = naive_search(text_large, p)
    _, c2 = kmp_search(text_large, p)
    _, c3 = rabin_karp(text_large, p)

    naive_comp.append(c1)
    kmp_comp.append(c2)
    rk_comp.append(c3)

    print(f"{p:>12} {c1:>12} {c2:>12} {c3:>15}")


# ---------------- GRAPH ----------------

plt.figure(figsize=(9, 5))

plt.plot(patterns,
         naive_comp,
         marker='o',
         linewidth=2,
         label="Naive Search")

plt.plot(patterns,
         kmp_comp,
         marker='s',
         linewidth=2,
         label="KMP")

plt.plot(patterns,
         rk_comp,
         marker='^',
         linewidth=2,
         label="Rabin-Karp")

plt.title("Pattern Matching Algorithm Efficiency")
plt.xlabel("Pattern Length")
plt.ylabel("Number of Comparisons")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
