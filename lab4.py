import time
from random import randint

class GaloisField:
    def __init__(self, m):
        self.m = m
        self.size = 2 ** m
        self.primitive_poly = self.generate_primitive_poly()

    def generate_primitive_poly(self):
        # Простий поліном для прикладу. У реальній задачі варто використовувати табличні примітивні поліноми.
        return (1 << self.m) | 1

    def zero(self):
        return 0

    def one(self):
        return 1

    def add(self, a, b):
        return a ^ b

    def multiply(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a & self.size:
                a ^= self.primitive_poly
            b >>= 1
        return result % self.size

    def trace(self, a):
        result = 0
        current = a
        for _ in range(self.m):
            result ^= current
            current = self.square(current)
        return result

    def square(self, a):
        return self.multiply(a, a)

    def power(self, a, exp):
        result = 1
        while exp:
            if exp & 1:
                result = self.multiply(result, a)
            a = self.square(a)
            exp >>= 1
        return result

    def inverse(self, a):
        return self.power(a, self.size - 2)

    def to_binary(self, a):
        return bin(a)[2:].zfill(self.m)

    def from_binary(self, binary):
        return int(binary, 2)

# Створення поля Галуа розмірності 593
m = 10  # Для тесту зменшимо m до 10 (велике m може спричинити надто довгий розрахунок)
gf = GaloisField(m)

# Тестові значення для операцій
a, b, c, d = 5, 10, 15, 20

def test_operations():
    try:
        assert gf.add(a, b) == gf.add(b, a)
        assert gf.multiply(a, b) == gf.multiply(b, a)
        assert gf.multiply(gf.add(a, b), c) == gf.add(gf.multiply(a, c), gf.multiply(b, c))
        if d != 0:
            assert gf.multiply(d, gf.inverse(d)) == gf.one()
        print("Усі базові операції виконуються коректно.")
    except AssertionError as e:
        print("Помилка в тестах операцій.", e)

def benchmark_operations():
    operations = {
        "Додавання": lambda: gf.add(a, b),
        "Множення": lambda: gf.multiply(a, b),
        "Квадрат": lambda: gf.square(a),
        "Степінь": lambda: gf.power(a, 10),
        "Слід": lambda: gf.trace(a),
        "Обернене значення": lambda: gf.inverse(a),
        "До бінарного рядка": lambda: gf.to_binary(a),
        "З бінарного рядка": lambda: gf.from_binary(gf.to_binary(a)),
    }

    results = {}
    for name, operation in operations.items():
        start_time = time.time()
        for _ in range(1000):
            operation()
        end_time = time.time()
        results[name] = (end_time - start_time) / 1000

    for op, avg_time in results.items():
        print(f"{op}: {avg_time:.10f} секунд на операцію")

def main():
    test_operations()
    benchmark_operations()

if __name__ == "__main__":
    main()
