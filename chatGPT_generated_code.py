from scipy.optimize import linprog

# Coefficients for the cost function (minimize weekly cost)
cost = [1.75, 3.92, 1.50, 0.45, 0.23]  # Daily cost per portion
weekly_cost = [7 * c for c in cost]    # Weekly cost

# Nutritional constraints (nutrient values per portion)
sodium = [625, 961, 1750, 64, 1]       # mg
calories = [325, 486, 570, 142, 105]   # kcal
protein = [17.5, 41.2, 23, 27, 1.3]    # g
vitamin_d = [0, 27, 0, 4, 0]           # mcg
calcium = [38, 456, 104, 10, 0]        # mg
iron = [3.5, 4.1, 4, 0.7, 0.2]         # mg
potassium = [240, 426, 316, 179, 422]  # mg

# Constraint bounds for daily intake (multiplied by 7 for a weekly diet)
daily_constraints = {
    "sodium": [0, 5000],
    "calories": [2000, 3000],
    "protein": [50, float("inf")],
    "vitamin_d": [20, float("inf")],
    "calcium": [1300, float("inf")],
    "iron": [18, float("inf")],
    "potassium": [4700, float("inf")],
}

# Inequality matrix and bounds
A = [
    sodium,                       # Sodium ≤ 5000
    [-c for c in calories],       # Calories ≥ 2000 (negated to form ≤ constraint)
    calories,                     # Calories ≤ 3000
    [-p for p in protein],        # Protein ≥ 50
    [-v for v in vitamin_d],      # Vitamin D ≥ 20
    [-c for c in calcium],        # Calcium ≥ 1300
    [-i for i in iron],           # Iron ≥ 18
    [-k for k in potassium],      # Potassium ≥ 4700
]

b = [
    daily_constraints["sodium"][1],  # Max sodium
    -daily_constraints["calories"][0],  # Min calories
    daily_constraints["calories"][1],   # Max calories
    -daily_constraints["protein"][0],   # Min protein
    -daily_constraints["vitamin_d"][0], # Min vitamin D
    -daily_constraints["calcium"][0],   # Min calcium
    -daily_constraints["iron"][0],      # Min iron
    -daily_constraints["potassium"][0], # Min potassium
]

# Bounds for decision variables (non-negativity constraint)
x_bounds = [(0, None) for _ in cost]

# Solve the linear program
result = linprog(c=weekly_cost, A_ub=A, b_ub=b, bounds=x_bounds, method="highs")

print(result)