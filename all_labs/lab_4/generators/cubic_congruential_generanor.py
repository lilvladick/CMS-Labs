class CubicCongruentialGenerator:
    def __init__(self, a:int, b:int, c:int, k:int, x0:int, d:int=0):
        """
        Инициализация генератора псевдослучайных чисел по кубическому конгруэнтному методу.
        
        Параметры:
        a (int): Коэффициент при x^3
        b (int): Коэффициент при x^2
        c (int): Коэффициент при x
        k (int): Степень для m = 2^k
        x0 (int): Начальное значение (seed)
        d (int, необязательно): Константа, по умолчанию 0
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.m = 2 ** k
        self.current = x0

    def next(self) -> int:
        """
        Возвращает следующее число в последовательности.
        
        Возвращает:
        int: Следующее число
        """
        self.current = (self.a * self.current**3 + self.b * self.current**2 + 
                       self.c * self.current + self.d) % self.m
        return self.current

    def generate_sequence(self, n:int) -> list:
        """
        Генерирует последовательность из n псевдослучайных чисел.
        
        Параметры:
        n (int): Количество чисел для генерации
        
        Возвращает:
        list: Список из n сгенерированных чисел
        """
        return [self.next() for _ in range(n)]