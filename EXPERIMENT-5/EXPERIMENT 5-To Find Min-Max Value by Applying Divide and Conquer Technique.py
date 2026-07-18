import random
import matplotlib.pyplot as plt

comparison_count = 0


def min_max_dc(arr, low, high):
    global comparison_count

    # Base case: one element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        comparison_count += 1
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2

    lmin, lmax = min_max_dc(arr, low, mid)
    rmin, rmax = min_max_dc(arr, mid + 1, high)

    # Combine
    comparison_count += 1
    overall_min = lmin if lmin < rmin else rmin

    comparison_count += 1
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    mn = mx = arr[0]
    comps = 0

    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x

        comps += 1
        if x > mx:
            mx = x

    return mn, mx, comps


# ---------------- Sample Execution ----------------

arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]

comparison_count = 0
mn, mx = min_max_dc(arr, 0, len(arr) - 1)
dc_comps = comparison_count

_, _, naive_comps = min_max_naive(arr)

print("Array:", arr)
print("Minimum =", mn)
print("Maximum =", mx)
print("Divide & Conquer Comparisons =", dc_comps)
print("Naive Comparisons =", naive_comps)


# ---------------- Performance Analysis ----------------

sizes = [10, 100, 1000, 10000]

dc_values = []
naive_values = []
formula_values = []

print(f'\n{"Size":>8} {"DC Comps":>12} {"Naive Comps":>14} {"Formula":>12}')
print("-" * 50)

for size in sizes:

    arr = [random.randint(1, 10000) for _ in range(size)]

    comparison_count = 0
    mn, mx = min_max_dc(arr, 0, len(arr) - 1)
    dc = comparison_count

    _, _, naive = min_max_naive(arr)

    formula = (3 * size) // 2 - 2

    dc_values.append(dc)
    naive_values.append(naive)
    formula_values.append(formula)

    print(f"{size:>8} {dc:>12} {naive:>14} {formula:>12}")


# ---------------- Performance Graph ----------------

plt.figure(figsize=(8, 5))

plt.plot(sizes, dc_values, marker='o', linewidth=2,
         label="Divide & Conquer")

plt.plot(sizes, naive_values, marker='s', linewidth=2,
         label="Naive")

plt.plot(sizes, formula_values, marker='^', linestyle='--',
         linewidth=2, label="Theoretical (3n/2 - 2)")

plt.title("Comparison Count Analysis")
plt.xlabel("Input Size (n)")
plt.ylabel("Number of Comparisons")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
