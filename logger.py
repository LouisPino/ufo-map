import json

file_path = 'thirtyK.json'

# Open the file and read the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Now 'data' contains the JSON data.
# You can print it or perform other operations.
data_objs = data["data"]

for obj in data_objs:
    if "NY, " in obj["location"]:
        print(obj["location"]) 




