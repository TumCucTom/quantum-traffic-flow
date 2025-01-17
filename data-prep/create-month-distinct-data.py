import os
import csv
from collections import defaultdict

def combine_csv_files_by_month(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary to store data grouped by month-year (mm/yyyy)
    month_data = defaultdict(list)

    # Loop through all the CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            # Extract the date part (e.g., '3-21-2020.csv' -> '3-21-2020')
            date_part = filename.split('.')[0]  # Remove the .csv part

            # Get the 'mm/yyyy' part
            month, day, year = date_part.split('-')  # Split into [month, day, year]
            month_year = f"{int(month):02d}/{year}"  # Format month to be 2 digits, year is kept as 4 digits

            # Read the CSV file and add its data to the corresponding month
            with open(os.path.join(input_dir, filename), mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    month_data[month_year].append(row)

    # Combine and write the data for each month
    for month_year, combined_data in month_data.items():
        if combined_data:
            # Get all unique fieldnames from the combined data
            all_fieldnames = set()
            for row in combined_data:
                all_fieldnames.update(row.keys())

            all_fieldnames = list(all_fieldnames)  # Convert to list

            # Write the combined data to a new CSV file named by the month and year
            output_file = os.path.join(output_dir, f"{month_year.replace('/', '-')}.csv")

            with open(output_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=all_fieldnames)
                writer.writeheader()
                writer.writerows(combined_data)

            print(f"Created file for {month_year}: {output_file}")


input_directory = "../data/only-date-organised"  # Path to the folder containing date-organized CSV files
output_directory = "../data/only-month-organised"  # Output directory for month-organized CSV files

combine_csv_files_by_month(input_directory, output_directory)
