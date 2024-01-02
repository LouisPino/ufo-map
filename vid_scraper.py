import json

video_ids = []

with open("vid_list.txt") as vid_list:
    video_ids = json.load(vid_list)

# Modify json to track which videos have (1) videos or not (0)

with open("Scrape2.json") as scrape2:
    scrape_data = json.load(scrape2)

for sighting in scrape_data["data"]:
    if sighting["id"] in video_ids:
        sighting["video"] = 1
    else:
        sighting["video"] = 0

with open("Scrape2.json", "w") as outfile:
            json.dump(scrape_data, outfile, indent=4)   



# videos are blocked by Muse.ai video hosting service. :( Will just have to link to pages that have videos :(