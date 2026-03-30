def is_safe(v, graph, color, c):
    for i in range(len(graph)):
        if graph[v][i] == 1 and c == color[i]:
            return False
    return True

def graph_coloring_util(graph, m, color, v):
    if v == len(graph):
        return True

    for c in range(1, m + 1):
        if is_safe(v, graph, color, c):
            color[v] = c
            if graph_coloring_util(graph, m, color, v + 1):
                return True
            color[v] = 0
    return False

def solve_exact_coloring(graph):
    n = len(graph)
    for m in range(1, n + 1):
        color = [0] * n
        if graph_coloring_util(graph, m, color, 0):
            return m, color
    return None

adj_matrix = [
    [0, 1, 1, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [1, 0, 1, 0]
]

chromatic_number, final_colors = solve_exact_coloring(adj_matrix)

print(f"Minimum colors: {chromatic_number}")
print(f"Nodes coloring: {final_colors}")