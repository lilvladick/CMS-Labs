def newton_math(f_prime, f_prime_prime, x0, tol=1e-6, maxiter=100):
    x = x0
    for _ in range(maxiter):
        fx_prime = f_prime(x)
        if abs(fx_prime) < tol:
            return x
        fxx_prime = f_prime_prime(x)
        if fxx_prime == 0:
            raise ZeroDivisionError("Вторая производная равна нулю, метод Ньютона не применим.")
        x = x - fx_prime / fxx_prime
    raise RuntimeError("Не удалось найти корень за максимальное количество итераций.")