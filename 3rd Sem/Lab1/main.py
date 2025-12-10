import math
from typing import Union

class Angle:

    def __init__(self, value: Union[float, 'Angle', int], is_degrees=False):
        if isinstance(value, Angle):
            rads = value.rad
        else:
            rads = math.radians(value) if is_degrees else float(value)
        self.rad = (rads)

    def _normalize_angle(self, rad):
        rad = rad % (2 * math.pi)
        return rad

    @property
    def degrees(self):
        return math.degrees(self.rad)

    @degrees.setter
    def degrees(self, value):
        self.rad = (math.radians(value))

    @property
    def radians(self):
        return self.rad

    @radians.setter
    def radians(self, value):
        self.rad = (value)

    def __str__(self):
        return f"{self.degrees:.2f}°"
    def __repr__(self):
        return f"Angle({self.rad:.4f} rad)"
    def __float__(self):
        return float(self.rad)
    def __int__(self):
        return int(self.rad)



    def __eq__(self, other : Union['Angle', float, int]):
        val = other._normalize_angle(other.rad) if isinstance(other, Angle) else self._normalize_angle(other)
        return abs(self._normalize_angle(self.rad) - val) < 1e-10

    def __lt__(self, other : Union['Angle', float, int]):
        val = other.rad if isinstance(other, Angle) else (other)
        return self.rad < val

    def __add__(self, other : Union['Angle', float, int]):
        val = other.rad if isinstance(other, Angle) else other
        return Angle(self.rad + val)
    
    def __radd__(self, other : Union['Angle', float, int]):
        return self.__add__(other)
    def __sub__(self, other : Union['Angle', float, int]):
        val = other.rad if isinstance(other, Angle) else other
        return Angle(self.rad - val)

    def __mul__(self, number : Union[float, int]):
        return Angle(self.rad * number)
    def __rmul__(self, number : Union[float, int]):
        return self.__mul__(number)
    def __truediv__(self, number : Union[float, int]):
        return Angle(self.rad / number)


class AngleRange:
    def __init__(self, start, end, inc_start=True, inc_end=True):

        self.start = start if isinstance(start, Angle) else Angle(start)
        self.end = end if isinstance(end, Angle) else Angle(end)
        self.inc_start = inc_start
        self.inc_end = inc_end

    def length(self):
        s, e = self.start.rad, self.end.rad
        if e >= s: return e - s
        return (2 * math.pi - s) + e

    def __repr__(self):
        s_sym = "[" if self.inc_start else "("
        e_sym = "]" if self.inc_end else ")"
        return f"{s_sym}{self.start}, {self.end}{e_sym}"
    
    def __str__(self):
        return self.__repr__()

    def __eq__(self, other : 'AngleRange'):
        return (self.start == other.start and self.end == other.end and 
                self.length() == other.length())

    def __lt__(self, other): 
        return self.length() < other.length()

    def __contains__(self, item : Union['Angle', 'AngleRange', float, int]):
        if isinstance(item, AngleRange):
            return (item.start in self) and (item.end in self) and (item.length() <= self.length())
        
        angle = item if isinstance(item, Angle) else Angle(item)
        val = angle.rad
        s, e = self.start.rad, self.end.rad
        
        s_ok = (val >= s) if self.inc_start else (val > s)
        e_ok = (val <= e) if self.inc_end else (val < e)
        
        if s <= e:
            return s_ok and e_ok
        else:      
            return s_ok or e_ok

    def __add__(self, other : 'AngleRange'):
        
        if other in self:
            return self
        if self in other:
            return other
        
        s_in = self.start in other
        e_in = self.end in other
        o_s_in = other.start in self
        o_e_in = other.end in self
        
        if not (s_in or e_in or o_s_in or o_e_in):
            return [self, other]

        if o_s_in and not s_in:
            new_start = self.start
        else:
            new_start = other.start if s_in else self.start
            
        if o_e_in and not e_in:
            new_end = self.end
        else:
            new_end = other.end if e_in else self.end

        return AngleRange(new_start, new_end)

    def __sub__(self, other : 'AngleRange'):

        start_in = self.start in other
        end_in = self.end in other
        o_start_in = other.start in self
        o_end_in = other.end in self
        
        if start_in and end_in: 
            return []

        if start_in and not end_in:
            return AngleRange(other.end, self.end, not other.inc_end, self.inc_end)
        
        if end_in and not start_in:
            return AngleRange(self.start, other.start, self.inc_start, not other.inc_start)

        if o_start_in and o_end_in:
             r1 = AngleRange(self.start, other.start, self.inc_start, not other.inc_start)
             r2 = AngleRange(other.end, self.end, not other.inc_end, self.inc_end)
             return [r1, r2]
        
        return self

print

print("--- Angle ---")
a1 = Angle(90, is_degrees=True)
a2 = Angle(math.pi) 
a3 = Angle(450, is_degrees=True) 

print(f"a1: {a1}, rad: {a1.radians:.2f}")
print(f"a3: {a3}")
print(f"Сравнение 90 и 450: {a1 == a3}") 
print(f"Сложение (90deg + 180deg): {a1 + a2}")
print(f"Сложение с числом (90deg + PI rad): {a1 + math.pi}")
print(f"Типы: int({int(a1)}), float({float(a1):.2f})")

print("\n--- AngleRange ---")
r1 = AngleRange(Angle(350, True), Angle(20, True)) 
r2 = AngleRange(Angle(0, True), Angle(10, True))

print(f"Range 1: {r1}, Длина: {math.degrees(r1.length()):.2f}°")
print(f"0° входит в [350°, 20°]? {Angle(0, True) in r1}")
print(f"Range 2 входит в Range 1? {r2 in r1}")

print("\n--- Арифметика промежутков ---")
r3 = AngleRange(Angle(10, True), Angle(30, True))
res_add = r1 + r3

print(f"{r3} in {r1} {r3 in r1}")
print(f"Сложение {r1} + {r3} = {res_add}")

res_sub = r1 - r2
print(f"Вычитание {r1} - {r2} = {res_sub}")

r4 = AngleRange(Angle(90, True), Angle(180, True))
r5 = AngleRange(Angle(90, True), Angle(180, True), False, False)

r6 = AngleRange(Angle(math.pi/2), Angle(math.pi*5), True, True)
r7 = AngleRange(Angle(math.pi/3), Angle(math.pi*13/2), True, True)

print(f"{repr(r6)} in {repr(r7)} {r6 in r7}")

r8 = AngleRange(Angle(10, True), Angle(50, True), False, False)
r9 = AngleRange(Angle(25, True), Angle(30, True), True, True)

print(f"{repr(r8)} - {repr(r9)} = {r8-r9}")

r10 = AngleRange(Angle(10, True), Angle(50, True), False, False)
r11 = AngleRange(Angle(25, True), Angle(30, True), False, False)

print(f"{repr(r10)} - {repr(r11)} = {r10-r11}")

r12 = AngleRange(Angle(10, True), Angle(50, True), False, False)
r13 = AngleRange(Angle(25, True), Angle(30, True), True, False)

print(f"{repr(r12)} - {repr(r13)} = {r12-r13}")


res_sub2 = r4 - r5
res_add2 = r4 + r5

print(f"Сложение {r4} + {r5} = {res_add2}")
print(f"Вычитание {r4} - {r5} = {res_sub2}")


print("\n=== ТЕСТЫ ДЛЯ __add__ И __sub__ ===")

# Тест 1: Сложение диапазонов без пересечения
print("\n--- Тест 1: Сложение без пересечения ---")
t1_r1 = AngleRange(Angle(10, True), Angle(30, True))
t1_r2 = AngleRange(Angle(100, True), Angle(120, True))
t1_res = t1_r1 + t1_r2
print(f"{t1_r1} + {t1_r2} = {t1_res}")
assert isinstance(t1_res, list) and len(t1_res) == 2, "Должно быть два отдельных диапазона"
print("✓ Тест 1 пройден")

# Тест 2: Сложение полностью перекрывающихся диапазонов
print("\n--- Тест 2: Одинаковые диапазоны ---")
t2_r1 = AngleRange(Angle(45, True), Angle(90, True))
t2_r2 = AngleRange(Angle(45, True), Angle(90, True))
t2_res = t2_r1 + t2_r2
print(f"{t2_r1} + {t2_r2} = {t2_res}")
assert t2_res == t2_r1, "Результат должен быть равен исходному диапазону"
print("✓ Тест 2 пройден")

# Тест 3: Сложение с частичным пересечением
print("\n--- Тест 3: Частичное пересечение ---")
t3_r1 = AngleRange(Angle(20, True), Angle(60, True))
t3_r2 = AngleRange(Angle(50, True), Angle(80, True))
t3_res = t3_r1 + t3_r2
print(f"{t3_r1} + {t3_r2} = {t3_res}")
assert isinstance(t3_res, AngleRange), "Должен быть один объединённый диапазон"
assert t3_res.start == t3_r1.start and t3_res.end == t3_r2.end, "Границы должны быть объединены"
print("✓ Тест 3 пройден")

# Тест 4: Сложение когда один диапазон внутри другого
print("\n--- Тест 4: Один диапазон внутри другого ---")
t4_r1 = AngleRange(Angle(10, True), Angle(100, True))
t4_r2 = AngleRange(Angle(30, True), Angle(70, True))
t4_res = t4_r1 + t4_r2
print(f"{t4_r1} + {t4_r2} = {t4_res}")
assert t4_res == t4_r1, "Результат должен быть больший диапазон"
print("✓ Тест 4 пройден")

# Тест 5: Сложение циклических диапазонов (пересекающих 0°)
print("\n--- Тест 5: Циклические диапазоны с пересечением ---")
t5_r1 = AngleRange(Angle(350, True), Angle(20, True))
t5_r2 = AngleRange(Angle(10, True), Angle(30, True))
t5_res = t5_r1 + t5_r2
print(f"{t5_r1} + {t5_r2} = {t5_res}")
assert isinstance(t5_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 5 пройден")

# Тест 6: Вычитание без пересечения
print("\n--- Тест 6: Вычитание без пересечения ---")
t6_r1 = AngleRange(Angle(10, True), Angle(50, True))
t6_r2 = AngleRange(Angle(100, True), Angle(150, True))
t6_res = t6_r1 - t6_r2
print(f"{t6_r1} - {t6_r2} = {t6_res}")
assert t6_res == t6_r1, "Результат должен быть исходный диапазон"
print("✓ Тест 6 пройден")

# Тест 7: Вычитание полностью перекрывающегося диапазона
print("\n--- Тест 7: Полное вычитание ---")
t7_r1 = AngleRange(Angle(20, True), Angle(80, True))
t7_r2 = AngleRange(Angle(10, True), Angle(100, True))
t7_res = t7_r1 - t7_r2
print(f"{t7_r1} - {t7_r2} = {t7_res}")
assert t7_res == [], "Результат должен быть пустой список"
print("✓ Тест 7 пройден")

# Тест 8: Вычитание только начало перекрывается
print("\n--- Тест 8: Начало в пересечении ---")
t8_r1 = AngleRange(Angle(20, True), Angle(80, True))
t8_r2 = AngleRange(Angle(10, True), Angle(50, True))
t8_res = t8_r1 - t8_r2
print(f"{t8_r1} - {t8_r2} = {t8_res}")
assert isinstance(t8_res, AngleRange), "Результат должен быть один диапазон"
assert t8_res.start == t8_r2.end, "Начало должно быть конец вычитаемого"
print("✓ Тест 8 пройден")

# Тест 9: Вычитание только конец перекрывается
print("\n--- Тест 9: Конец в пересечении ---")
t9_r1 = AngleRange(Angle(20, True), Angle(80, True))
t9_r2 = AngleRange(Angle(60, True), Angle(100, True))
t9_res = t9_r1 - t9_r2
print(f"{t9_r1} - {t9_r2} = {t9_res}")
assert isinstance(t9_res, AngleRange), "Результат должен быть один диапазон"
assert t9_res.end == t9_r2.start, "Конец должен быть начало вычитаемого"
print("✓ Тест 9 пройден")

# Тест 10: Вычитание дырки из середины
print("\n--- Тест 10: Вычитание из середины ---")
t10_r1 = AngleRange(Angle(10, True), Angle(100, True))
t10_r2 = AngleRange(Angle(40, True), Angle(60, True))
t10_res = t10_r1 - t10_r2
print(f"{t10_r1} - {t10_r2} = {t10_res}")
assert isinstance(t10_res, list) and len(t10_res) == 2, "Результат должен быть два диапазона"
assert t10_res[0].end == t10_r2.start and t10_res[1].start == t10_r2.end, "Правильные границы"
print("✓ Тест 10 пройден")

# Тест 11: Сложение с разными inc_start/inc_end
print("\n--- Тест 11: Сложение с разными границами ---")
t11_r1 = AngleRange(Angle(20, True), Angle(60, True), True, False)
t11_r2 = AngleRange(Angle(60, True), Angle(90, True), True, True)
t11_res = t11_r1 + t11_r2
print(f"{t11_r1} + {t11_r2} = {t11_res}")
assert isinstance(t11_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 11 пройден")

# Тест 12: Вычитание с разными inc_start/inc_end
print("\n--- Тест 12: Вычитание с разными границами ---")
t12_r1 = AngleRange(Angle(10, True), Angle(80, True), True, True)
t12_r2 = AngleRange(Angle(30, True), Angle(60, True), False, False)
t12_res = t12_r1 - t12_r2
print(f"{t12_r1} - {t12_r2} = {t12_res}")
assert isinstance(t12_res, list), "Результат должен быть список"
print("✓ Тест 12 пройден")

# Тест 13: Циклический диапазон вычитание
print("\n--- Тест 13: Циклический диапазон вычитание ---")
t13_r1 = AngleRange(Angle(350, True), Angle(20, True))
t13_r2 = AngleRange(Angle(0, True), Angle(10, True))
t13_res = t13_r1 - t13_r2
print(f"{t13_r1} - {t13_r2} = {t13_res}")
print("✓ Тест 13 пройден")

# Тест 14: Сложение соседних диапазонов
print("\n--- Тест 14: Соседние диапазоны (с общей точкой) ---")
t14_r1 = AngleRange(Angle(10, True), Angle(50, True), True, True)
t14_r2 = AngleRange(Angle(50, True), Angle(90, True), True, True)
t14_res = t14_r1 + t14_r2
print(f"{t14_r1} + {t14_r2} = {t14_res}")
assert isinstance(t14_res, AngleRange), "Соседние диапазоны должны объединиться"
print("✓ Тест 14 пройден")

# Тест 15: Сложение с большими углами (> 2π)
print("\n--- Тест 15: Диапазоны с большими углами ---")
t15_r1 = AngleRange(Angle(0), Angle(math.pi*3))
t15_r2 = AngleRange(Angle(math.pi*2), Angle(math.pi*5))
t15_res = t15_r1 + t15_r2
print(f"Сложение диапазонов > 2π: результат получен")
assert isinstance(t15_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 15 пройден")

print("\n=== ВСЕ ТЕСТЫ __add__ И __sub__ ПРОЙДЕНЫ ===")

print("\n=== ТЕСТЫ ДЛЯ ДИАПАЗОНОВ С ПЕРЕХОДОМ ЧЕРЕЗ 360° ===")

# Тест 16: Сложение двух циклических диапазонов
print("\n--- Тест 16: Сложение двух циклических диапазонов ---")
t16_r1 = AngleRange(Angle(340, True), Angle(20, True))
t16_r2 = AngleRange(Angle(350, True), Angle(30, True))
t16_res = t16_r1 + t16_r2
print(f"{t16_r1} + {t16_r2} = {t16_res}")
assert isinstance(t16_res, AngleRange), "Должен быть объединённый циклический диапазон"
print("✓ Тест 16 пройден")

# Тест 17: Вычитание из циклического диапазона
print("\n--- Тест 17: Вычитание из циклического диапазона ---")
t17_r1 = AngleRange(Angle(330, True), Angle(30, True))
t17_r2 = AngleRange(Angle(350, True), Angle(10, True))
t17_res = t17_r1 - t17_r2
print(f"{t17_r1} - {t17_r2} = {t17_res}")
print("✓ Тест 17 пройден")

# Тест 18: Циклический диапазон полностью содержит обычный
print("\n--- Тест 18: Циклический содержит обычный ---")
t18_r1 = AngleRange(Angle(350, True), Angle(50, True))
t18_r2 = AngleRange(Angle(10, True), Angle(30, True))
t18_res = t18_r1 + t18_r2
print(f"{t18_r1} + {t18_r2} = {t18_res}")
assert t18_res == t18_r1, "Циклический диапазон должен поглотить обычный"
print("✓ Тест 18 пройден")

# Тест 19: Большой циклический диапазон (> 180°)
print("\n--- Тест 19: Большой циклический диапазон ---")
t19_r1 = AngleRange(Angle(270, True), Angle(90, True))
t19_r2 = AngleRange(Angle(300, True), Angle(60, True))
t19_res = t19_r1 + t19_r2
print(f"{t19_r1} (длина {math.degrees(t19_r1.length()):.1f}°) + {t19_r2} = {t19_res}")
assert isinstance(t19_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 19 пройден")

# Тест 20: Вычитание обычного из циклического
print("\n--- Тест 20: Вычитание обычного из циклического ---")
t20_r1 = AngleRange(Angle(320, True), Angle(40, True))
t20_r2 = AngleRange(Angle(10, True), Angle(20, True))
t20_res = t20_r1 - t20_r2
print(f"{t20_r1} - {t20_r2} = {t20_res}")
print("✓ Тест 20 пройден")

# Тест 21: Циклический диапазон полное пересечение
print("\n--- Тест 21: Циклические диапазоны полное пересечение ---")
t21_r1 = AngleRange(Angle(300, True), Angle(60, True))
t21_r2 = AngleRange(Angle(310, True), Angle(50, True))
t21_res = t21_r1 - t21_r2
print(f"{t21_r1} - {t21_r2} = {t21_res}")
print("✓ Тест 21 пройден")

# Тест 22: Циклический диапазон начинается в 350°
print("\n--- Тест 22: Циклический [350°, 10°] ---")
t22_r1 = AngleRange(Angle(350, True), Angle(10, True))
t22_r2 = AngleRange(Angle(0, True), Angle(20, True))
t22_res = t22_r1 + t22_r2
print(f"{t22_r1} + {t22_r2} = {t22_res}")
print("✓ Тест 22 пройден")

print("\n=== ТЕСТЫ ДЛЯ ДИАПАЗОНОВ С start > end (РАДИАНЫ) ===")

# Тест 23: Сложение диапазонов где start > end в радианах
print("\n--- Тест 23: Радиан диапазоны start > end ---")
t23_r1 = AngleRange(Angle(4.0), Angle(1.0))
t23_r2 = AngleRange(Angle(5.0), Angle(2.0))
t23_res = t23_r1 + t23_r2
print(f"{t23_r1} (start > end) + {t23_r2} = {t23_res}")
print("✓ Тест 23 пройден")

# Тест 24: Вычитание из диапазона start > end
print("\n--- Тест 24: Вычитание из диапазона start > end ---")
t24_r1 = AngleRange(Angle(5.0), Angle(1.0))
t24_r2 = AngleRange(Angle(3.0), Angle(2.0))
t24_res = t24_r1 - t24_r2
print(f"{t24_r1} (start > end) - {t24_r2} = {t24_res}")
print("✓ Тест 24 пройден")

# Тест 25: Оба диапазона с start > end
print("\n--- Тест 25: Оба диапазона с start > end ---")
t25_r1 = AngleRange(Angle(4.5), Angle(1.5))
t25_r2 = AngleRange(Angle(5.0), Angle(2.0))
t25_res = t25_r1 + t25_r2
print(f"{t25_r1} + {t25_r2} = {t25_res}")
assert isinstance(t25_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 25 пройден")

# Тест 26: Циклический диапазон пересекает 0
print("\n--- Тест 26: Диапазон [5.5 rad, 0.8 rad] ---")
t26_r1 = AngleRange(Angle(5.5), Angle(0.8))
t26_r2 = AngleRange(Angle(6.0), Angle(0.5))
t26_res = t26_r1 - t26_r2
print(f"{t26_r1} - {t26_r2} = {t26_res}")
print("✓ Тест 26 пройден")

# Тест 27: Вычитание полностью перекрывающегося из циклического
print("\n--- Тест 27: Вычитание всего циклического диапазона ---")
t27_r1 = AngleRange(Angle(5.0), Angle(1.0))
t27_r2 = AngleRange(Angle(4.5), Angle(1.5))
t27_res = t27_r1 - t27_r2
print(f"{t27_r1} - {t27_r2} = {t27_res}")
assert t27_res == [], "Результат должен быть пустой"
print("✓ Тест 27 пройден")

# Тест 28: Циклический большой диапазон > 180° в радианах
print("\n--- Тест 28: Циклический диапазон > π радиан ---")
t28_r1 = AngleRange(Angle(4.0), Angle(1.5))
t28_len = t28_r1.length()
print(f"Диапазон {t28_r1}, длина: {t28_len:.2f} rad = {math.degrees(t28_len):.1f}°")
assert t28_len > math.pi, "Длина должна быть больше π"
print("✓ Тест 28 пройден")

# Тест 29: Пересечение циклических диапазонов в радианах
print("\n--- Тест 29: Пересечение циклических [5.5, 0.9] и [5.8, 0.6] ---")
t29_r1 = AngleRange(Angle(5.5), Angle(0.9))
t29_r2 = AngleRange(Angle(5.8), Angle(0.6))
t29_res = t29_r1 + t29_r2
print(f"{t29_r1} + {t29_r2} = {t29_res}")
assert isinstance(t29_res, AngleRange), "Должен быть объединённый диапазон"
print("✓ Тест 29 пройден")

# Тест 30: Сложение циклического и обычного в радианах
print("\n--- Тест 30: Сложение циклического и обычного [rad] ---")
t30_r1 = AngleRange(Angle(5.0), Angle(0.8))
t30_r2 = AngleRange(Angle(0.5), Angle(0.9))
t30_res = t30_r1 + t30_r2
print(f"{t30_r1} + {t30_r2} = {t30_res}")
print("✓ Тест 30 пройден")

print("\n=== ВСЕ РАСШИРЕННЫЕ ТЕСТЫ ПРОЙДЕНЫ ===")