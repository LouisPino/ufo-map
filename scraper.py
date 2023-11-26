from bs4 import BeautifulSoup
import json
import aiohttp
from aiohttp import ClientError
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import requests

base_url = "https://nuforc.org/sighting/?id="
# file_path = "ufo-data.json"
file_path = "test.json"
# file_path = "ufo-data-long-test.json"


try:
    with open(file_path, "r") as file:
        data_dict = json.load(file)
except FileNotFoundError:
    data_dict = {"data": []}




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
                    # Parse HTML as needed
                    return soup
                else:
                    # Handle other content types or raise an error
                    raise ValueError(f'Unexpected content type: {content_type}')
        except (ClientError, asyncio.TimeoutError) as e:
                if attempt < retry_count - 1:
                    await asyncio.sleep(delay)
                    delay *= 2  # Double the delay for the next retry
                else:
                    raise e  # Reraise the exception after the last retry

async def main():
    count = 0
    while count < 179135 :
        async with aiohttp.ClientSession() as session:
            # Fetch data for each ID concurrently
            results = await asyncio.gather(
                *[fetch_data(session, id) for id in range(count, count + 1000)]
            )
            # Process results as needed
            for idx, result in enumerate(results):
                    print(idx)
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
                    # new_vids = soup.find_all("video")
                    # vid_links = []
                    # for i in range(0, len(new_vids)):
                    #     vid = str(new_vids[i]).split("src=")[1].split('"')[1]
                    #     print(vid)
                    #     vid_links.append(vid)
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
                        "characteristics": new_entry.split("<b>Characteristics:</b> ")[1].split("<p style=\"color: white;")[0].replace("<br/>", ". ").replace("<br>", ". ") if "Characteristics" in new_entry else "" ,   
                        "images": img_links,
                        # "videos": vid_links,
                        }
                    
                    if new_dict["occurred"] != "" and new_dict["location"] != "":
                        data_dict["data"].append(new_dict)
                    # Write the updated dictionary back to the file in proper JSON format
                    
        with open(file_path, "w") as outfile:
            json.dump(data_dict, outfile, indent=4)   
        print(f"Read up to {count}")
        count+=1000
                    






asyncio.run(main()) 


# # Write the updated dictionary back to the file in proper JSON format
# with open(file_path, "w") as outfile:
#     json.dump(data_dict, outfile, indent=4)   
    
   
    
# to do:
# get videos
# Find efficient way to check if ID is already in list (maybe keep it sorted then binary search?)
# error handling so you can just go through the whole site.
# server disconnect handling
# Just write to a database instead?
# Some don't have a characteristics title but do have descriptions, get this somehow
# the word characteristics may exist in description, account for this