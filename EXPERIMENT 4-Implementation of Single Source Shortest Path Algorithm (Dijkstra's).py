import heapq
import matplotlib.pyplot as plt


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """

    n = len(graph)

    dist = [float('inf')] * n
    prev = [None] * n

    dist[source] = 0

    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)

        if u in visited:
            continue

        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = prev[node]

    path.reverse()

    if path and path[0] == source:
        return path

    return []


# ---------------- Graph Definition ----------------

graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

source = 0

# Run Dijkstra Algorithm
dist, prev = dijkstra(graph, source)

# ---------------- Display Output ----------------

print(f"\nShortest Paths from Vertex {source}\n")

print(f'{"Vertex":>8} {"Distance":>10} {"Path":>30}')
print("-" * 55)

for v in range(len(graph)):
    path = reconstruct_path(prev, source, v)
    path_str = " -> ".join(map(str, path)) if path else "No Path"

    d = dist[v] if dist[v] != float('inf') else "INF"

    print(f"{v:>8} {str(d):>10} {path_str:>30}")

# ---------------- Bar Graph ----------------

vertices = list(range(len(graph)))
distances = [d if d != float('inf') else 0 for d in dist]

plt.figure(figsize=(8, 5))

bars = plt.bar(vertices, distances)

# Display distance values on bars
for bar, value in zip(bars, distances):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 0.1,
        str(value),
        ha='center',
        fontsize=10
    )

plt.title("Shortest Distance from Source Vertex")
plt.xlabel("Vertex")
plt.ylabel("Distance")
plt.xticks(vertices)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
