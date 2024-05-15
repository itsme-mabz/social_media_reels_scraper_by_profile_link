# Social Media Scraper

## Overview
This scraper is designed to download videos from various social media platforms such as TikTok, Facebook, Douyin, and Kuaishou. Simply provide the user's profile link, follow the setup instructions, and the scraper will fetch and download all the videos associated with that user.

## Prerequisites
Before using the scraper, ensure you have the following installed:
- Python 3.x
- Google Chrome browser
- Chrome Web Store account

## Installation
1. Clone this repository to your local machine.
2. Open the cloned folder in your terminal.
3. Set up a virtual environment:
    ```
    python -m venv .env
    source .env/bin/activate
    ```
4. Install the required Python packages:
    ```
    pip install -r requirements.txt
    ```
    
5. Install the "Cookie editor" extension from the Chrome Web Store:
- Open Chrome and visit the [Cookie editor extension](https://chrome.google.com/webstore/search/cookie%20editor) page.
- Install the first available extension.
6. Login to the respective social media platform(s) (Facebook, TikTok, Douyin, Kuaishou) in your Chrome browser and refresh the page.

## Usage
1. Export Cookies:
- Click on the "Cookie editor" extension icon in Chrome.
- Choose the "Export" option and select JSON format.
- Copy the exported cookies to a `cookies.json` file in the respective platform's folder (e.g., `facebook/cookies.json`).
2. Run the scraper:
- Navigate to the desired platform's folder:
  ```
  cd facebook
  ```
- Execute the scraper script:
  ```
  python v1.py
  ```

The scraper will start fetching and downloading the videos associated with the provided user profile link. Enjoy!

## Note
- Ensure that you have proper permissions to download content from the targeted social media platforms.
- Respect the terms of service and privacy policies of each platform.
- Use responsibly and legally.
