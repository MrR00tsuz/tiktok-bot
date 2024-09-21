import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_driver_path = os.path.join(os.getcwd(), "config", "data", "chromedriver.exe")

service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()

prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://zefoy.com/")

driver.delete_all_cookies()

cookies_path = os.path.join(os.getcwd(), "config", "data", "cookies", "cookies0.json")

with open(cookies_path, "r") as cookies_file:
    cookies = json.load(cookies_file)
    for cookie in cookies:
        if cookie.get('sameSite') is None:
            cookie['sameSite'] = 'None'
        driver.add_cookie(cookie)

driver.refresh()

ad_block_script = """
var ads = document.querySelectorAll('iframe, .ad, .ads, .advertisement'); 
ads.forEach(function(ad) { ad.remove(); });
"""
driver.execute_script(ad_block_script)

time.sleep(5)  
views_button_xpath = "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button"
driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, views_button_xpath))

url_path = os.path.join(os.getcwd(), "config", "data", "url.json")
with open(url_path, "r") as url_file:
    url_data = json.load(url_file)
    video_url = url_data["url"]

url_input_xpath = "/html/body/div[10]/div/form/div/input"
url_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, url_input_xpath))
)
url_input.send_keys(video_url)

search_button_xpath = "/html/body/div[10]/div/form/div/div/button"
search_button = driver.find_element(By.XPATH, search_button_xpath)
search_button.click()

while True:
    try:
        countdown_xpath = "//span[@class='br views-countdown']"
        countdown_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, countdown_xpath))
        )
        print("Süre bekleniyor...")
        
        WebDriverWait(driver, 60).until(
            EC.text_to_be_present_in_element((By.XPATH, countdown_xpath), "Next Submit: READY....!")
        )
        
        search_button.click()
        time.sleep(4)  

        tiktok_button_xpath = "//*[@id='c2VuZC9mb2xeb3dlcnNfdGlrdG9V']/div[1]/div/form/button"
        tiktok_button = driver.find_element(By.XPATH, tiktok_button_xpath)
        tiktok_button.click()
        
    except Exception as e:
        print(f"Hata: {e}")
        
        try:
            tiktok_button_xpath = "//*[@id='c2VuZC9mb2xeb3dlcnNfdGlrdG9V']/div[1]/div/form/button"
            tiktok_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, tiktok_button_xpath))
            )
            tiktok_button.click()

            time.sleep(10)  

            tiktok_button.click()
            
        except Exception as inner_e:
            print(f"İkinci hata: {inner_e}")
            continue  

