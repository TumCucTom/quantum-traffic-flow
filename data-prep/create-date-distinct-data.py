import os
import csv
from collections import defaultdict

def process_csv_files_by_day(major_csv, minor_csv, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize dictionaries to store data grouped by date
    major_data_by_day = defaultdict(list)
    minor_data_by_day = defaultdict(list)

    # Read the major roads CSV and organize data by date
    with open(major_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['dCount']  # Use only the date part
            major_data_by_day[date].append(row)

    # Read the minor roads CSV and organize data by date
    with open(minor_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row['dCount']  # Use only the date part
            minor_data_by_day[date].append(row)

    # Combine the data from both files and write it to separate files
    all_dates = set(major_data_by_day.keys()).union(set(minor_data_by_day.keys()))

    for date in all_dates:
        combined_data = major_data_by_day.get(date, []) + minor_data_by_day.get(date, [])

        # Get all unique fieldnames from both major and minor data
        all_fieldnames = set()
        for row in combined_data:
            all_fieldnames.update(row.keys())

        all_fieldnames = list(all_fieldnames)  # Convert to list

        # Write the combined data to a new CSV file named by the date
        output_file = os.path.join(output_dir, f"{date.replace('/', '-')}.csv")

        if combined_data:
            with open(output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=all_fieldnames)
                writer.writeheader()
                writer.writerows(combined_data)

        print(f"Created file for {date}: {output_file}")


major_csv_file = "../data/DFT Counts 21-02-2017(MajorRoads).csv"  # Path to the major roads CSV file
minor_csv_file = "../data/DFT Counts 21-02-2017(MinorRoads).csv"  # Path to the minor roads CSV file
output_directory = "../data/only-date-organised"  # Output directory

process_csv_files_by_day(major_csv_file, minor_csv_file, output_directory)
