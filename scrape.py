# coding: utf-8
import sys

import requests

from bs4 import BeautifulSoup
# !apt-get update
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
# !pip install selenium

from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='/Users/kentarosugahara/Downloads/chromedriver',options=options)
driver.implicitly_wait(10)
print(driver)

query = "日本の城"
url = "https://www.google.com/search?q={}&hl=ja&tbm=isch".format(query)
# print(url)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

driver.get(url)
html = driver.page_source.encode("utf-8")
soup = BeautifulSoup(html, "html.parser")

soup

soup.find_all("img")
# print(soup)

img_tags = soup.find_all("img")
# print(len(img_tags))

img_urls = []

for img_tag in img_tags:
    url = img_tag.get("src")

    if url is None:
        url = img_tag.get("data-src")

    if url is not None:
        img_urls.append(url)
        # print(url)
def download_image(url, file_path):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(r.content)
        
import base64

def save_base64_image(data, file_path):
    data = data + '=' * (-len(data) % 4)
    img = base64.b64decode(data.encode())
    with open(file_path, "wb") as f:
        f.write(img)

import os
import re

classes = ["Japanese_castle","Europe_castle","Chinese_castle"]
for castle_name in classes:
    save_dir = "castle/{}".format(castle_name)

    os.makedirs(save_dir, exist_ok=True)

    base64_string = "data:image/jpeg;base64,"

    png_base64_string = "data:image/png;base64,"


    for index, url in enumerate(img_urls):
        file_name = "{}.jpg".format(index)

        image_path = os.path.join(save_dir, file_name)

        if len(re.findall(base64_string, url)) > 0 or len(re.findall(png_base64_string, url)) > 0:
            url = url.replace(base64_string, "")
            save_base64_image(data=url, file_path=image_path)
        else:
            download_image(url=url, file_path=image_path)




