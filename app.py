from selenium import webdriver
import pandas as pd
from IPython.display import display
import time

# Drive config setup
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


def test():
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(
        "https://waterlooworks.uwaterloo.ca/myAccount/co-op/coop-postings.htm")
    element = driver.find_element(
        "xpath", "/html/body/div[3]/div/div/div[3]/div/div/div/a")
    element.click()

    element = driver.find_element(
        "xpath", "/html/body/div[3]/div/div/div[5]/div/div/a[1]")
    element.click()

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[1]/input")
    element.send_keys("j75peng@uwaterloo.ca")

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span[2]")
    element.click()

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/input")
    element.send_keys("Pjc031209!")

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div/form/div[2]/div[4]/span[1]")
    element.click()
    time.sleep(10)

    element = driver.find_element(
        "xpath", "/html/body/div[2]/header/div[3]/div[1]/nav/ul/li[2]/a")
    element.click()

    SCROLL_PAUSE_TIME = 0.5

# Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    element = driver.find_element(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[3]/td[2]/a")
    element.click()


test()
