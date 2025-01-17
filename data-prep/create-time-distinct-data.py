import os
import csv
from collections import defaultdict

def process_csv_files(major_csv, minor_csv, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize dictionaries to store data grouped by date and time
    major_data = defaultdict(list)
    minor_data = defaultdict(list)

    # Read the major roads CSV and organize data by date and time
    with open(major_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_time = row['dCount'] + " " + row['Hour']  # Combine date and time
            major_data[date_time].append(row)

    # Read the minor roads CSV and organize data by date and time
    with open(minor_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_time = row['dCount'] + " " + row['Hour']  # Combine date and time
            minor_data[date_time].append(row)

    # Combine the data from both files and write it to separate files
    all_dates_times = set(major_data.keys()).union(set(minor_data.keys()))

    for date_time in all_dates_times:
        combined_data = major_data.get(date_time, []) + minor_data.get(date_time, [])

        # Get all unique fieldnames from both major and minor data
        all_fieldnames = set()
        for row in combined_data:
            all_fieldnames.update(row.keys())

        all_fieldnames = list(all_fieldnames)  # Convert to list

        # Write the combined data to a new CSV file named by date and time
        output_file = os.path.join(output_dir, f"{date_time.replace('/', '-').replace(':', '-')}.csv")

        if combined_data:
            with open(output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=all_fieldnames)
                writer.writeheader()
                writer.writerows(combined_data)

        print(f"Created file for {date_time}: {output_file}")


major_csv_file = "../data/DFT Counts 21-02-2017(MajorRoads).csv"  # Path to the major roads CSV file
minor_csv_file = "../data/DFT Counts 21-02-2017(MinorRoads).csv"  # Path to the minor roads CSV file
output_directory = "../data/time-date-organised"  # Output directory

process_csv_files(major_csv_file, minor_csv_file, output_directory)
