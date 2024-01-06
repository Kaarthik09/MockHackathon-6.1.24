import numpy as np
from tsp_solver.greedy import solve_tsp

def solve_knapsack(weights, values, capacity):
    n = len(weights)
    dp = np.zeros((n + 1, capacity + 1))

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)
            w -= weights[i - 1]
        i -= 1

    return selected_items

def optimize_delivery(input_data):
    # Convert distances to a regular Python list
    distances = list(input_data["neighbourhoods"]["n0"]["distances"])
    tsp_solution = solve_tsp(distances)

    vehicle_capacity = input_data["vehicles"]["v0"]["capacity"]
    delivery_slots = []

    for location in tsp_solution:
        order_quantities = [input_data["neighbourhoods"][f"n{location}"]["order_quantity"] for location in tsp_solution]

        # Assume weights and values are the same for simplicity
        weights = order_quantities
        values = order_quantities

        knapsack_solution = solve_knapsack(weights, values, vehicle_capacity)

        # Add the current delivery slot
        delivery_slots.append({
            "location": location,
            "orders": knapsack_solution
        })

    return delivery_slots

if __name__ == "__main__":
    # Load your input data from the JSON file
    import json
    input_file = 'C:\\MockHackathon 6.1.24\\Student Handout\\Input data\\level1a.json'
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    # Optimize the delivery
    optimized_delivery = optimize_delivery(input_data)

    # Display the optimized delivery slots
    print(optimized_delivery)

