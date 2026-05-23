import random
from collections import defaultdict

class FlowNetwork:
    def __init__(self):
        # Используем defaultdict для создания словарей соседства
        self.graph = defaultdict(lambda: defaultdict(int))
        self.orig_graph = defaultdict(lambda: defaultdict(int))
        self.nodes = set()

    def add_edge(self, u, v, capacity):
        """Добавление направленной дуги в граф"""
        self.graph[u][v] = capacity
        self.orig_graph[u][v] = capacity
        self.graph[v][u] = 0  # Инициализация обратной дуги нулем для остаточной сети
        self.nodes.add(u)
        self.nodes.add(v)

    def bfs(self, source, sink, parent):
        """Поиск в ширину (BFS) для нахождения пути в остаточной сети"""
        visited = {n: False for n in self.nodes}
        queue = [source]
        visited[source] = True

        while queue:
            u = queue.pop(0)
            for v in self.nodes:
                # Если узел не посещен и пропускная способность больше 0
                if not visited[v] and self.graph[u][v] > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
        return False

    def ford_fulkerson(self, source, sink):
        """Основной алгоритм Форда-Фалкерсона"""
        parent = {n: None for n in self.nodes}
        max_flow = 0
        step = 1

        print("--- Поиск увеличивающих путей ---")
        # Пока существует путь из S в T
        while self.bfs(source, sink, parent):
            path_flow = float("Inf")
            s = sink
            path = []
            
            # Определяем минимальную пропускную способность найденного пути
            while s != source:
                path.append(s)
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            path.append(source)
            path.reverse()

            max_flow += path_flow
            print(f"Шаг {step}: Найден путь {' -> '.join(path)}, поток увеличен на {path_flow}")
            step += 1

            # Обновляем значения в остаточной сети
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        # Поиск минимального разреза с помощью BFS по остаточной сети от S
        visited = {n: False for n in self.nodes}
        queue = [source]
        visited[source] = True
        while queue:
            u = queue.pop(0)
            for v in self.nodes:
                if not visited[v] and self.graph[u][v] > 0:
                    visited[v] = True
                    queue.append(v)

        # Множества V1 (достижимые) и V2 (недостижимые)
        v1 = [n for n in self.nodes if visited[n]]
        v2 = [n for n in self.nodes if not visited[n]]

        # Формируем дуги, попавшие в разрез
        cut_edges = []
        cut_capacity = 0
        for u in v1:
            for v in v2:
                if self.orig_graph[u][v] > 0:
                    cut_edges.append((u, v, self.orig_graph[u][v]))
                    cut_capacity += self.orig_graph[u][v]

        print(f"\nИТОГ:")
        print(f"Максимальный поток: {max_flow}")
        print(f"Минимальный разрез (множество V1): {sorted(v1)}")
        print(f"Минимальный разрез (множество V2): {sorted(v2)}")
        print("Дуги минимального разреза (из V1 в V2):")
        for u, v, cap in cut_edges:
            print(f"  {u} -> {v} (вес: {cap})")
        print(f"Емкость разреза: {cut_capacity}")

        return max_flow


def main():
    # Список всех дуг из лабораторной работы
    edges = [
        ('S', 'p'), ('S', 'd'), ('S', 'a'),
        ('p', 'k'), ('p', 'b'),
        ('a', 'd'), ('a', 'k'), ('a', 'b'),
        ('d', 'k'), ('d', 'c'),
        ('c', 'T'), ('c', 'b'),
        ('k', 'T'),
        ('b', 'T')
    ]

    print("==================================================")
    print("ЧАСТЬ 1: ИСХОДНАЯ СЕТЬ (ПРОВЕРКА)")
    print("==================================================")
    net1 = FlowNetwork()
    initial_capacities = {
        ('S', 'p'): 7, ('S', 'd'): 61, ('S', 'a'): 31,
        ('p', 'k'): 21, ('p', 'b'): 12,
        ('a', 'd'): 12, ('a', 'k'): 11, ('a', 'b'): 6,
        ('d', 'k'): 7, ('d', 'c'): 6,
        ('c', 'T'): 71, ('c', 'b'): 11,
        ('k', 'T'): 6,
        ('b', 'T'): 51
    }
    for (u, v), cap in initial_capacities.items():
        net1.add_edge(u, v, cap)
    
    net1.ford_fulkerson('S', 'T')

    print("\n\n==================================================")
    print("ЧАСТЬ 2: СЕТЬ СО СЛУЧАЙНЫМИ ВЕСАМИ [100, 1000]")
    print("==================================================")
    net2 = FlowNetwork()
    
    # Задаем случайные пропускные способности
    print("Сгенерированные пропускные способности:")
    for u, v in edges:
        weight = random.randint(100, 1000)
        net2.add_edge(u, v, weight)
        print(f"  {u} -> {v}: {weight}")

    print("")
    net2.ford_fulkerson('S', 'T')

if __name__ == "__main__":
    main()