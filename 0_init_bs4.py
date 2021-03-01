from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import io
import pandas as pd

driver = webdriver.Chrome('data/chromedriver.exe')
driver.get("https://www.google.fr/maps/")
search = driver.find_element_by_name('q')
search.clear()
search.send_keys("supertripper", Keys.ENTER)
soup = BeautifulSoup(driver.text,"html.parser")
time.sleep(3)
mydivs = soup.find("div", class_="ugiz4pqJLAG__primary-text")
print(mydivs)