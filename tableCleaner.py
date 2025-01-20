import csv

# Input and output file paths
input_file = "data.csv"
output_file = "output.csv"

# Read the CSV and filter out incomplete rows
with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Write the header row to the output file
    header = next(reader)
    writer.writerow(header)

    # Iterate through rows and keep only fully complete ones
    for row in reader:
        if all(row):  # Checks if all fields in the row are non-empty
            writer.writerow(row)

print(f"Filtered rows have been saved to {output_file}.")
