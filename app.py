from selenium import webdriver
import pandas as pd
from IPython.display import display
import time

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Drive config setup
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


def scrolToBottom(driver):
    # Scrol to the bottom
    SCROLL_PAUSE_TIME = 0.5
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


def getElementByXPath(driver, path):
    element = False
    while element == False:
        try:
            element = driver.find_element(
                "xpath", path)
            time.sleep(0.5)
        except:
            continue
    return element


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
    time.sleep(3)

    scrolToBottom(driver)

    element = driver.find_element(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div[3]/div[1]/div/div[2]/div/div/div/div/table/tbody/tr[3]/td[2]/a")
    element.click()
    time.sleep(3)

    scrolToBottom(driver)

    elements = driver.find_elements(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li")
    pages = len(elements) - 4

    flipButton = driver.find_element(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li[" + str(len(elements)-1) + "]/a")

    jobIDs = []
    jobTitles = []
    for i in range(pages):
        newJobIDs = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[3]")
        for each in newJobIDs:
            jobIDs.append(each.text)

        newJobTitles = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[4]")

        for each in newJobTitles:
            jobTitles.append(each.text)

        flipButton.click()
        time.sleep(2)
        flipButton = driver.find_element(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li[" + str(len(elements)-1) + "]/a")

    for i in range(len(jobTitles)):
        jobTitles[i] = jobTitles[i].replace("NEW ", "")
    print(len(jobIDs))
    dict1 = {
        'IDs': jobIDs,
        'Titles': jobTitles
    }
    df = pd.DataFrame(dict1)
    df.to_excel('Jobs.xlsx', sheet_name='Jobs')


test()
