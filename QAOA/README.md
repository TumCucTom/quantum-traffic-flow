# **QAOA for Traffic Flow Optimization**

This project implements a Quantum Approximate Optimization Algorithm (QAOA) to optimize traffic flow using two graphs:
- A **mini graph** representing the current traffic state.
- A **max graph** representing the maximum traffic capacity of roads.

The algorithm minimizes traffic overflow while rewarding efficient utilization of the road network.

---

## **Problem Description**

We aim to optimize the allocation of traffic on roads by minimizing overflow and maximizing utilization. Each road is represented as an edge in the graph, and the traffic conditions are modeled as follows:

- **Mini Graph (Current Traffic):**  
  Each edge \( (u, v) \) has a weight \( \text{traffic}_{uv} \), representing the current traffic on the road.

- **Max Graph (Capacity):**  
  Each edge \( (u, v) \) has a weight \( \text{capacity}_{uv} \), representing the maximum traffic the road can handle.

---

## **Optimization Problem**

### **Objective:**
The goal is to minimize traffic overflow and reward underutilization:

\[
\text{Minimize:} \quad \sum_{(u, v) \in E} \left[ \max( \text{traffic}_{uv} - \text{capacity}_{uv}, 0 ) \cdot x_{uv} \right] - \sum_{(u, v) \in E} \left[ (\text{capacity}_{uv} - \text{traffic}_{uv}) \cdot x_{uv} \right]
\]

Where:
- \( x_{uv} \) is a binary decision variable (\( x_{uv} = 1 \) if traffic is allocated, 0 otherwise).
- \( \max( \text{traffic}_{uv} - \text{capacity}_{uv}, 0 ) \): Traffic overflow penalty.
- \( \text{capacity}_{uv} - \text{traffic}_{uv} \): Utilization reward.

### **Constraints:**
Ensure that allocated traffic does not exceed the road's capacity:

\[
x_{uv} \cdot \text{traffic}_{uv} \leq \text{capacity}_{uv}, \quad \forall (u, v) \in E
\]

---

## **Hamiltonian Setup**

To solve this optimization problem using QAOA, we represent it as a Hamiltonian:

### **Cost Hamiltonian:**

\[
H_C = \sum_{(u, v) \in E} \left[ \max( \text{traffic}_{uv} - \text{capacity}_{uv}, 0 ) \cdot Z_{uv} - (\text{capacity}_{uv} - \text{traffic}_{uv}) \cdot Z_{uv} \right]
\]

Where \( Z_{uv} \) is the Pauli-Z operator acting on the qubit corresponding to edge \( (u, v) \).

### **Mixer Hamiltonian:**

The mixer Hamiltonian promotes transitions between feasible configurations:
\[
H_M = \sum_{(u, v) \in E} X_{uv}
\]
Where \( X_{uv} \) is the Pauli-X operator.

## **Setup Instructions**

### **Dependencies**

Install the required libraries using pip:

```bash
pip install qiskit networkx
```

### **Run the Script**

Place the `mini_graph.pkl` and `max_graph.pkl` files in the same directory as the script, then run:

```bash
python optimize_traffic_qaoa.py
```

---

## **How It Works**

1. **Graph Loading:**  
   The script loads `mini_graph.pkl` and `max_graph.pkl`.

2. **Problem Formulation:**  
   The optimization problem is constructed using Qiskit’s `QuadraticProgram`.

3. **QAOA Execution:**  
   The Quadratic Program is converted into an Ising model and solved using QAOA.

4. **Results:**  
   The optimized traffic allocation is printed for each road.

---

## **Example Output**

```
Optimized Traffic Allocation:
Edge (A, B): Allocated Traffic = 1
Edge (B, C): Allocated Traffic = 0
Edge (C, D): Allocated Traffic = 1
```

---

## **Future Enhancements**
- Support for dynamic traffic adjustment based on real-time inputs.
- Integration with a classical optimizer to benchmark results.
- Visualization of traffic flow on the graph.

---

