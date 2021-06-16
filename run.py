import json
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


def login():
    username = driver.find_element_by_name('email')
    username.send_keys(EMAIL)

    password = driver.find_element_by_name('password')
    password.send_keys(PASSWORD)
    time.sleep(1)

    button = driver.find_element_by_xpath('//*[@id="LoginForm"]/div[3]/button')

    button.click()


def get_episode_page(i):
    driver.get('https://anchor.fm/dashboard/episodes')
    time.sleep(10)
    page_num = (i-1) // 15
    ind = (i-1) % 15 + 1

    #try:
    for i in range(page_num):
        next_button = driver.find_element_by_xpath('//*[@id="app-content"]/div/div/div/div[3]/div/button[3]')
        next_button.click()
        time.sleep(5)
    button = driver.find_element_by_xpath(
        f'//*[@id="app-content"]/div/div/div/div[2]/ul/li[{ind}]/button')
    button.click()


def find_episodes():
    li_elements = driver.find_elements_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/ul/li')
    buttons = [x.find_element_by_tag_name(
        'button') for x in li_elements]
    print(f"{len(li_elements)} episodes found.")
    return buttons


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
    time.sleep(5)


if __name__ == '__main__':
    login()
    time.sleep(1)
    i = 1
    while True:
        get_episode_page(i)
        i += 1
        download_stats()
