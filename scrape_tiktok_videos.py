from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        '__cflb': '0H28v8EEysMCvTTqtu4Ydr4bADFLp2DZoSXwXt1WQ9T',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'HX-Request': 'true',
        'HX-Trigger': '_gcaptcha_pt',
        'HX-Target': 'target',
        'HX-Current-URL': 'https://ssstik.io/en',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://ssstik.io',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://ssstik.io/en',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'cGVNOTk2', # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }
    
    
    

    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as f:
        while True:
            data = mp4File.read(4096)
            if data:
                f.write(data)
            else:
                break



print("STEP 1: Open Firefox browser")
driver = webdriver.Firefox()
# Tiktok link
driver.get("https://www.tiktok.com/@celinedept")

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 

soup = BeautifulSoup(driver.page_source, "html.parser")
# this class may change, so make sure to inspect the page and find the correct class
videos = soup.find_all("div", {"class": "tiktok-x6y88p-DivItemContainerV2 e19c29qe8"})
print(videos)
print(f"STEP 3: Time to download {len(videos)} videos")

for index, video in enumerate(videos):
    print(f"Downloading video: {index}")
    downloadVideo(video.a["href"], index)
    time.sleep(10)