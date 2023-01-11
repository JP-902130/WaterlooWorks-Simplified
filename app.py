from selenium import webdriver
import pandas as pd
from IPython.display import display
import time


def test():
    driver = webdriver.Chrome()
    driver.get(
        "https://waterlooworks.uwaterloo.ca/myAccount/co-op/coop-postings.htm")

    element = driver.find_element(
        "xpath", "/html/body/div[3]/div/div/div[3]/div/div/div/a")

    element.click()
    time.sleep(10)


test()
