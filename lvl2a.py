import json
import networkx as nx
import numpy as np

def create_graph(neighbourhoods):
    G = nx.Graph()

    for neighborhood, data in neighbourhoods.items():
        G.add_node(neighborhood)

    for i, (source, data_source) in enumerate(neighbourhoods.items()):
        for j, (target, data_target) in enumerate(neighbourhoods.items()):
            if i != j:
                distance = data_source["distances"][j]
                G.add_edge(source, target, weight=distance)

    return G

def find_nearest_neighbourhood(restaurants, neighborhoods):
    restaurant_location = list(restaurants.keys())[0]
    distances = neighborhoods[restaurant_location]["distances"]
    nearest_neighbourhood_index = np.argmin(distances)
    nearest_neighbourhood = list(neighborhoods.keys())[nearest_neighbourhood_index]
    return nearest_neighbourhood

def solve_tsp(graph):
    return list(nx.approximation.traveling_salesman_problem(graph, cycle=True))

def optimize_delivery(input_data):
    neighborhoods = input_data["neighbourhoods"]
    restaurants = input_data["restaurants"]
    vehicles = input_data["vehicles"]
    delivery_slots = {}

    for vehicle_id, vehicle_data in vehicles.items():
        visited_nodes = set()
        graph = create_graph(neighborhoods)

        try:
            start_point = vehicle_data["start_point"]
        except KeyError:
            start_point = find_nearest_neighbourhood(restaurants, neighborhoods)

        tsp_path = solve_tsp(graph)
        vehicle_capacity = vehicle_data["capacity"]

        delivery_slots[vehicle_id] = {}
        path_count = 1
        current_path = []
        current_capacity = 0

        for i in range(len(tsp_path) - 1):
            location = tsp_path[i]
            next_location = tsp_path[i + 1]

            if location not in visited_nodes:
                order_quantity = neighborhoods[location]["order_quantity"]
                weight = order_quantity

                if current_capacity + weight > vehicle_capacity:
                    if current_path:
                        delivery_slots[vehicle_id]["path" + str(path_count)] = ["r0"] + current_path + ["r0"]
                        path_count += 1
                        current_path = []
                        current_capacity = 0

                current_path.append(location)
                current_capacity += weight
                visited_nodes.add(location)

        if current_path:
            delivery_slots[vehicle_id]["path" + str(path_count)] = ["r0"] + current_path + ["r0"]

    return delivery_slots

if __name__ == "__main__":
    input_file = r'C:\MockHackathon 6.1.24\Student Handout\Input data\level2a.json'
    with open(input_file, 'r') as f:
        input_data = json.load(f)

    optimized_delivery = optimize_delivery(input_data)

    output_file = 'level2a_output.json'
    with open(output_file, 'w') as f:
        json.dump(optimized_delivery, f, indent=2)
