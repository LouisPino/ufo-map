from bs4 import BeautifulSoup
import json
import requests

url = "https://nuforc.org/sighting/?id="
file_path = "ufo-data.json"


try:
    with open(file_path, "r") as file:
        data_dict = json.load(file)
except FileNotFoundError:
    data_dict = {"data": []}


for i in range(100):
    print(i)
    html = requests.get(url + str(i + 179015))
    soup = BeautifulSoup(html.content, 'html.parser')
    new_entry = str(soup.find("div", class_="content-area"))
    new_dict = {
        "occurred": new_entry.split("<b>Occurred:</b> ")[1].split(" Local<br/>")[0],
        "location": new_entry.split("<b>Location:</b> ")[1].split("<br/>")[0],
        "location_details": new_entry.split("details:</b> ")[1].split("<br/>")[0] if "Location details" in new_entry else "",
        "shape": new_entry.split("<b>Shape:</b> ")[1].split("<br/>")[0],
        "duration": new_entry.split("<b>Duration:</b> ")[1].split("<br/>")[0],
        "observers": new_entry.split("<b>No of observers:</b> ")[1].split("<br/>")[0] if "No of observers" in new_entry else "",
        "reported": new_entry.split("<b>Reported:</b> ")[1].split("<br/>")[0],
        "posted": new_entry.split("<b>Posted:</b> ")[1].split("<br/>")[0],
        "characteristics": new_entry.split("<b>Characteristics:</b> ")[1].split("<p style=\"color: white;")[0].replace("<br/>", "").replace("<br>", "") if "Characteristics" in new_entry else ""    
        }
    if new_dict["occurred"] != "" and new_dict["location"] != "":
        data_dict["data"].append(new_dict)


# Write the updated dictionary back to the file in proper JSON format
with open(file_path, "w") as outfile:
    json.dump(data_dict, outfile, indent=4)   
    
    
    
# to do:
# get pictures
# miht need to add checks to all fields
# add try catch (whatever python equiv is) before trying to run on large set