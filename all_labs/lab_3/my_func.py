import math

def f(x):
    return x / (1 + math.sin(x))

# Производная функции
def f_prime(x):
    return (1 + math.sin(x) - x * math.cos(x)) / (1 + math.sin(x))**2

# Вторая производная функции
def f_prime_prime(x):
    return ((2 * math.cos(x) + x * math.sin(x)) * (1 + 2 * math.sin(x) + math.sin(x)**2) - 
            (1 + math.sin(x) - x * math.cos(x)) * (2 * math.cos(x) + 2 * math.sin(x) * math.cos(x))) / (1 + math.sin(x))**4