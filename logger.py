import json

file_path = 'Scrape1.json'

with open(file_path, 'r') as file:
    data = json.load(file)

data_objs = data["data"]


# # Print location for all sightings in NY
# for obj in data_objs:
#     if "NY, " in obj["location"]:
#         print(obj["location"]) 


# # Print amt of sightings
# print(len(data_objs))


# # Print hash map with amt of sightings per country
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



# # Print all IDs of sightings from selected contry
# perCtry = {}
# for obj in data_objs:
#     ctry = obj["location"].split(",")[2]
#     if ctry in perCtry.keys():
#         perCtry[ctry].append(obj)
#     else:
#         perCtry[ctry]=[obj]
 
# for sighting in perCtry[" Spain"]:
#          print(f'{sighting["id"]}')

# Get amount with images
# img_count = 0
# for obj in data_objs:
#     if len(obj["images"]) > 0:
#         img_count += 1      
# print(img_count)

# Get IDs of sightings with videos
# vid_ids = []
# for obj in data_objs:
#     if  "#museai-player" in obj["characteristics"]:
#         vid_ids.append(obj["id"])
# print(vid_ids)

# write to file if needed
# # with open("vid_list.txt", "w") as outfile:
# #     json.dump(vid_ids, outfile, indent=4)   