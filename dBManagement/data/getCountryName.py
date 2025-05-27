import json
import os

# Get the directory where the country.json file is located
json_file_path = "./dBManagement/data/country.json"
json_dir = os.path.dirname(json_file_path)

# Open and read the JSON file
with open(json_file_path, "r") as file:
    data = json.load(file)

# Extract the 'name' field from each item in the JSON
names = [item["name"] for item in data]

# Define the output file path in the same directory
output_file_path = os.path.join(json_dir, "country_names.txt")

# Write the names to a text file (overwriting the file)
with open(output_file_path, "w") as file:
    for name in names:
        file.write(name + "\n")

print(f"Names have been written to '{output_file_path}'.")
