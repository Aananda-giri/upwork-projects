import csv
import glob

# List all CSV files in the directory
csv_files = glob.glob("*.csv")  # Adjust the pattern if needed to specify a path

# Name of the combined CSV file
output_file = "combined_inactive_subreddits.csv"

# Set to keep track of seen subreddits
seen_subreddits = set()   # To avoid duplicate subreddits

# Open the output file in write mode
with open(output_file, 'w', newline='') as outfile:
    writer = None

    # Iterate over each CSV file
    for i, file in enumerate(csv_files):
        with open(file, 'r', newline='') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Read the header from each file

            # Write the header only for the first file
            if i == 0:
                writer = csv.writer(outfile)
                writer.writerow(header)  # Write header once

            for row in reader:
                if row[0] not in seen_subreddits:
                    writer.writerow(row)
                    seen_subreddits.add(row[0])

            # # Write all rows from the current file
            # writer.writerows(row for row in reader)

print(f"Combined CSV file created: {output_file}")



# --------------------------
# Short by members count
# --------------------------

# Input and output file names
input_file = 'combined_inactive_subreddits.csv'
output_file = 'shorted_inactive_subreddits_with_members_count.csv'

# Read the input CSV file and sort by 'Members-Count'
with open(input_file, 'r', newline='') as infile:
    reader = csv.DictReader(infile)
    
    # Sort rows by 'Members-Count' (converted to integer)
    sorted_rows = sorted(reader, key=lambda row: int(row['Members-Count']), reverse=True)

    # Write the sorted data to the new CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write sorted rows
        writer.writerows(sorted_rows)

print(f"Sorted data saved to {output_file}.")