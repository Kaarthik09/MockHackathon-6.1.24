#import pandas as pd
#df = pd.read_json('C:\MockHackathon 6.1.24\Student Handout\Input data\level0.json')
#print(df.neighbourhoods.n0)
import networkx as nx
import json

def create_adjacency_matrix(input_data):
    n_neighbourhoods = input_data["n_neighbourhoods"]
    neighbourhoods = input_data["neighbourhoods"]

    adjacency_matrix = [[float("inf")] * n_neighbourhoods for _ in range(n_neighbourhoods)]

    for i in range(n_neighbourhoods):
        for j in range(n_neighbourhoods):
            if i != j:
                adjacency_matrix[i][j] = neighbourhoods[f"n{i}"]["distances"][j]

    return adjacency_matrix

def tsp(adjacency_matrix):
    G = nx.Graph()

    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[i])):
            G.add_edge(i, j, weight=adjacency_matrix[i][j])

    optimal_path = list(nx.approximation.traveling_salesman_problem(G, cycle=True))

    cost = sum(adjacency_matrix[optimal_path[i]][optimal_path[i + 1]] for i in range(len(optimal_path) - 1))

    return optimal_path, cost

def save_output_to_json(output_path, vehicle_name, path, cost):
    output_data = {vehicle_name: {"path": path, "cost": cost}}
    with open(output_path, "w") as output_file:
        json.dump(output_data, output_file, indent=2)

if __name__ == "__main__":
    input_file_path = r"C:\MockHackathon 6.1.24\Student Handout\Input data\level0.json"
    with open(input_file_path, "r") as file:
        input_data = json.load(file)

    adjacency_matrix = create_adjacency_matrix(input_data)
    optimal_path, cost = tsp(adjacency_matrix)

    print("Optimal Path:", optimal_path)
    print("Cost:", cost)

    output_file_path = 'lvl0output.json'
    save_output_to_json(output_file_path, "v0", optimal_path, cost)


