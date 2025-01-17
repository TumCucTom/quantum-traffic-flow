# Backend Server for Traffic Optimization

This backend server provides a Python-based implementation for optimizing traffic allocation using Quantum Approximate Optimization Algorithm (QAOA). It allows you to:

1. Upload and update a `mini_graph` from a CSV file.
2. Run traffic optimization between a `mini_graph` (current traffic) and a `max_graph` (maximum allowable traffic).

## Features

- **Load Graphs**: Load preprocessed `mini_graph` and `max_graph` data from pickle files.
- **Update Mini Graph**: Update the `mini_graph` by providing a CSV file representing the current traffic data.
- **Optimize Traffic Allocation**: Run QAOA to minimize overflow and maximize utilization of road capacity.

## Endpoints

### 1. `/update-mini-graph`
- **Method**: POST
- **Description**: Updates the `mini_graph` by processing a given CSV file.
- **Input**: JSON payload with a `csv_file` parameter indicating the file path.
- **Response**: Status message indicating success or failure.

### 2. `/optimise`
- **Method**: GET
- **Description**: Runs the QAOA-based optimization algorithm using the `mini_graph` and `max_graph`.
- **Response**: A JSON object containing optimized traffic allocation per edge in the `mini_graph`.

## Dependencies

- Python 3.8+
- Libraries:
    - Flask
    - NetworkX
    - Qiskit
    - Pickle

## Setup Instructions

1. Start the server:
   ```bash
   python backend_server.py
   ```

2. Use the API endpoints to update the `mini_graph` and perform optimization.

## Files

- `backend_server.py`: Main server script.
- `algorithm.py`: Contains QAOA logic for traffic optimization.
- `mini_graph.pkl`: Initial pickle file for the `mini_graph`.
- `max_graph.pkl`: Pickle file for the `max_graph`.

## Example Usage

### Update Mini Graph
Send a POST request to `/update-mini-graph` with the path to a CSV file:
```json
{
  "csv_file": "path/to/mini_graph.csv"
}
```

### Run Optimization
Send a GET request to `/optimise` to get the optimized traffic allocation.

## License
This project is licensed under the MIT License.

