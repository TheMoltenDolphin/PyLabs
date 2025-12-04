import math
from typing import Union

class Angle:

    def __init__(self, value: Union[float, 'Angle', int], is_degrees=False):
        if isinstance(value, Angle):
            rads = value.rad
        else:
            rads = math.radians(value) if is_degrees else float(value)
        self.rad = self._normalize(rads)

    def _normalize(self, value):
        return value % (2 * math.pi)

    @property
    def degrees(self):
        return math.degrees(self.rad)

    @degrees.setter
    def degrees(self, value):
        self.rad = self._normalize(math.radians(value))

    @property
    def radians(self):
        return self.rad

    @radians.setter
    def radians(self, value):
        self.rad = self._normalize(value)

    def __str__(self):
        return f"{self.degrees:.2f}°"
    def __repr__(self):
        return f"Angle({self.rad:.4f} rad)"
    def __float__(self):
        return float(self.rad)
    def __int__(self):
        return int(self.rad)

    def __eq__(self, other : Union['Angle', float, int]):
        val = other.rad if isinstance(other, Angle) else self._normalize(other)
        return abs(self.rad - val) < 1e-10

    def __lt__(self, other : Union['Angle', float, int]):
        val = other.rad if isinstance(other, Angle) else self._normalize(other)
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
        
        if s_in and e_in: return other
        if not s_in and not e_in and not (other.start in self):
            return [self, other]

        new_start = other.start if (self.start in other) else self.start
        new_end = other.end if (self.end in other) else self.end
        return AngleRange(new_start, new_end)

    def __sub__(self, other : 'AngleRange'):

        start_in = self.start in other
        end_in = self.end in other
        
        if start_in and end_in and other.length() < self.length():
             r1 = AngleRange(self.start, other.start, self.inc_start, not other.inc_start)
             r2 = AngleRange(other.end, self.end, not other.inc_end, self.inc_end)

             return [r1, r2]
        
        if start_in and end_in: return []

        if start_in:
            return AngleRange(other.end, self.end, not other.inc_end, self.inc_end)
        
        if end_in:
            return AngleRange(self.start, other.start, self.inc_start, not other.inc_start)

        if other.start in self:
             r1 = AngleRange(self.start, other.start, self.inc_start, not other.inc_start)
             r2 = AngleRange(other.end, self.end, not other.inc_end, self.inc_end)

             return [r1, r2]
        
        return self

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