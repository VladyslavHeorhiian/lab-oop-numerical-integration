"""Модуль реалізації класів чисельного інтегрування."""


class BaseIntegrator:
    """Базовий клас для чисельного обчислення визначених інтегралів."""

    order = 1
    method_name = "Базовий метод"

    def __init__(self, func, a, b):
        """Ініціалізує підінтегральну функцію та межі інтегрування."""
        self.func = func
        self.validate_bounds(a, b)
        self.a = a
        self.b = b

    @classmethod
    def from_dict(cls, func, params):
        """Альтернативний конструктор для створення інтегратора зі словника."""
        return cls(func, params["a"], params["b"])

    @staticmethod
    def validate_bounds(a, b):
        """Перевіряє коректність меж інтегрування."""
        if a >= b:
            raise ValueError("Неправильні межі інтегрування")

    def integrate(self, n):
        """Обчислює наближене значення інтеграла для n розбиттів."""
        raise NotImplementedError

    def adaptive_integrate(self, eps=1e-4, initial_n=2):
        """Знаходить інтеграл із заданою точністю eps за правилом Рунге."""
        n = initial_n
        delta = lambda n: (self.integrate(2 * n) - self.integrate(n)) / (2 ** self.order - 1)
        while abs(delta(n)) >= eps:
            n *= 2

        return { "integral": self.integrate(2 * n) + delta(n),
                 "n_min": 2 * n }

    def __str__(self):
        """Повертає рядкове представлення об'єкта інтегратора."""
        return f"{self.method_name} на відрізку [{self.a}; {self.b}] (порядок точності O(h^{self.order}))"


class RectangleIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою середніх прямокутників."""

    order = 2
    method_name = "Формула прямокутників"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        integral = 0
        h = (self.b - self.a) / n
        for i in range(0, n):
            integral += self.func(self.a + i * h + h / 2)
        integral *= h
        
        return integral


class TrapezoidIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою трапецій."""

    order = 2
    method_name = "Формула трапецій"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        integral = 0
        h = (self.b - self.a) / n
        for i in range(1, n):
            integral += self.func(self.a + i * h)
        integral += (self.func(self.a) + self.func(self.b)) / 2
        integral *= h
        
        return integral


class SimpsonIntegrator(BaseIntegrator):
    """Обчислення інтеграла складеною формулою Сімпсона."""

    order = 4
    method_name = "Формула Сімпсона"

    def __init__(self, func, a, b):
        super().__init__(func, a, b)

    def integrate(self, n):
        if n % 2 != 0:
            return "n is odd"

        integral = 0
        h = (self.b - self.a) / n

        integral_odd = 0
        for i in range(1, n, 2):
            integral_odd += self.func(self.a + i * h)
        integral_odd *= 4

        integral_even = 0
        for i in range(2, n - 1, 2):
            integral_even += self.func(self.a + i * h)
        integral_even *= 2

        integral = integral_odd + integral_even
        integral += self.func(self.a) + self.func(self.b)
        integral *= h / 3

        return integral