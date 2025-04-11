import json
import os

current_working_directory = os.getcwd()

print(f"The current working directory is: {current_working_directory}")

# Open and read the JSON file
with open("./dBManagement/country.json", "r") as file:
    data = json.load(file)

# Extract the 'name' field from each item in the JSON
names = [item["name"] for item in data]

# Print the result
print(names)
