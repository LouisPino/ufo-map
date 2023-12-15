import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re


video_ids = []

with open("vid_list.txt") as vid_list:
    video_ids = json.load(vid_list)

with open("Scrape2.json") as scrape2:
    scrape_data = json.load(scrape2)

for sighting in scrape_data["data"]:
    if sighting["id"] in video_ids:
        sighting["video"] = 1
    else:
        sighting["video"] = 0

with open("Scrape2.json", "w") as outfile:
            json.dump(scrape_data, outfile, indent=4)   


# Selenium 
# driver = webdriver.Chrome()
# driver.get(f"https://nuforc.org/sighting/?id={video_ids[0]}")
# assert "NUFORC" in driver.title
# pattern = re.compile(r"museai-player")
# elements = driver.find_elements(By.TAG_NAME, "div")
# video_player = [elem for elem in elements if pattern.search(elem.get_attribute('id'))][0]
# print(video_player)
# driver.close()

# Videos are blocked by Muse.ai video host. :( Will just have to link to pages that have videos :(