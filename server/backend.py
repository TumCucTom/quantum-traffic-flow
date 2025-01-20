from flask import Flask, request, jsonify
import pickle
import os
import networkx as nx
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from QAOA.algorithm import main as run_qaoa

app = Flask(__name__)

# Load initial graphs
mini_graph_path = "mini_graph.pkl"
max_graph_path = "../graph-prep/max_graph.pkl"

# Ensure the graphs exist
if not os.path.exists(mini_graph_path) or not os.path.exists(max_graph_path):
    raise FileNotFoundError("Required graph files not found.")

with open(max_graph_path, "rb") as f:
    max_graph = pickle.load(f)

# Endpoint to run the optimization algorithm
@app.route("/optimise", methods=["POST"])
def optimise():
    try:
        # Run QAOA and optimization logic from the algorithm.py script
        result = run_qaoa()
        return jsonify({"success": True, "message": "Optimization completed.", "result": result})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Endpoint to update the mini graph
@app.route("/update-mini-graph", methods=["POST"])
def update_mini_graph():
    data = request.json
    csv_file = data.get("csv_file")

    if not csv_file or not os.path.exists(csv_file):
        return jsonify({"success": False, "message": "Invalid or missing CSV file."}), 400

    try:
        mini_graph = process_roads_csv(csv_file)

        # Save the updated mini graph
        with open(mini_graph_path, "wb") as f:
            pickle.dump(mini_graph, f)

        return jsonify({"success": True, "message": "Mini graph updated successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def process_roads_csv(csv_file):
    """Process a CSV file to create a NetworkX graph."""
    graph = nx.Graph()
    VEHICLE_TYPES = ["PC", "2WMV", "CAR", "BUS", "LGV", "HGVR2", "HGVR3", "HGVR4", "HGVA3", "HGVA5", "HGVA6"]

    def create_junction_id(easting, northing):
        return f"{easting}_{northing}"

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            junction_a = create_junction_id(row.get("A Ref E", row.get("S Ref E")), row.get("A Ref N", row.get("S Ref N")))
            junction_b = create_junction_id(row.get("B Ref E", row.get("S Ref E")), row.get("B Ref N", row.get("S Ref N")))

            graph.add_node(junction_a)
            graph.add_node(junction_b)

            for vehicle_type in VEHICLE_TYPES:
                try:
                    count = int(row[vehicle_type])
                except (ValueError, KeyError):
                    continue

                graph.add_edge(junction_a, junction_b, vehicle_type=vehicle_type, weight=count)

    return graph

if __name__ == "__main__":
    app.run(debug=True)
