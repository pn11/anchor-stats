import json
import time
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.select import Select


# EMAIL, PASSWORD は .env に書く
load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.path.dirname(__file__)} # this does not work currently
chromeOptions.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chromeOptions)

driver.get('https://anchor.fm/dashboard/episodes')


def login():
    username = driver.find_element_by_name('email')
    username.send_keys(EMAIL)

    password = driver.find_element_by_name('password')
    password.send_keys(PASSWORD)
    time.sleep(1)

    button = driver.find_element_by_xpath('//*[@id="LoginForm"]/div[3]/button')

    button.click()


def find_episodes():
    li_elements = driver.find_elements_by_xpath(
        '//*[@id="app-content"]/div/div/div/div[2]/ul/li')
    links = [x.find_element_by_tag_name(
        'a').get_attribute('href') for x in li_elements]
    print(f"{len(li_elements)} episodes found.")
    return links


def download_stats(link):
    driver.get(link)
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


login()
time.sleep(10)
links = find_episodes()
print(links)
for l in links:
    download_stats(l)
