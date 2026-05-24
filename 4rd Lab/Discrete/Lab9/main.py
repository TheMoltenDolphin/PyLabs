import collections
import networkx as nx
import matplotlib.pyplot as plt

# --- Исходные данные ---
edges = [
    (3, 5), (3, 16), (4, 7), (4, 8), (4, 13), (4, 16),
    (5, 10), (5, 14), (6, 17), (7, 9), (7, 10), (7, 14),
    (7, 15), (7, 17), (8, 9), (8, 14), (8, 17), (10, 11),
    (10, 13), (10, 16), (11, 15), (12, 14), (12, 15),
    (13, 14), (13, 15), (15, 16)
]

# --- 1) Алгоритм раскраски (Проверка на двудольность) ---
def get_bipartite_sets(edge_list):
    """
    Проверяет граф на двудольность алгоритмом раскраски (BFS).
    Возвращает две доли вершин (U и V), очищенный список ребер 
    и список удаленных ребер (если граф не был двудольным).
    """
    # Собираем все уникальные вершины
    nodes = set()
    for u, v in edge_list:
        nodes.add(u)
        nodes.add(v)

    # Строим список смежности для неориентированного графа
    adj = {node: set() for node in nodes}
    for u, v in edge_list:
        adj[u].add(v)
        adj[v].add(u)

    color = {} # Словарь для хранения цветов вершин: 0 или 1
    edges_to_remove = [] # Список ребер, нарушающих двудольность
    valid_edges = list(edge_list) # Копия исходных ребер

    # Запускаем BFS для каждой компоненты связности
    for start_node in nodes:
        if start_node not in color:
            color[start_node] = 0 # Красим стартовую вершину в цвет 0
            queue = collections.deque([start_node])

            while queue:
                current = queue.popleft()
                
                # Проверяем всех соседей текущей вершины
                # list() используем, чтобы можно было безопасно удалять элементы из adj
                for neighbor in list(adj[current]): 
                    if neighbor not in color:
                        # Если сосед не покрашен, красим в противоположный цвет (1 - 0 = 1, 1 - 1 = 0)
                        color[neighbor] = 1 - color[current]
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        # Конфликт цветов! Найдено ребро внутри одной доли.
                        # Добавляем ребро в список на удаление
                        conflict_edge = (current, neighbor) if (current, neighbor) in valid_edges else (neighbor, current)
                        if conflict_edge in valid_edges:
                            edges_to_remove.append(conflict_edge)
                            valid_edges.remove(conflict_edge)
                            # Разрываем связь в графе
                            adj[current].remove(neighbor)
                            adj[neighbor].remove(current)

    # Формируем две доли на основе цветов
    U = {node for node, c in color.items() if c == 0}
    V = {node for node, c in color.items() if c == 1}

    return U, V, valid_edges, edges_to_remove

# Выполняем алгоритм раскраски
U, V, valid_edges, removed_edges = get_bipartite_sets(edges)

print("--- Результаты алгоритма раскраски ---")
print(f"Доля U: {sorted(list(U))}")
print(f"Доля V: {sorted(list(V))}")
if not removed_edges:
    print("Граф является двудольным. Удаление ребер не потребовалось.")
else:
    print(f"Граф не двудольный. Удалены ребра: {removed_edges}")
print("-" * 40)

# --- А) Алгоритм Форда-Фалкерсона для паросочетаний ---
def ford_fulkerson_matching(edges, U, V):
    # Строим ориентированный граф (сеть)
    # Исток 'S' соединяем со всеми вершинами доли U, а все вершины V соединяем со стоком 'T'
    graph = nx.DiGraph()
    for u in U:
        graph.add_edge('S', u, capacity=1)
    for u, v in edges:
        # Убедимся, что ребро направлено от U к V
        if u in U and v in V:
            graph.add_edge(u, v, capacity=1)
        elif v in U and u in V:
            graph.add_edge(v, u, capacity=1)
    for v in V:
        graph.add_edge(v, 'T', capacity=1)

    # Используем встроенный алгоритм Форда-Фалкерсона/Эдмондса-Карпа
    flow_value, flow_dict = nx.maximum_flow(graph, 'S', 'T')
    
    # Извлекаем паросочетание из потока
    matching = []
    for u in U:
        for v, flow in flow_dict[u].items():
            if flow == 1 and v != 'S' and v != 'T':
                matching.append((u, v))
                
    return matching

# --- Б) Алгоритм увеличивающих цепей (Алгоритм Куна) ---
def kuhn_matching(edges, U, V):
    # Создаем список смежности
    adj = {u: [] for u in U}
    for u, v in edges:
        if u in U and v in V: adj[u].append(v)
        elif v in U and u in V: adj[v].append(u)

    match = {} # Хранит пару для вершин из V (v: u)
    
    def dfs(u, visited):
        for v in adj[u]:
            if v in visited:
                continue
            visited.add(v)
            # Если вершина v свободна ИЛИ мы можем найти увеличивающую цепь для её текущего партнера
            if v not in match or dfs(match[v], visited):
                match[v] = u
                return True
        return False

    # Запускаем поиск увеличивающих цепей для каждой вершины из U
    for u in U:
        visited = set()
        dfs(u, visited)
        
    return [(u, v) for v, u in match.items()]

# --- Выполнение алгоритмов ---
ff_result = ford_fulkerson_matching(edges, U, V)
kuhn_result = kuhn_matching(edges, U, V)

print("Максимальное паросочетание (Форд-Фалкерсон):", ff_result)
print("Размер:", len(ff_result))
print("Максимальное паросочетание (Увеличивающие цепи):", kuhn_result)
print("Размер:", len(kuhn_result))

# --- В) Программа, визуализирующая результаты ---
def visualize_bipartite_graph(edges, U, V, matching):
    G = nx.Graph()
    G.add_nodes_from(U, bipartite=0)
    G.add_nodes_from(V, bipartite=1)
    G.add_edges_from(edges)

    # Позиционирование графа для двух долей
    pos = {}
    pos.update((node, (1, index)) for index, node in enumerate(sorted(U)))
    pos.update((node, (2, index)) for index, node in enumerate(sorted(V)))

    plt.figure(figsize=(10, 8))
    
    # Рисуем обычные ребра (тонкие, серые)
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='lightgray', width=1)
    
    # Рисуем ребра, вошедшие в максимальное паросочетание (толстые, красные)
    matching_edges = [(u, v) if (u, v) in edges or (v, u) in edges else (v, u) for u, v in matching]
    nx.draw_networkx_edges(G, pos, edgelist=matching_edges, edge_color='red', width=3)
    
    # Рисуем вершины
    nx.draw_networkx_nodes(G, pos, nodelist=U, node_color='skyblue', node_size=600)
    nx.draw_networkx_nodes(G, pos, nodelist=V, node_color='lightgreen', node_size=600)
    
    # Добавляем подписи
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    plt.title("Визуализация наибольшего паросочетания (красные ребра)")
    plt.axis('off')
    plt.show()

# Запуск визуализации (покажет граф с найденным паросочетанием)
visualize_bipartite_graph(edges, U, V, kuhn_result)