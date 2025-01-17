# CSV Data Processor for Major and Minor Roads

This script processes two CSV files containing data about major and minor roads. It groups the data by unique date and time and then outputs separate CSV files for each unique date and time into a specified directory.

## How It Works

1. **Input Files**: The script expects two CSV files:
    - `MajorRoads.csv` for major roads data
    - `MinorRoads.csv` for minor roads data

2. **Data Grouping**: The script combines data from both files based on the `dCount` (date) and `Hour` (time).

3. **Output Files**: For each unique combination of date and time, the script generates a new CSV file containing the combined data from both major and minor roads.

4. **Directory Creation**: If the output directory (`time-date-organised`) does not exist, the script will create it.

## Usage

1. **Prepare Your CSV Files**:
    - Place the `MajorRoads.csv` and `MinorRoads.csv` in the appropriate directory.

2. **Run the Script**:
    - Make sure the script is in the same directory as the CSV files, or modify the file paths accordingly.
    - Run the script in Python:
      ```bash
      python process_csv.py
      ```

3. **Output**: The script will create a new directory called `time-date-organised` and store the processed files there. Each file will be named by its unique date and time, e.g., `2003-04-08 7.csv`.

## Requirements
- Python 3.x
- CSV files in the format described above
