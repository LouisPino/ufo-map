import json

file_path = 'Scrape1.json'

# Open the file and read the JSON data
with open(file_path, 'r') as file:
    data = json.load(file)

# Now 'data' contains the JSON data.
# You can print it or perform other operations.
data_objs = data["data"]


# Print location for all sightings in NY
# for obj in data_objs:
#     if "NY, " in obj["location"]:
#         print(obj["location"]) 



# Print amt of sightings
# print(len(data_objs))


# Print hash map with amt of sightings per country
# perCtry = {}
# for obj in data_objs:
#     ctry = obj["location"].split(",")[2]
#     if ctry in perCtry.keys():
#         perCtry[ctry]+=1
#     else:
#         perCtry[ctry]=1
# perCtry = dict(sorted(perCtry.items(), key=lambda item: item[1]))

# for key, value in perCtry.items():
#     # uncomment line below to see only one country / specify a rule
#     # if key == " USA":     
#          print(f"{key}: {value}")



# Print all IDs of sightings from selected contry
# perCtry = {}
# for obj in data_objs:
#     ctry = obj["location"].split(",")[2]
#     if ctry in perCtry.keys():
#         perCtry[ctry].append(obj)
#     else:
#         perCtry[ctry]=[obj]
#  
# for sighting in perCtry[" Italy"]:
#          print(f'{sighting["id"]}')

# Get amount with images
img_count = 0
first_image = 0
for obj in data_objs:
    if len(obj["images"]) > 0:
        img_count += 1
        if first_image == 0:
            first_image = obj["id"]
            
print(img_count)
print(first_image)