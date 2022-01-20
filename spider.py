import time
import csv
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# chromedriver will execute the program on our behalf
DRIVER_PATH = "/path/to/chromedriver"
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

# -------------------------------------------------------------------------
# Step 1: Accessing the Office of the Integrity Commissioner's website

url = "https://pds.oico.on.ca/Pages/Public/PublicDisclosures.aspx"
driver.get(url)
print("Got the URL")
time.sleep(1)

# -------------------------------------------------------------------------
# Step 2: Creating a new csv with headers

with open('ontario_public_register_data.csv', 'w', newline='') as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(["as_of", "mpp_name", "riding", "income",
                 "assets", "liabilities", "gifts", "offices"])

# -------------------------------------------------------------------------
# Step 3: Finding all the years the IC has data for + and creating a year loop

    raw_years = driver.find_element_by_id(
        "BodyContent_ddlYear").text.splitlines()[1:]
    years = [s.strip() for s in raw_years]

    for i in range(0, len(years)):
        year = years[i]
        year_dropdown = Select(WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BodyContent_ddlYear"))))
        year_dropdown.select_by_value(year)
        print("Got the YEAR: " + year)
        time.sleep(1)

# -------------------------------------------------------------------------
# Step 4: Finding all the MPPs the IC has data for + and creating an MPP loop

        raw_mpps = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "BodyContent_ddlMemberName")))
        options = [x for x in raw_mpps.find_elements_by_tag_name("option")]

        mpps = []

        for mpp_value in options[1:]:
            mpp = mpp_value.get_attribute("value")
            mpps.append(mpp)

        for i in range(0, len(mpps)):
            mpp = mpps[i]
            mpp_dropdown = Select(WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "BodyContent_ddlMemberName"))))
            mpp_dropdown.select_by_value(mpp)
            time.sleep(1)

# -------------------------------------------------------------------------
# Step 5: Getting all relevant data for corresponding MPP and year

            date = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "BodyContent_fldAsOf"))).text
            name = driver.find_element_by_id("BodyContent_fldMemberName").text
            riding = driver.find_element_by_id("BodyContent_fldRiding").text
            income = driver.find_element_by_id("BodyContent_fldMppIncome").text
            assets = driver.find_element_by_id("BodyContent_fldMppAssets").text
            liabilities = driver.find_element_by_id(
                "BodyContent_fldMppLiabilities").text
            gifts = driver.find_element_by_id(
                "BodyContent_fldGiftsAndBenefits").text
            offices = driver.find_element_by_id("BodyContent_fldOffices").text

# -------------------------------------------------------------------------
# Step 6: Writing rows in our csv file. Rinse and repeat.

            wr.writerow([date, name, riding, income, assets,
                         liabilities, gifts, offices])
            print("Printed row for: " + name + " - " + date)
            time.sleep(5)
