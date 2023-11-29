from bs4 import BeautifulSoup
import json
import aiohttp
from aiohttp import ClientError
import asyncio
import datetime
import math
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #FOR WINDOWS ONLY

LAST_ID = 179135
PREV_ID = 0
BATCH_SIZE = 50

base_url = "https://nuforc.org/sighting/?id="
file_path = "test.json"

# open specified json file as data_dict
try:
    with open(file_path, "r") as file:
        data_dict = json.load(file)
except FileNotFoundError:
    data_dict = {"data": []}

def remove_leading_newlines(string):
    return string.lstrip('\n \r\t')

# Function to collect html from one page
async def fetch_data(session, id, retry_count=3, delay=1):
    url = f"https://nuforc.org/sighting/?id={id}"
    for attempt in range(retry_count):
        try:
            async with session.get(url) as resp:
                content_type = resp.headers.get('Content-Type', '').lower()
                if 'application/json' in content_type:
                    return await resp.json()  # JSON response
                elif 'text/html' in content_type:
                    html_content = await resp.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    return soup
                else:
                    raise ValueError(f'Unexpected content type: {content_type}')
        except (ClientError, asyncio.TimeoutError) as e:
                if attempt < retry_count - 1:
                    await asyncio.sleep(delay)
                    delay *= 2  # Double the delay for the next retry
                else:
                    raise e  # Reraise the exception after the last retry

# Loop through all pages, fetching and writing 1000 at a time
async def main():
    start_time = datetime.datetime.now()
    count = 179134
    while count < LAST_ID:
        async with aiohttp.ClientSession() as session:
            # Fetch data for each ID from current to current+1000
            results = await asyncio.gather(
                *[fetch_data(session, id) for id in range(count, count + BATCH_SIZE)]
            )
            # Process results after all fetches are complete
            for idx, result in enumerate(results):
                    print(idx + PREV_ID)
                    new_entry = str(result.find("div", class_="content-area"))
                    new_imgs = result.find_all("img")
                    img_links = []
                    try:
                        id = str(result.find("h1")).split("NUFORC Sighting ")[1].split("</h1>")[0]
                    except:
                        id = "999999"
                    for i in range(1, len(new_imgs)):
                        img = str(new_imgs[i]).split("src=")[1].split('"')[1]
                        img_links.append(img)
                    # new_vids = result.find_all("div", class_="content-area")
                    # vid_links = []
                    # for i in range(0, len(new_vids)):
                    #     vid = str(new_vids[i]).split("src=")[1].split('"')[1]
                    #     print(vid)
                    #     vid_links.append(vid)
                    
                    # create new dict with all the info from the html
                    try:
                        new_dict = {
                            "id": id,
                            "occurred": new_entry.split("<b>Occurred:</b> ")[1].split(" Local<br/>")[0] if "Occurred" in new_entry else "",
                            "location": new_entry.split("<b>Location:</b> ")[1].split("<br/>")[0] if "Location" in new_entry else "",
                            "location_details": new_entry.split("details:</b> ")[1].split("<br/>")[0] if "Location details" in new_entry else "",
                            "shape": new_entry.split("<b>Shape:</b> ")[1].split("<br/>")[0] if "Shape" in new_entry else "",
                            "duration": new_entry.split("<b>Duration:</b> ")[1].split("<br/>")[0] if "Duration" in new_entry else "",
                            "observers": new_entry.split("<b>No of observers:</b> ")[1].split("<br/>")[0] if "No of observers" in new_entry else "",
                            "reported": new_entry.split("<b>Reported:</b> ")[1].split("<br/>")[0] if "Reported" in new_entry else "",
                            "posted": new_entry.split("<b>Posted:</b> ")[1].split("<br/>")[0] if "Posted" in new_entry else "",
                            "characteristics": new_entry.split("<b>Posted:</b> ")[1].split("<p style=\"color: white;")[0].split("<img")[0].replace("<br/>", "\n").replace("<br>", "\n").replace("<b>Posted:</b> ", "").replace("<b>Characteristics:</b> ", "")[19:],   
                            "explanation": new_entry.split("<b>Explanation:</b>")[1].split("<br/>")[0] if "Explanation" in new_entry else "",
                            "images": img_links,
                            # "videos": vid_links,
                            }
                    # ignore and move on if something goes wrong
                    except:
                        continue
                    
                    # extra parsing on characteristics field
                    if "<b>Explanation:</b>" in new_dict["characteristics"]:
                        new_dict["characteristics"] = " ".join(new_dict["characteristics"][20:].split("\n")[1:])
                    new_dict["characteristics"] = remove_leading_newlines(new_dict["characteristics"])
                 
                    # If it has an occurred date and location, add it to array of dicts   
                    if new_dict["occurred"] != "" and new_dict["location"] != ", , ":
                        data_dict["data"].append(new_dict)

        #   Write entire data_dict object to json (including the original data from import)
        with open(file_path, "w") as outfile:
            json.dump(data_dict, outfile, indent=4)   
        count+= BATCH_SIZE
        print(f"Read up to {count}")
    total = (datetime.datetime.now().timestamp() - start_time.timestamp())
    print(f"Scrape complete in {math.floor(total/60)} minutes and {math.floor(total%60)} seconds.")
                    






asyncio.run(main()) 
   
    
# to do:
# Find efficient way to check if ID is already in list (maybe keep it sorted then binary search?)


# Convert all duration to int:seconds
# convert observers to ints
# make bools or an array for description selections "lights on craft, left a trail, etc."