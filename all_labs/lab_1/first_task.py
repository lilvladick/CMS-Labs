import json
from pulp import LpProblem, LpMaximize, LpVariable, value

def maximize_profit(json_data):
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    profit = data['profit']
    time_matrix = data['time_matrix']
    time_limits = data['time_limits']

    model = LpProblem("Maximize_profit", LpMaximize)

    variables = [LpVariable(f"x{i+1}", lowBound=0, cat='Integer') for i in range(len(profit))]

    model += sum(profit[i] * variables[i] for i in range(len(profit)))

    for i in range(len(time_matrix)):
        model += sum(time_matrix[i][j] * variables[j] for j in range(len(variables))) <= time_limits[i]

    model.solve()

    results = {data['products'][i]: value(variables[i]) for i in range(len(variables))}

    return json.dumps({"status": model.status, "results": results}, ensure_ascii=False, indent=4)
