import time

def pulp_solution():
    from pulp import LpProblem, LpMaximize, LpVariable, value
    # задача максимизации
    problem = LpProblem("Candy Production Optimization", LpMaximize)

    # Обозначение карамели 1 и 2 вида
    x1 = LpVariable("x1", lowBound=0)
    x2 = LpVariable("x2", lowBound=0)

    # Функция
    problem += 1080 * x1 + 1120 * x2, "Прибыль"

    # Ограничения
    problem += 0.5 * x1 + 0.8 * x2 <= 80, "Сахара внутри"
    problem += 0.4 * x1 + 0.3 * x2 <= 60, "Патоки внутри"
    problem += 0.1 * x1 + 0.1 * x2 <= 13, "Фруктовой пюрешечки внутри"

    problem.solve()
    
    sugar_used = 0.5 * value(x1) + 0.8 * value(x2)
    syrup_used = 0.4 * value(x1) + 0.3 * value(x2)
    fruit_used = 0.1 * value(x1) + 0.1 * value(x2)

    print("\nИспользование ингредиентов:")
    print("Сахар:", sugar_used, "тонн")
    print("Патока:", syrup_used, "тонн")
    print("Фруктовое пюре:", fruit_used, "тонн")

    print("План производства:")
    print("Карамелька первого вида:", value(x1), "тонн")
    print("Карамелька второго вида:", value(x2), "тонн")
    print("Максимальная прибыль:", value(problem.objective), "вечно деревянных")
    
def scipy_solution():
    import numpy as np
    from scipy.optimize import linprog
    
    # Коэффициенты целевой функции (с отрицательным знаком для максимизации, 
    # так как linprog изначально решает задачу минимизации)
    c = [-1080, -1120]

    # Матрица коэффициентов ограничений
    A = [
        [0.5, 0.8],
        [0.4, 0.3],
        [0.1, 0.1]
    ]

    # Вектор правых частей ограничений
    b = [80, 60, 13]

    # Границы переменных (верхних границ нет)
    x1_bounds = (0, None)
    x2_bounds = (0, None)

    res = linprog(c, A_ub=A, b_ub=b, bounds=[x1_bounds, x2_bounds], method='highs')

    print("План производства:")
    print(f"Карамелька первого вида: {res.x[0]:.2f} тонн")
    print(f"Карамелька второго вида: {res.x[1]:.2f} тонн")
    print(f"Максимальная прибыль: {-res.fun:.2f} вечно деревянных")
    
if __name__ == "__main__":
    start = time.time()
    pulp_solution()
    end = time.time()
    solution_time = end - start
    
    print(f"Время выполнения: {solution_time} секунд (pulp) \n")
    
    start = time.time()    
    scipy_solution()
    end = time.time()
    solution_time = end - start
    
    print(f"Время выполнения: {solution_time} секунд (scipy)")
    