import math


def get_line_eq(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (y1 - y2), (x2 - x1), (x1 * y2 - x2 * y1)

def intersect_lines(p1, p2, p3, p4):
    A1, B1, C1 = get_line_eq(p1, p2)
    A2, B2, C2 = get_line_eq(p3, p4)
    det = A1 * B2 - A2 * B1
    if abs(det) < 1e-9: return None 
    x = (B1 * C2 - B2 * C1) / det
    y = (A2 * C1 - A1 * C2) / det
    return (x, y)

def on_segment(p, a, b):
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and \
           min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def intersect_segments(p1, p2, p3, p4):
    pt = intersect_lines(p1, p2, p3, p4)
    if pt and on_segment(pt, p1, p2) and on_segment(pt, p3, p4):
        return pt
    return None

def intersect_line_circle(p1, p2, center, r):
    cx, cy = center
    A, B, C = get_line_eq(p1, p2)
    dist = abs(A*cx + B*cy + C) / math.sqrt(A**2 + B**2)
    if dist > r: return []
    
    x0 = -A*C/(A**2+B**2) 
    t_c = (cx, cy)
    A, B, C = get_line_eq((p1[0]-cx, p1[1]-cy), (p2[0]-cx, p2[1]-cy))
    x0, y0 = -A*C/(A**2+B**2), -B*C/(A**2+B**2)
    
    if abs(dist - r) < 1e-9: return [(x0+cx, y0+cy)]
    
    d = math.sqrt(r**2 - dist**2)
    mult = math.sqrt(d**2 / (A**2 + B**2))
    return [(x0 + B*mult + cx, y0 - A*mult + cy), (x0 - B*mult + cx, y0 + A*mult + cy)]

def intersect_circles(c1, r1, c2, r2):
    d = math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0: return []
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = math.sqrt(max(0, r1**2 - a**2))
    x2 = c1[0] + a * (c2[0] - c1[0]) / d
    y2 = c1[1] + a * (c2[1] - c1[1]) / d
    return [
        (x2 + h * (c2[1] - c1[1]) / d, y2 - h * (c2[0] - c1[0]) / d),
        (x2 - h * (c2[1] - c1[1]) / d, y2 + h * (c2[0] - c1[0]) / d)
    ]


def is_inside(tri, p):
    def area(a, b, c):
        return abs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-y1) + c[0]*(y1-b[1])) / 2.0)
    
    a, b, c = tri
    y1 = a[1] 
    abc = abs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])) / 2.0)
    pab = abs((p[0]*(a[1]-b[1]) + a[0]*(b[1]-p[1]) + b[0]*(p[1]-a[1])) / 2.0)
    pbc = abs((p[0]*(b[1]-c[1]) + b[0]*(c[1]-p[1]) + c[0]*(p[1]-b[1])) / 2.0)
    pac = abs((p[0]*(a[1]-c[1]) + a[0]*(c[1]-p[1]) + c[0]*(p[1]-a[1])) / 2.0)
    return abs(abc - (pab + pbc + pac)) < 1e-9

def solve_nested_triangles(points):
    from itertools import combinations
    n = len(points)
    if n < 6: return False 
    
    triangles = list(combinations(points, 3))
    
    for i in range(len(triangles)):
        for j in range(len(triangles)):
            if i == j: continue
            t1, t2 = triangles[i], triangles[j]
            if all(is_inside(t1, p) for p in t2):
                print(f"Треугольник {t2} вложен в {t1}")
                return True
    return False

pts = [(0,0), (10,0), (5,10), (2,2), (4,2), (3,4)]
print("Есть вложенные треугольники:", solve_nested_triangles(pts))