import argparse
import json
from enum import Enum
import time
import os
import re

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import tqdm

class Status(Enum):
    OK = 0
    FAILED = 1
    FINISHED = 2


def main():
    parser = argparse.ArgumentParser(description='Anchor stats')
    parser.add_argument(
        '--json', help='Specify episode.json to skip scraping to make the episode list.', required=False)
    parser.add_argument(
        '--headless', help='Use Headless Chrome', action='store_true', required=False)
    args = parser.parse_args()

    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.path.dirname(__file__) + '/data'}
    chromeOptions.add_experimental_option("prefs", prefs)
    if args.headless:
        chromeOptions.add_argument('--headless')

    driver = webdriver.Chrome(executable_path='./chromedriver', options=chromeOptions)

    driver.get('https://anchor.fm/dashboard/episodes')

    num_trial = 5

    login(driver)
    time.sleep(1)
    if args.json:
        episodes = json.load(open(args.json))
    else:
        episodes = fetch_episode_list(driver, num_trial)
        json.dump(episodes, open('episodes.json', 'w'),
                  ensure_ascii=False, indent=2)

    for episode in tqdm.tqdm(episodes, desc="Downloading CSV"):
        time.sleep(1)
        download_csv(driver, episode['id'], episode['title'])
    time.sleep(5)


def login(driver):
    # ANCHOR_EMAIL, ANCHOR_PASSWORD は .env に書く
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    email = os.environ.get("ANCHOR_EMAIL")
    password = os.environ.get("ANCHOR_PASSWORD")
    username_area = driver.find_element(by=By.NAME, value='email')
    username_area.send_keys(email)

    password_area = driver.find_element(by=By.NAME, value='password')
    password_area.send_keys(password)
    time.sleep(1)

    button = driver.find_element(by=By.XPATH, value='//*[@id="LoginForm"]/div[3]/button')
    button.click()


def find_button(driver, xpath: str, num_trial: int) -> Status:
    """find button by xpath and click. return False if failed."""
    for t in range(num_trial):
        try:
            button = driver.find_element(by=By.XPATH, value=xpath)
            button.click()
            return Status.OK
        except NoSuchElementException:
            print(f"Error in finding buttons. ({t+1}/{num_trial}).")
            time.sleep(5)
    print(f"Cannot find button xpath = {xpath}")
    return Status.FAILED


def get_num_episodes(driver, num_trial, sleep_time):
    for t in range(num_trial):
        try:
            num = len(driver.find_elements(by=By.XPATH, value=
                '//*[@id="app-content"]/div/div/div/div[2]/ul/li'))
            if num == 0:
                raise Exception
            return num
        except:
            print(f"Error in counting episodes. ({t+1}/{num_trial}).")
            time.sleep(sleep_time)
    return None


def get_episode_page(driver, i: int, num_trial: int) -> Status:
    driver.get('https://anchor.fm/dashboard/episodes')
    time.sleep(10)
    page_num = (i-1) // 15
    ind = (i-1) % 15 + 1

    for _ in range(page_num):
        # find the button to the next page.
        isOK = find_button(driver,
            xpath='//*[@id="app-content"]/div/div/div/div[3]/div/div/button[3]', num_trial=num_trial)
        if isOK:
            time.sleep(10)
        else:
            # if the button to the next page not found, then finish.
            return Status.FINISHED

    num_episodes_per_page = get_num_episodes(driver, num_trial, sleep_time=5)
    if num_episodes_per_page is None or num_episodes_per_page == 0:
        return Status.FAILED

    print(
        f"Processing {ind}/{num_episodes_per_page} episodes in page {page_num+1}.")
    if ind >= num_episodes_per_page and num_episodes_per_page != 15:
        return Status.FINISHED

    return find_button(driver, xpath=f'//*[@id="app-content"]/div/div/div/div[2]/ul/li[{ind}]/button', num_trial=num_trial)


def fetch_episode_list(driver, num_trial):
    i = 1
    episodes = []
    while True:
        print(f"Processing {i}th episode.")
        status = get_episode_page(driver, i, num_trial)
        i += 1
        if status == Status.OK:
            time.sleep(5)
            url = driver.current_url
            epi_id = url.split('/')[-1]
            title = driver.find_elements(by=By.TAG_NAME, value='h1')[1].text
            # 英数字以外除去
            title = re.sub(r'\W', '', title)
            episodes.append({'id': epi_id, 'title': title})
        elif status == Status.FAILED:
            continue
        elif status == Status.FINISHED:
            break
    return episodes


def download_csv(driver, episode_id, episode_title):
    driver.get(
        f"https://anchor.fm/api/proxy/v3/analytics/episode/webEpisodeId:{episode_id}/plays?&timeInterval=86400&limit=3&csvFilename={episode_title}.csv")


if __name__ == '__main__':
    main()
