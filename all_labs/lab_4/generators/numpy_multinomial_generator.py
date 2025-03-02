import numpy as np

def generate_sequence(pvals, n):
    """
    Генерирует цепочку случайных чисел длины n с использованием мультиномиального распределения.

    Параметры:
    pvals (list): Массив вероятностей для каждого исхода. Сумма должна быть равна 1.
    n (int): Длина генерируемой цепочки.

    Возвращает:
    numpy.ndarray: Массив длины n, содержащий индексы исходов (0, 1, 2, ...).
    """
    samples = np.random.multinomial(1, pvals, size=n)
    sequence = np.argmax(samples, axis=1)
    return sequence

if __name__ == "__main__":
    arr = generate_sequence([0.3, 0.7], 10)
    print(arr)