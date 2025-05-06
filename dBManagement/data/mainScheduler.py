import json
import os


class mainScheduler:
    #Time Constants
    CLASS_A = 15
    CLASS_B = 30
    CLASS_C = 45
    CLASS_D = 60
    CLASS_E = 75
    CLASS_F = 90

    def __init__(self):
        # Get the directory where the country.json file is located
        json_file_path = "./dBManagement/data/classCategory.json"
        #json_dir = os.path.dirname(json_file_path)

        # Open and read the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        print(data['classA'])

if __name__ == "__main__":
    print("Running Locally")
    mainScheduler()