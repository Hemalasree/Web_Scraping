from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random
import os

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

products = []

for page in range(1, 6):
    url = f"https://www.flipkart.com/search?q=tv&page={page}"
    driver.get(url)
    time.sleep(random.uniform(4, 7))

    try:
        driver.find_element(By.XPATH, "//button[contains(text(),'✕')]").click()
    except:
        pass

    cards = driver.find_elements(By.CSS_SELECTOR, "div._1AtVbE")

    for card in cards:
        try:
            name = card.find_element(By.CSS_SELECTOR, "div._4rR01T").text
            price = card.find_element(By.CSS_SELECTOR, "div._30jeq3").text
            rating = card.find_element(By.CSS_SELECTOR, "div._3LWZlK").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

            products.append([name, price, rating, link])
        except:
            pass

driver.quit()

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "flipkart_tvs.xlsx")

df = pd.DataFrame(products, columns=["Name", "Price", "Rating", "Link"])
df.to_excel(file_path, index=False)

print(f"Flipkart TV data saved to: {file_path}")
