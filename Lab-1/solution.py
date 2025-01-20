from pulp import *

profit = [10, 14, 12]
time_matrix = [
    [2, 4, 5],  # Фрезерное
    [1, 8, 6], # Токарное
    [7, 4, 5], # Сварочное
    [4, 6, 7]  # Шлифовальное
]
time_limits = [120, 280, 240, 360]

model = LpProblem("Maximize_profit", LpMaximize)

x1 = LpVariable("x1", lowBound=0, cat='Integer') #A
x2 = LpVariable("x2", lowBound=0, cat='Integer') #B
x3 = LpVariable("x3", lowBound=0, cat='Integer') #C

model += profit[0]*x1 + profit[1]*x2 + profit[2]*x3

for i in range(len(time_matrix)):
    model += time_matrix[i][0]*x1 + time_matrix[i][1]*x2 + time_matrix[i][2]*x3 <= time_limits[i]

model.solve()

print(f"Оптимальные значения:")
print(f"x1 = {value(x1)}, x2 = {value(x2)}, x3 = {value(x3)}")