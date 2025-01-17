import csv
import networkx as nx
import pickle

# Function to create a unique junction identifier based on coordinates
def create_junction_id(easting, northing):
    return f"{easting}_{northing}"

# Vehicle types in the dataset
VEHICLE_TYPES = ["PC", "2WMV", "CAR", "BUS", "LGV", "HGVR2", "HGVR3", "HGVR4", "HGVA3", "HGVA5", "HGVA6"]

# Function to process the CSV for minor roads
def process_minor_roads_csv(csv_file, graph, max_weights):
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract junctions
            junction_a = create_junction_id(row["S Ref E"], row["S Ref N"])
            junction_b = create_junction_id(row["S Ref E"], row["S Ref N"])  # You might need different logic if "B Ref E" and "B Ref N" are also present for minor roads

            # Ensure nodes exist in the graph
            graph.add_node(junction_a)
            graph.add_node(junction_b)

            # Process each vehicle type
            for vehicle_type in VEHICLE_TYPES:
                # Edge key includes junctions and vehicle type
                edge_key = (junction_a, junction_b, vehicle_type)

                # Convert count to integer or skip if invalid
                try:
                    count = int(row[vehicle_type])
                except ValueError:
                    continue

                # Update the maximum weight for this edge and vehicle type
                if edge_key not in max_weights:
                    max_weights[edge_key] = count
                else:
                    max_weights[edge_key] = max(max_weights[edge_key], count)

    # Add edges to the graph with the computed max weights
    for (junction_a, junction_b, vehicle_type), weight in max_weights.items():
        graph.add_edge(junction_a, junction_b, vehicle_type=vehicle_type, weight=weight)

# Function to process the major roads CSV
def process_major_roads_csv(csv_file):
    graph = nx.Graph()
    max_weights = {}

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract junctions
            junction_a = create_junction_id(row["A Ref E"], row["A Ref N"])
            junction_b = create_junction_id(row["B Ref E"], row["B Ref N"])

            # Ensure nodes exist in the graph
            graph.add_node(junction_a)
            graph.add_node(junction_b)

            # Process each vehicle type
            for vehicle_type in VEHICLE_TYPES:
                # Edge key includes junctions and vehicle type
                edge_key = (junction_a, junction_b, vehicle_type)

                # Convert count to integer or skip if invalid
                try:
                    count = int(row[vehicle_type])
                except ValueError:
                    continue

                # Update the maximum weight for this edge and vehicle type
                if edge_key not in max_weights:
                    max_weights[edge_key] = count
                else:
                    max_weights[edge_key] = max(max_weights[edge_key], count)

    # Add edges to the graph with the computed max weights
    for (junction_a, junction_b, vehicle_type), weight in max_weights.items():
        graph.add_edge(junction_a, junction_b, vehicle_type=vehicle_type, weight=weight)

    return graph, max_weights

# Path to the CSV files
major_roads_csv = "../data/DFT Counts 21-02-2017(MajorRoads).csv"
minor_roads_csv = "../data/DFT Counts 21-02-2017(MinorRoads).csv"  # Replace with actual path

# Process the major roads CSV
graph, max_weights = process_major_roads_csv(major_roads_csv)

# Process the minor roads CSV and add to the existing graph
process_minor_roads_csv(minor_roads_csv, graph, max_weights)

# Save the graph in Pickle format
with open("max_graph.pkl", "wb") as f:
    pickle.dump(graph, f)

# Print a basic summary of the combined graph
print(f"Nodes: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")
print(f"First 5 nodes: {list(graph.nodes())[:5]}")
print(f"First 5 edges with weights: {list(graph.edges(data=True))[:5]}")
