import math

def get_orientation(p1, p2, p3):
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def graham_scan(points):
    n = len(points)
    if n < 3: return []

    p0 = min(points, key=lambda p: (p[1], p[0]))
    
    def get_angle(p):
        return math.atan2(p[1] - p0[1], p[0] - p0[0])

    def dist_sq(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    sorted_points = sorted(points, key=lambda p: (get_angle(p), dist_sq(p0, p)))
    
    unique_points = []
    for i in range(n):
        while i < n - 1 and get_angle(sorted_points[i]) == get_angle(sorted_points[i+1]):
            i += 1
        unique_points.append(sorted_points[i])

    if len(unique_points) < 3: return []

    hull = [unique_points[0], unique_points[1], unique_points[2]]

    for i in range(3, len(unique_points)):
        while len(hull) > 1 and get_orientation(hull[-2], hull[-1], unique_points[i]) != 2:
            hull.pop()
        hull.append(unique_points[i])

    return hull

data = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]

result_hull = graham_scan(data)

if len(result_hull) >= 3:
    print(f"Оболочка существует. Точек в ней: {len(result_hull)}")
    print("Координаты оболочки:", result_hull)
else:
    print("Выпуклая оболочка не существует.")