from selenium import webdriver
import pandas as pd
from IPython.display import display
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import languageProcessing
# Drive config setup
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

load_dotenv()


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


def scrapDataFromShortListAndStoreInExcel():
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
    element.send_keys(os.getenv('USERNAME'))

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span[2]")
    element.click()

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/input")
    element.send_keys(os.getenv('PASSWORD'))

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
    jobOpenings = []
    jobApplicants = []
    jobCompanies = []

    for i in range(pages):
        newJobIDs = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[3]")
        for each in newJobIDs:
            jobIDs.append(each.text)

        newJobTitles = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[4]")
        for each in newJobTitles:
            jobTitles.append(each.text)

        newJobOpenings = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[7]")
        for each in newJobOpenings:
            jobOpenings.append(int(each.text))

        newJobApplicants = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[11]")
        for each in newJobApplicants:
            jobApplicants.append(int(each.text))

        newJobCompanies = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[5]/span")

        for each in newJobCompanies:
            try:
                jobCompanies.append(each.text)
            except:
                continue

        flipButton.click()
        time.sleep(2)
        flipButton = driver.find_element(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li[" + str(len(elements)-1) + "]/a")

    for i in range(len(jobTitles)):
        jobTitles[i] = jobTitles[i].replace("NEW ", "")

    dict1 = {
        'JobID': jobIDs,
        'Titles': jobTitles,
        'Openings': jobOpenings,
        'Applicants': jobApplicants,
        'Companies': jobCompanies
    }
    df = pd.DataFrame(dict1)
    df["Competitive Index"] = df["Applicants"] / df["Openings"]
    df.to_excel('Jobs.xlsx', sheet_name='Jobs')


def checkEachJobAndCalculateMatchingIndex():
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
    element.send_keys(os.getenv('USERNAME'))

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div/div/form/div[2]/div[4]/span[2]")
    element.click()

    element = driver.find_element(
        "xpath", "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div/form/div[2]/div[2]/input")
    element.send_keys(os.getenv('PASSWORD'))

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

    elements = driver.find_elements(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li")
    pages = len(elements) - 4

    flipButton = driver.find_element(
        "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li[" + str(len(elements)-1) + "]/a")

    jobIDs = []
    jobDescriptions = []
    jobMatchIndexes = []

    for i in range(pages):
        buttonsVisited = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[4]/span/a")

        buttonsNotVisited = driver.find_elements(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[3]/table/tbody/tr/td[4]/strong/span/a")

        buttons = buttonsNotVisited + buttonsVisited

        count = 0
        for each in buttons:
            # if count > 2:
            #     break
            count += 1

            each.click()
            driver.switch_to.window(driver.window_handles[1])

            # Inside this page
            jobTitle = driver.find_element(
                "xpath", "/html/body/main/div[1]/div/div[2]/div/div[2]/h1")
            jobId = languageProcessing.getIDFromString(jobTitle.text)
            print(jobId)
            # path to all li
            liXPATH = "/html/body/main/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/table/tbody//tr[td/strong[contains(text(), 'Required Skills')]]/td[2]//li"
            # all li in required skills
            target_li = driver.find_elements("xpath", liXPATH)
            matchingCount = 0

            description = ""
            if len(target_li) != 0:
                for each in target_li:
                    # print(each.text)
                    description = description + each.text
                    matchingCount += languageProcessing.getMatchingIndex(
                        each.text)
            else:
                spanPath = "/html/body/main/div[4]/div/div/div/div[2]/div/div[1]/div/div[1]/div[2]/table/tbody//tr[td/strong[contains(text(), 'Required Skills')]]/td[2]/span"
                spanObj = driver.find_element("xpath", spanPath)
                # print(spanObj.text)
                description = description + spanObj.text
                matchingCount += languageProcessing.getMatchingIndex(
                    spanObj.text)

            # Add the result to a list

            jobIDs.append(jobId)
            jobDescriptions.append(description)
            jobMatchIndexes.append(matchingCount)

            # Get back
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        flipButton.click()
        time.sleep(2)
        flipButton = driver.find_element(
            "xpath", "/html/body/main/div[2]/div/div/div/div[2]/div/div/div/div/div[3]/div[4]/div/ul/li[" + str(len(elements)-1) + "]/a")
        driver.execute_script("window.scrollTo(0, 220)")
    df = pd.DataFrame(
        {'JobID': jobIDs, 'JobDescription': jobDescriptions, 'JobMatchIndex': jobMatchIndexes})
    df.to_excel('matchIndex.xlsx', index=False)
