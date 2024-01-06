import json
import networkx as nx

def create_graph(neighbourhoods):
    G = nx.Graph()

    for neighborhood, data in neighbourhoods.items():
        G.add_node(neighborhood, visited=False)

    for i, (source, data_source) in enumerate(neighbourhoods.items()):
        for j, (target, data_target) in enumerate(neighbourhoods.items()):
            if i != j:
                distance = data_source["distances"][j]
                G.add_edge(source, target, weight=distance)

    return G

def solve_tsp(graph):
    tsp_path = nx.approximation.traveling_salesman_problem(graph, cycle=True)
    return tsp_path

def solve_knapsack(locations, weights, values, capacity):
    n = len(weights)
    dp = [[{"path": [], "value": 0, "weight": 0} for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                include_current = {"path": dp[i - 1][w - weights[i - 1]]["path"] + [locations[i - 1]],
                                   "value": dp[i - 1][w - weights[i - 1]]["value"] + values[i - 1],
                                   "weight": dp[i - 1][w - weights[i - 1]]["weight"] + weights[i - 1]}
                exclude_current = dp[i - 1][w]

                if include_current["value"] > exclude_current["value"]:
                    dp[i][w] = include_current
                else:
                    dp[i][w] = exclude_current
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

def optimize_delivery(input_data):
    neighborhoods = input_data["neighbourhoods"]
    graph = create_graph(neighborhoods)
    tsp_path = solve_tsp(graph)

    vehicle_capacity = input_data["vehicles"]["v0"]["capacity"]
    delivery_slots = {"v0": {}}
    path_count = 1

    for i in range(len(tsp_path) - 1):
        location = tsp_path[i]
        next_location = tsp_path[i + 1]

        if not graph.nodes[location]['visited']:
            order_quantities = [neighborhoods[location]["order_quantity"]]
            weights = order_quantities
            values = order_quantities

            # Check if the current location has been visited in previous paths
            for path in delivery_slots["v0"].values():
                if location in path:
                    break
            else:
                knapsack_solution = solve_knapsack([location], weights, values, vehicle_capacity)

                # Mark the current node as visited
                graph.nodes[location]['visited'] = True

                # Add the current delivery path to the output
                delivery_slots["v0"]["path" + str(path_count)] = knapsack_solution["path"] + [next_location]
                path_count += 1

    return delivery_slots

if __name__ == "__main__":
    input_file = r'C:\MockHackathon 6.1.24\Student Handout\Input data\level1a.json'
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    optimized_delivery = optimize_delivery(input_data)

    output_file = 'lvl1aoutput.json'
    with open(output_file, 'w') as f:
        json.dump(optimized_delivery, f, indent=2)
