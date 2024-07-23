from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# ------------ SOUP DATA FROM ZILLOW LISTINGS -------------#

ZILLOW_LINK = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_LINK)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")

results = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
price_result = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")


links = []
addresses = []
prices = []

for n in results:
    link = n.get("href")
    links.append(link)
    address = n.text
    addresses.append(address.strip())

for p in price_result:
    price = p.text
    prices.append(price.replace("+/mo", "")
                  .replace("/mo", "")
                  .replace("+ 1 bd", "")
                  .replace("+ 1bd", ""))

# print(links)
# print(addresses)
# print(prices)

data = {}

for n in range(len(links)):
    data[n] = {
        "address": addresses[n],
        "price": prices[n],
        "link": links[n]
    }

# print(data[1])

# -------------------- SELENIUM ------------------------#


GOOGLE_FORM_LINK = ("https://docs.google.com/forms/d/e/1FAIpQLSdlY8RV45IQKnRKcKCIXWEFpFj5O9PSpz"
                    "YPlxpBBUvfig-QLw/viewform?usp=sf_link")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(GOOGLE_FORM_LINK)
time.sleep(5)


for item in range(len(data)):

    add_address = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/"
                                                    "div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    add_address.send_keys(data[item]["address"], Keys.ENTER)
    time.sleep(3)

    add_price = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/"
                                                    "div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    add_price.send_keys(data[item]["price"], Keys.ENTER)
    time.sleep(3)

    add_link = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/"
                                                    "div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    add_link.send_keys(data[item]["link"], Keys.ENTER)
    time.sleep(3)

    submit_button = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/"
                                                "div[1]/div[1]/div/span/span")
    submit_button.click()
    time.sleep(5)
    another_response = driver.find_element(By.LINK_TEXT, value="Submit another response")
    another_response.click()








