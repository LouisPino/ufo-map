import json
import sys

file_path = 'Scrape2.json'

with open(file_path, 'r') as file:
    data = json.load(file)

data_objs = data["data"]


# Print location for all sightings in given location
# Usage: python3 logger.py location NY
if sys.argv[1] == "location":
    for obj in data_objs:
        if f"{sys.argv[2]}, " in obj["location"]:
            print(obj["location"]) 


# Print amt of sightings
# Usage: python3 logger.py length
if sys.argv[1] == "length":
    print(len(data_objs))


# Print map with amt of sightings per country
# Usage: python3 logger.py country
if sys.argv[1] == "country":
    perCtry = {}
    for obj in data_objs:
        ctry = obj["location"].split(",")[2].capitalize()
        if ctry in perCtry.keys():
            perCtry[ctry]+=1
        else:
            perCtry[ctry]=1
    perCtry = dict(sorted(perCtry.items(), key=lambda item: item[1]))
    print(perCtry)


# Print all IDs of sightings from selected country
# Usage: python3 logger.py in Spain
if sys.argv[1] == "in":
    perCtry = {}
    for obj in data_objs:
        ctry = obj["location"].split(",")[2]
        if ctry in perCtry.keys():
            perCtry[ctry].append(obj)
        else:
            perCtry[ctry]=[obj]
    
    for sighting in perCtry[f" {sys.argv[2]}"]:
            print(f'{sighting["id"]}')

# Get amount with images
# Usage: python3 logger.py image
if sys.argv[1] == "image":
    img_count = 0
    for obj in data_objs:
        if len(obj["images"]) > 0:
            img_count += 1      
    print(img_count)


# Get IDs of sightings with videos
# Usage: python3 logger.py video
if sys.argv[1] == "video":
    vid_ids = []
    for obj in data_objs:
        if  "#museai-player" in obj["characteristics"]:
            vid_ids.append(obj["id"])
    print(vid_ids) 


# Print shapes map
# Usage: python3 logger.py shape

if sys.argv[1] == "shape":
    shapes = {}
    for obj in data_objs:
        shape = obj["shape"].lower()
        if shape in shapes.keys():
            shapes[shape]+=1
        else:
            shapes[shape]=1
    shapes = dict(sorted(shapes.items(), key=lambda item: item[1]))

    for key, value in shapes.items():    
        print(f"{key}: {value}")




# Print observers map
# Usage: python3 logger.py observer
if sys.argv[1] == "observer":
    obs_map = {}
    for obj in data_objs:
        observers = obj["observers"].lower()
        if observers in obs_map.keys():
            obs_map[observers]+=1
        else:
            obs_map[observers]=1
    obs_map = dict(sorted(obs_map.items(), key=lambda item: item[1]))

    for key, value in obs_map.items():    
        print(f"{key}: {value}")
