"""Головний модуль запуску чисельного інтегрування."""

import math

from integrators import (
    RectangleIntegrator,
    SimpsonIntegrator,
    TrapezoidIntegrator,
)

def example_function(x):
    if abs(x) <= 10 ** (-8):
        return -0.5

    return (math.cos(x) - 1) / x ** 2

def target_function(x):
    """Підінтегральна функція згідно з індивідуальним варіантом."""
    pass


def main():
    """Точка входу програми."""
    a = 0
    b = 1
    e = 0.0001
    func = example_function

    integrators = [RectangleIntegrator(func, a, b),
                   TrapezoidIntegrator(func, a, b),
                   SimpsonIntegrator(func, a, b)]
    
    for integrator in integrators:
        print(integrator)

        adaptive_integrate = integrator.adaptive_integrate(e)
        sigma_integral = adaptive_integrate["integral"] #уточнене значення інтеграла (sigma - крутий)
        n_min = adaptive_integrate["n_min"]

        n = 2
        while n <= n_min:
            print(f"n = {n} -> I = {integrator.integrate(n):.7f}")
            n *= 2

        print(f"Уточнений результат: {sigma_integral:.7f} (n_min = {n_min}, похибка ≈ {abs((sigma_integral - integrator.integrate(n_min))):.2e})\n")

if __name__ == "__main__":
    main()