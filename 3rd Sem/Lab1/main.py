import math
from typing import Union

class Angle:
    def __init__(self, value: float, is_degrees: bool = False):
        self._radians = value if not is_degrees else math.radians(value)
        self._normalize()
    
    def _normalize(self):
        self._radians = self._radians % (2 * math.pi)

    @property
    def radians(self) -> float:
        return self._radians
    
    @radians.setter
    def radians(self, value: float):
        self._radians = value
        self._normalize()
    
    @property
    def degrees(self) -> float:
        return math.degrees(self._radians)
    
    @degrees.setter
    def degrees(self, value: float):
        self._radians = math.radians(value)
        self._normalize()
    
    def __float__(self) -> float:
        return self._radians
    
    def __int__(self) -> int:
        return int(self._radians)
    
    def __str__(self) -> str:
        return f"{self.degrees:.2f}°"
    
    def __repr__(self):
        return f"Angle({self._radians})"
    
    def __eq__(self, other : Union["Angle", int, float]) -> bool:
        if isinstance(other, (int, float)):
            other = Angle(other)
        return abs(self._radians - other._radians) < 1e-10
    
    def __lt__(self, other : Union["Angle", int, float]) -> bool:
        if isinstance(other, (int, float)):
            other = Angle(other)
        return self._radians < other._radians
    
    def __add__(self, other : Union["Angle", int, float]):
        if isinstance(other, (int, float)):
            return Angle(self._radians + other)
        return Angle(self._radians + other._radians)
    
    def __sub__(self, other: Union["Angle", int, float]):
        if isinstance(other, (int, float)):
            return Angle(self._radians - other)
        return Angle(self._radians - other._radians)
    
    def __mul__(self, other: Union[int, float]):
        return Angle(self._radians * other)

    def __truediv__(self, other: Union[int, float]):
        return Angle(self._radians / other)

class AngleRange:
    def __init__(self, start: Union[Angle, float, int], end: Union[Angle, float, int], 
                 include_start: bool = True, include_end: bool = True):
        self.start = start if isinstance(start, Angle) else Angle(start)
        self.end = end if isinstance(end, Angle) else Angle(end)
        self.include_start = include_start
        self.include_end = include_end
    
    def __str__(self) -> str:
        left = '[' if self.include_start else '('
        right = ']' if self.include_end else ')'
        return f"{left}{self.start}, {self.end}{right}"
    
    def __repr__(self) -> str:
        return f"AngleRange({self.start!r}, {self.end!r}, {self.include_start}, {self.include_end})"
    
    def length(self) -> float:
        length = self.end.radians - self.start.radians
        if length < 0:
            length += 2 * math.pi
        return length

    def __eq__(self, other : "AngleRange") -> bool:
        return (self.start == other.start and self.end == other.end and
                self.include_start == other.include_start and
                self.include_end == other.include_end)

    def __contains__(self, item : Union[Angle, float, int]) -> bool:
        if isinstance(item, (int, float)):
            item = Angle(item)
        if self.start <= self.end:
            return ((self.start < item or (self.start == item and self.include_start)) and
                    (item < self.end or (item == self.end and self.include_end)))
        else:
            return ((item >= self.start and self.include_start) or
                    (item <= self.end and self.include_end))

a1 = Angle(math.pi/2)
a2 = Angle(90, is_degrees=True)
print(f"a1: {a1}, в радианах: {a1.radians}")
print(f"a2: {a2}, в радианах: {a2.radians}")
print(f"a1 == a2: {a1 == a2}")
print(f"a1 + a2: {a1 + a2}")
print(f"a1 * 2: {a1 * 2}")
print(f"a1 + 2: {a1 + 2}")

r1 = AngleRange(0, math.pi/2)
r2 = AngleRange(0, math.pi/2, False, True)

print(f"r1: {r1}")
print(f"r2: {r2}")
print(f"Длина r1: {r1.length()}")
print(f"Равны ли r1 и r2? {r1 == r2}")