import pickle
import networkx as nx
from qiskit.optimization import QuadraticProgram
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit import Aer
from qiskit.utils import QuantumInstance

# Function to load a graph from a pickle file
def load_graph(pickle_file):
    with open(pickle_file, "rb") as f:
        return pickle.load(f)

# Function to create the optimization problem
def create_traffic_optimization_problem(mini_graph, max_graph):
    qp = QuadraticProgram()

    # Add variables for each edge in the mini graph
    for u, v, data in mini_graph.edges(data=True):
        qp.binary_var(f"x_{u}_{v}")

    # Objective: Minimize traffic overflow
    objective = 0
    for u, v, data in mini_graph.edges(data=True):
        traffic = data.get("weight", 0)
        max_traffic = max_graph.edges[u, v].get("weight", 1)
        overflow = max(traffic - max_traffic, 0)
        utilization = max_traffic - traffic

        # Objective term: penalize overflow, reward utilization
        objective += overflow * qp.get_var_by_name(f"x_{u}_{v}")
        objective -= utilization * qp.get_var_by_name(f"x_{u}_{v}")

    qp.minimize(objective)

    # Constraints: Ensure no more than max traffic is allocated
    for u, v, data in mini_graph.edges(data=True):
        max_traffic = max_graph.edges[u, v].get("weight", 1)
        qp.linear_constraint(
            linear={f"x_{u}_{v}": 1},
            sense="LE",
            rhs=max_traffic,
            name=f"capacity_constraint_{u}_{v}"
        )

    return qp

# Function to solve the problem with QAOA
def solve_with_qaoa(qp):
    backend = Aer.get_backend("aer_simulator")
    quantum_instance = QuantumInstance(backend)

    # Configure QAOA
    qaoa = QAOA(optimizer=COBYLA(maxiter=200), reps=3, quantum_instance=quantum_instance)
    result = qaoa.compute_minimum_eigenvalue(qp.to_ising()[0])

    # Extract the results
    solution = qp.interpret(result.eigenstate)
    return solution

# Main function
def main():
    # Load the graphs
    mini_graph = load_graph("mini_graph.pkl")
    max_graph = load_graph("max_graph.pkl")

    # Ensure both graphs share the same edges for the subset problem
    for u, v in mini_graph.edges:
        if not max_graph.has_edge(u, v):
            raise ValueError(f"Edge ({u}, {v}) in mini_graph not found in max_graph.")

    # Create the optimization problem
    qp = create_traffic_optimization_problem(mini_graph, max_graph)

    # Solve using QAOA
    solution = solve_with_qaoa(qp)

    # Output the solution
    print("Optimized Traffic Allocation:")
    for u, v, data in mini_graph.edges(data=True):
        edge_var = f"x_{u}_{v}"
        print(f"Edge ({u}, {v}): Allocated Traffic = {solution[edge_var]}")

if __name__ == "__main__":
    main()
