import math
from typing import Union, Any


class Vec2:
    def __init__(self, x: float, y: float):
        if not isinstance(x, (int, float)):
            raise TypeError(f'x should be int or float, got {type(x)} instead')
        if not isinstance(y, (int, float)):
            raise TypeError(f'y should be int or float, got {type(y)} instead')
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __add__(self, other: Any):
        if not isinstance(other, Vec2):
            other = Vec2(other, other)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Any):
        if not isinstance(other, Vec2):
            other = Vec2(other, other)
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Any):
        if not isinstance(other, Vec2):
            other = Vec2(other, other)
        return Vec2(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: Any):
        if not isinstance(other, Vec2):
            other = Vec2(other, other)
        return Vec2(self.x / other.x, self.y / other.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        if not isinstance(x, (int, float)):
            raise TypeError(f'x should be int or float, got {type(x)} instead')
        if not isinstance(y, (int, float)):
            raise TypeError(f'y should be int or float, got {type(y)} instead')
        if not isinstance(z, (int, float)):
            raise TypeError(f'z should be int or float, got {type(z)} instead')
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str((self.x, self.y, self.z))

    def __add__(self, other: Any):
        if not isinstance(other, Vec3):
            other = Vec3(other, other, other)
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Any):
        if not isinstance(other, Vec3):
            other = Vec3(other, other, other)
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Any):
        if not isinstance(other, Vec3):
            other = Vec3(other, other, other)
        return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __truediv__(self, other: Any):
        if not isinstance(other, Vec3):
            other = Vec3(other, other, other)
        return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __abs__(self):
        return Vec3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def norm(self):
        return self / self.length()

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    @staticmethod
    def _sign(value):
        return (0 < value) - (value < 0)

    def sign(self):
        return Vec3(self._sign(self.x), self._sign(self.y), self._sign(self.z))

    @staticmethod
    def _step(edge, x):
        return int(x > edge)

    def step(self, v):
        return Vec3(self._step(self.x, v.x), self._step(self.y, v.y), self._step(self.z, v.z))


def clamp(value, _min, _max):
    """
    Ограничивает значение с двух сторон
    """
    return max(min(value, _max), _min)


def sphere_intersection(ro: Vec3, rd: Vec3, r: float):
    b = ro.dot(rd)
    c = ro.dot(ro) - r**2
    h = b**2 - c
    if h < 0:
        return Vec2(-1, -1)
    h = math.sqrt(h)
    return Vec2(-b-h, -b+h)


def box_intersection(ro: Vec3, rd: Vec3, box_size: Vec3):
    m = Vec3(1, 1, 1) / rd
    n = m * ro
    k = abs(m) * box_size
    t1 = -n - k
    t2 = -n + k
    tN = max(max(t1.x, t1.y), t1.z)
    tF = min(min(t2.x, t2.y), t2.z)
    if tN > tF or tF < 0:
        return Vec2(-1, -1)
    yzx = Vec3(t1.y, t1.z, t1.x)
    zxy = Vec3(t1.z, t1.x, t1.y)
    out_normal = -rd.sign() * yzx.step(t1) * zxy.step(t1)
    return Vec2(tN, tF), out_normal


def plane_intersection(ro: Vec3, rd: Vec3, p: Vec3, w):
    return -(ro.dot(p) + w) / rd.dot(p)


if __name__ == '__main__':
    a = Vec3(1, 1, 1)
    b = Vec3(3, 3, 3)
    print(a)
    print(b)
    print(a / 2)
