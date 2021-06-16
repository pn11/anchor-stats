import json
from enum import Enum
import time
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException


# EMAIL, PASSWORD は .env に書く
load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.path.dirname(__file__) + '/data'}
chromeOptions.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=chromeOptions)

driver.get('https://anchor.fm/dashboard/episodes')

NUM_TRIAL = 5

class Status(Enum):
    OK = 0
    FAILED = 1
    FINISHED = 2

def login():
    username = driver.find_element_by_name('email')
    username.send_keys(EMAIL)

    password = driver.find_element_by_name('password')
    password.send_keys(PASSWORD)
    time.sleep(1)

    button = driver.find_element_by_xpath('//*[@id="LoginForm"]/div[3]/button')
    button.click()


def find_button(xpath: str, num_trial: int)->Status:
    """find button by xpath and click. return False if failed."""
    for t in range(num_trial):
        try:
            button = driver.find_element_by_xpath(xpath)
            button.click()
            return Status.OK
        except NoSuchElementException:
            print(f"Error in finding buttons. ({t+1}/{NUM_TRIAL}).")
            time.sleep(5)
    print(f"Cannot find button xpath = {xpath}")
    return Status.FAILED


def get_num_episodes(num_trial, sleep_time):
    for t in range(num_trial):
        try:
            num = len(driver.find_elements_by_xpath('//*[@id="app-content"]/div/div/div/div[2]/ul/li'))
            if num == 0:
                raise Exception
            return num
        except:
            print(f"Error in counting episodes. ({t+1}/{NUM_TRIAL}).")
            time.sleep(sleep_time)
    return None


def get_episode_page(i: int) ->Status:
    driver.get('https://anchor.fm/dashboard/episodes')
    time.sleep(10)
    page_num = (i-1) // 15
    ind = (i-1) % 15 + 1

    for _ in range(page_num):
        # find the button to the next page.
        isOK = find_button(xpath='//*[@id="app-content"]/div/div/div/div[3]/div/button[3]', num_trial=NUM_TRIAL)
        if isOK:
            time.sleep(10)
        else:
            # if the button to the next page not found, then finish.
            return Status.FINISHED
    
    num_episodes_per_page = get_num_episodes(num_trial=NUM_TRIAL, sleep_time=5)
    if num_episodes_per_page is None or num_episodes_per_page == 0:
        return Status.FAILED
    
    print(f"Processing {ind}/{num_episodes_per_page} episodes in page {page_num+1}.")
    if ind >= num_episodes_per_page and num_episodes_per_page != 15:
        return Status.FINISHED
    
    return find_button(xpath=f'//*[@id="app-content"]/div/div/div/div[2]/ul/li[{ind}]/button',  num_trial=NUM_TRIAL)


def download_stats():
    time.sleep(10)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/div[1]/div[6]/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[1]/div/div/div/div/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[1]/div/div/div/div[2]/div/div/div[1]/div/div').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[3]/div[3]/div/div/div/a').click()
    print('Downloading', driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/h1').text)
    time.sleep(5)


if __name__ == '__main__':
    login()
    time.sleep(1)
    i = 1
    while True:
        print(f"Processing {i}th episode.")
        status = get_episode_page(i)
        i += 1
        if status == Status.OK:
            download_stats()
        elif status == Status.FAILED:
            continue
        elif status == Status.FINISHED:
            break
