
# Graph Creation and Data Import for Road Networks

## Overview
This script processes CSV files containing traffic data for both major and minor roads and creates a graph representation of the road network using the NetworkX library. The graph nodes represent junctions (locations), and the edges represent road segments connecting those junctions, with weights based on traffic data for different vehicle types. The script combines data from two CSV files, one for major roads and one for minor roads, and saves the resulting graph in a Pickle file format for future use.

## Features
- Processes CSV files for both major and minor roads.
- Creates a graph with junctions as nodes and road segments as weighted edges.
- Supports multiple vehicle types: PC, 2WMV, CAR, BUS, LGV, and various HGV categories.
- Outputs a combined graph stored in Pickle format (`combined_graph.pkl`).
- Provides basic graph summary (number of nodes, edges, first few nodes, and edges).

## Requirements
- Python 3.x
- NetworkX library (for graph creation and manipulation)
- CSV files with traffic data for major and minor roads

### Install Dependencies
To install the required dependencies, you can use `pip`:
```bash
pip install networkx
```

## CSV File Format

### Major Roads CSV
The major roads CSV should have the following columns:
- `A Ref E`, `A Ref N`: Easting and Northing coordinates for the first junction (A).
- `B Ref E`, `B Ref N`: Easting and Northing coordinates for the second junction (B).
- Vehicle type columns such as `PC`, `2WMV`, `CAR`, `BUS`, `LGV`, `HGVR2`, etc. representing the traffic counts.

### Minor Roads CSV
The minor roads CSV should have similar columns, but the coordinates may need to be adjusted depending on the data structure. The script assumes that the junction coordinates (`S Ref E`, `S Ref N`) are consistent with the major roads format.

## How to Use

1. **Prepare the CSV files**:
   - Make sure the CSV files are properly formatted and contain the necessary traffic count data for both major and minor roads.
   - Ensure the file paths for the CSV files are correct.

2. **Run the Script**:
   - The script will read the data from the provided CSV files (`DFT Counts 21-02-2017(MajorRoads).csv` for major roads and `MinorRoads.csv` for minor roads).
   - The graph will be created and saved as `combined_graph.pkl` using Pickle format.

   Example:
   ```bash
   python create_road_network_graph.py
   ```

3. **Graph Summary**:
   After running the script, a basic summary of the graph will be printed to the console, including the number of nodes, edges, and the first few nodes and edges with their weights.

4. **Load the Graph**:
   Once the graph is created, it can be loaded from the Pickle file for further analysis or manipulation:
   ```python
   import pickle

   with open("combined_graph.pkl", "rb") as f:
       graph = pickle.load(f)

   # Now you can work with the graph object
   ```

## File Paths
Make sure to update the file paths in the script for your specific data files. The paths are set to:
- `major_roads_csv = "../data/DFT Counts 21-02-2017(MajorRoads).csv"`
- `minor_roads_csv = "../data/MinorRoads.csv"`

Adjust them based on the actual location of your CSV files.

## Example Output
```bash
Nodes: 1000
Edges: 1500
First 5 nodes: ['333990_158570', '333991_158570', '333990_158571', '333991_158571', '333992_158570']
First 5 edges with weights: [
    ('333990_158570', '333991_158570', {'vehicle_type': 'PC', 'weight': 100}),
    ('333991_158570', '333992_158570', {'vehicle_type': '2WMV', 'weight': 50}),
    ...
]
```

## Troubleshooting
- **Missing CSV Columns**: Ensure that all necessary columns (`A Ref E`, `A Ref N`, `B Ref E`, `B Ref N`, and vehicle type columns) are present in the CSV files.
- **File Path Issues**: If the CSV files are not found, check that the file paths are correct relative to the script’s location.
- **Graph Errors**: If there are issues with graph creation, ensure that the junction identifiers are being generated correctly based on the coordinates.
