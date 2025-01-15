from pulp import *

# Create the LP problem
prob = LpProblem("Diet_Problem", LpMinimize)

# Define the decision variables
foods = ['Chicken', 'Omelet', 'Banana', 'Hotdog', 'Potsticker']
food_vars = LpVariable.dicts("Food", foods, lowBound=7, upBound=42)

# Define the objective function (minimize cost) for 1 serving of each
cost = {'Chicken': 0.45, 'Omelet': 3.92, 'Banana': .23, 'Hotdog': 1.5, 'Potsticker': 1.75}
prob += lpSum([cost[f] * food_vars[f] for f in foods])

# Define the nutritional requirements
nutrients = {
    'Sodium': {'Chicken': 64, 'Omelet': 961, 'Banana': 1, 'Hotdog': 1750, 'Potsticker': 625},
    'Calories': {'Chicken': 142, 'Omelet': 486, 'Banana': 105, 'Hotdog': 570, 'Potsticker': 325},
    'Protein': {'Chicken': 27, 'Omelet': 41.2, 'Banana': 1.3, 'Hotdog': 23, 'Potsticker': 17.5},
    'D': {'Chicken': 4, 'Omelet': 27, 'Banana': 0, 'Hotdog': 0, 'Potsticker': 0},
    'Calcium': {'Chicken': 10, 'Omelet': 456, 'Banana': 0, 'Hotdog': 104, 'Potsticker': 38},
    'Iron': {'Chicken': .7, 'Omelet': 4.1, 'Banana': .2, 'Hotdog': 4, 'Potsticker': 3.5},
    'Potassium': {'Chicken': 179, 'Omelet': 426, 'Banana': 422, 'Hotdog': 316, 'Potsticker': 240}
}

# Daily values
min_nutrition_daily = {
    'Calories': 2000,
    'Protein': 50,
    'D': 20,
    'Calcium': 1300,
    'Iron': 18,
    'Potassium': 4700
}

max_nutrition_daily = {
    'Sodium': 5000,
    'Calories': 3000
}

# Weekly values
min_nutrition = {k: v * 7 for k, v in min_nutrition_daily.items()}
max_nutrition = {k: v * 7 for k, v in max_nutrition_daily.items()}


# Add the nutritional constraints
for nutrient in nutrients:
    if nutrient in min_nutrition:
        prob += lpSum([nutrients[nutrient][f] * food_vars[f] for f in foods]) >= min_nutrition[nutrient]
    if nutrient in max_nutrition:
        prob += lpSum([nutrients[nutrient][f] * food_vars[f] for f in foods]) <= max_nutrition[nutrient]

# Solve the problem
prob.solve()

# Print the optimal values of the variables
for v in prob.variables():
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

# Print the optimal objective function value
print("Total Cost of Diet = ", value(prob.objective))